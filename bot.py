"""机器人主逻辑 — 消息轮询、AI 回复、命令处理"""

import logging
import os
import signal
import sys
import time
from datetime import datetime

from console_ui import Console
from config import Config
from oj_client import OjClient
from ai_client import AiClient
from command_parser import parse, CommandResult, execute_actions, ADMIN_ACTION_PROMPT
from web_tools import get_current_time

try:
    from web_server import BotState
except ImportError:
    class BotState:
        class _lock:
            @staticmethod
            def __enter__(*a): pass
            @staticmethod
            def __exit__(*a): pass
        def __init__(self):
            self.lock = self._lock()
            self.running = False
            self.status_text = ""
            self.messages_processed = 0
            self.active_users = 0
        def snapshot(self): return {"running": self.running}

logger = logging.getLogger(__name__)


class Bot:
    """小恐龙 OJ 自动回复机器人"""

    def __init__(self, config: Config, bot_state: BotState | None = None):
        self.config = config
        self.oj = OjClient(config)
        self.ai = AiClient(config, bot_state=bot_state)
        self.seen_ids: set[str] = set()
        self.running = False
        self.state: BotState = bot_state or BotState()

    # ── 入口 ──

    def run(self):
        """启动主循环"""
        Console.setup_ansi()
        os.system("cls" if sys.platform == "win32" else "clear")
        Console.banner(self.config)

        if not self.oj.login():
            Console.warn("OJ 登录失败，按 Enter 退出...")
            self._pause()
            return

        self.oj.my_id = self.oj.fetch_my_id()
        if not self.oj.my_id:
            Console.error("无法获取用户信息")
            self._pause()
            return

        self._seed_seen_ids()
        Console.info(f"用户 ID: {self.oj.my_id}")
        Console.info(f"已记录 {len(self.seen_ids)} 条历史消息")
        Console.ok("开始监听消息...")
        Console.blank()

        self.running = True
        with self.state.lock:
            self.state.running = True
            self.state.status_text = "监听中..."
        signal.signal(signal.SIGINT, self._on_signal)
        signal.signal(signal.SIGTERM, self._on_signal)

        heartbeat_ts = time.time()

        while self.running:
            with self.state.lock:
                if not self.state.running:
                    self.running = False
                    break

            try:
                data = self.oj.fetch_messages()
                if data is None:
                    Console.warn("连接异常，正在重新登录...")
                    with self.state.lock:
                        self.state.status_text = "重新登录中..."
                    if self.oj.login():
                        self.oj.my_id = self.oj.fetch_my_id()
                    time.sleep(self.config.poll_interval)
                    continue

                for uid, conv in data.get("messages", {}).items():
                    for msg in conv.get("messages", []):
                        self._process(msg, conv)

                with self.state.lock:
                    if self.state.status_text == "重新登录中...":
                        self.state.status_text = "监听中..."

                now = time.time()
                if now - heartbeat_ts > 300:
                    logger.info(
                        f"心跳正常 | 已处理 {len(self.seen_ids)} 条消息"
                    )
                    Console.heartbeat(len(self.seen_ids), 0)
                    heartbeat_ts = now

            except Exception as e:
                logger.exception("主循环异常")

            time.sleep(self.config.poll_interval)

        with self.state.lock:
            self.state.running = False
            self.state.status_text = "已停止"
        self.oj.close_session()
        Console.warn("机器人已停止")

    # ── 消息处理 ──

    def _seed_seen_ids(self):
        data = self.oj.fetch_messages()
        if not data:
            return
        for conv in data.get("messages", {}).values():
            for msg in conv.get("messages", []):
                self.seen_ids.add(msg.get("_id"))

    def _process(self, msg: dict, conv: dict):
        """处理单条消息"""
        msg_id = msg.get("_id")
        if msg_id in self.seen_ids:
            return
        self.seen_ids.add(msg_id)

        sender = msg.get("from")
        content = msg.get("content", "")
        sender_name = conv.get("udoc", {}).get("uname", f"用户{sender}")

        if sender == self.oj.my_id or not content.strip():
            return

        now = datetime.now().strftime("%H:%M:%S")
        content = content.strip()
        Console.divider()
        Console.msg_in(now, sender_name, sender, content)

        result = parse(content, sender, self.config)
        reply_text = None

        if result.reply is not None:
            reply_text = result.reply

        elif result.status_request:
            reply_text = self._get_status_report()

        else:
            matched = [w for w in self.config.blocked_words if w in content]
            if matched:
                words = "、".join(f"「{w}」" for w in matched)
                reply_text = f"消息包含屏蔽词 {words}，已忽略"
                Console.blocked(words)
            else:
                # 先发送即时反馈，避免用户空等
                self._send_reply(sender, "🤖 AI思考中，请稍等...")
                Console.think_start()

                # 构建系统提示
                history = []
                if sender == self.config.admin_id:
                    _sys_extra = {"role": "system", "content": ADMIN_ACTION_PROMPT.strip()}
                    history = [_sys_extra]

                reply_text = self.ai.ask(content, history=history)

                if reply_text is None:
                    reply_text = "AI 回复失败，请稍后重试"
                else:
                    # 执行 AI 动作指令（仅管理员）
                    if sender == self.config.admin_id:
                        reply_text = execute_actions(reply_text, self.config)

                    for w in self.config.blocked_words:
                        if w in reply_text:
                            reply_text = reply_text.replace(w, "*" * len(w))
                            Console.blocked("AI 输出已打码")

        Console.msg_out(reply_text)
        self._send_reply(sender, reply_text)

        with self.state.lock:
            self.state.messages_processed += 1

    def _send_reply(self, to_uid: int, text: str, retries: int = 2):
        """发送回复（失败重试）"""
        for attempt in range(retries + 1):
            ok, resp = self.oj.send_message(to_uid, text)
            if ok:
                Console.sent(True)
                mdoc = resp.get("mdoc", {})
                if mdoc.get("_id"):
                    self.seen_ids.add(mdoc["_id"])
                return
            logger.warning(f"发送失败，正在重试 ({attempt + 1}/{retries})")
            time.sleep(1)
        Console.sent(False, retries)

    def _notify_admin(self, user_id: int, user_name: str):
        """通知管理员有新申请"""
        msg = (
            f"【申请】用户 {user_name}(ID:{user_id}) 申请加入白名单\n"
            f"输入 #同意申请 {user_id} 批准"
        )
        ok, _ = self.oj.send_message(self.config.admin_id, msg)
        if ok:
            Console.notify("已通知管理员")

    @staticmethod
    def _check_deepseek_balance(api_key: str) -> str:
        """查询 DeepSeek 账户余额"""
        try:
            import requests
            resp = requests.get(
                "https://api.deepseek.com/user/balance",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                infos = data.get("balance_infos", [])
                if infos:
                    parts = []
                    for b in infos:
                        cur = b.get("currency", "CNY")
                        total = b.get("total_balance", "0")
                        parts.append(f"  {cur} {total}")
                    return "\n".join(parts)
                return "无余额信息"
            return f"查询失败 (HTTP {resp.status_code})"
        except Exception as e:
            return f"查询异常: {e}"

    def _get_status_report(self) -> str:
        """生成机器人运行状态报告"""
        import time as _time
        from datetime import datetime as _dt

        started = self.state.started_at
        try:
            st = _dt.fromisoformat(started)
            elapsed = _time.time() - st.timestamp()
            hours, rem = divmod(int(elapsed), 3600)
            mins, secs = divmod(rem, 60)
            uptime_str = f"{hours}小时{mins}分{secs}秒"
        except Exception:
            uptime_str = "未知"

        with self.state.lock:
            processed = self.state.messages_processed
            active = self.state.active_users

        balance = self._check_deepseek_balance(self.config.ai["api_key"])
        now = get_current_time()

        lines = [
            "===== HydroAI 运行状态 =====",
            f"当前时间: {now}",
            f"运行时长: {uptime_str}",
            f"已处理消息: {processed} 条",
            f"白名单: {len(self.config.allowed_ids())} 人",
            f"屏蔽词: {len(self.config.blocked_words)} 个",
            f"AI 模型: {self.config.ai['model']}",
            f"轮询间隔: {self.config.poll_interval} 秒",
            "------------------------",
            "DeepSeek 余额:",
            balance,
        ]
        return "\n".join(lines)

    def _on_signal(self, sig, frame):
        self.running = False
        with self.state.lock:
            self.state.running = False
        Console.warn("正在停止...")

    @staticmethod
    def _pause():
        try:
            input()
        except Exception:
            pass
