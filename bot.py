"""机器人主逻辑 — 消息轮询、AI 回复、命令处理"""

import logging
import os
import signal
import sys
import time
from datetime import datetime

from config import Config, RST, RED, GRN, YEL, BLU, CYN, DIM
from oj_client import OjClient
from ai_client import AiClient
from command_parser import parse, CommandResult, execute_actions, ADMIN_ACTION_PROMPT

try:
    from web_server import BotState
except ImportError:
    # 兼容没有 web_server.py 的情况
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

# 所有 print 强制即时刷新（防止 Windows 控制台缓冲不显示）
def p(*args, **kwargs):
    kwargs["flush"] = True
    print(*args, **kwargs)


class ConversationMemory:
    """对话上下文记忆（内存），保留最近 N 轮"""

    def __init__(self, max_rounds: int = 6):
        self.max_rounds = max_rounds
        self._data: dict[int, list[dict]] = {}

    def history(self, user_id: int) -> list[dict]:
        return self._data.get(user_id, [])[-self.max_rounds * 2:]

    def add(self, user_id: int, role: str, content: str):
        self._data.setdefault(user_id, [])
        self._data[user_id].append({"role": role, "content": content})
        limit = self.max_rounds * 2
        if len(self._data[user_id]) > limit:
            self._data[user_id] = self._data[user_id][-limit:]

    def clear(self, user_id: int):
        self._data.pop(user_id, None)

    @property
    def active_users(self) -> int:
        return len(self._data)


class Bot:
    """小恐龙 OJ 自动回复机器人"""

    def __init__(self, config: Config, bot_state: BotState | None = None):
        self.config = config
        self.oj = OjClient(config)
        self.ai = AiClient(config, bot_state=bot_state)
        self.memory = ConversationMemory(max_rounds=6)
        self.seen_ids: set[str] = set()
        self.running = False
        self.state: BotState = bot_state or BotState()

    # ── 入口 ──

    def run(self):
        """启动主循环"""
        self._setup_console()
        os.system("cls" if sys.platform == "win32" else "clear")

        self._print_banner()

        if not self.oj.login():
            self._pause()
            return

        self.oj.my_id = self.oj.fetch_my_id()
        if not self.oj.my_id:
            p(f"  {RED}[错误]{RST} 无法获取用户信息")
            self._pause()
            return

        self._seed_seen_ids()

        p(f"  {BLU}·{RST} 用户 ID: {self.oj.my_id}")
        p(f"  {BLU}·{RST} 已记录 {len(self.seen_ids)} 条消息")
        p(f"  {GRN}· 开始监听...{RST}")
        p()

        self.running = True
        with self.state.lock:
            self.state.running = True
            self.state.status_text = "监听中..."
        signal.signal(signal.SIGINT, self._on_signal)
        signal.signal(signal.SIGTERM, self._on_signal)

        heartbeat_ts = time.time()

        while self.running:
            # 检查 Web 面板是否请求停止
            with self.state.lock:
                if not self.state.running:
                    self.running = False
                    break

            try:
                data = self.oj.fetch_messages()
                if data is None:
                    p(f"  {YEL}· 连接异常，正在重新登录...{RST}")
                    with self.state.lock:
                        self.state.status_text = "重新登录中..."
                    if self.oj.login():
                        self.oj.my_id = self.oj.fetch_my_id()
                    time.sleep(self.config.poll_interval)
                    continue

                for uid, conv in data.get("messages", {}).items():
                    for msg in conv.get("messages", []):
                        self._process(msg, conv)

                # 更新共享状态
                with self.state.lock:
                    self.state.active_users = self.memory.active_users
                    if self.state.status_text == "重新登录中...":
                        self.state.status_text = "监听中..."

                now = time.time()
                if now - heartbeat_ts > 300:
                    logger.info(
                        f"心跳正常 | 已处理 {len(self.seen_ids)} 条消息 | "
                        f"记忆 {self.memory.active_users} 个用户"
                    )
                    heartbeat_ts = now

            except Exception as e:
                logger.exception("主循环异常")

            time.sleep(self.config.poll_interval)

        with self.state.lock:
            self.state.running = False
            self.state.status_text = "已停止"
        self.oj.close_session()
        p(f"  {YEL}· 机器人已停止{RST}")

    # ── 内部 ──

    def _setup_console(self):
        """Windows 终端 — ANSI 颜色支持"""
        if sys.platform != "win32":
            return
        try:
            import ctypes
            k32 = ctypes.windll.kernel32
            h = k32.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            if k32.GetConsoleMode(h, ctypes.byref(mode)):
                k32.SetConsoleMode(h, mode.value | 0x0004)
        except Exception:
            pass

    def _print_ascii_banner(self):
        """从左到右彩虹色 ASCII 艺术字"""
        ascii_lines = [
            r" _   _             _                ___   _____ ",
            r"| | | |           | |              / _ \ |_   _|",
            r"| |_| | _   _   __| | _ __   ___  / /_\ \  | |  ",
            r"|  _  || | | | / _` || '__| / _ \ |  _  |  | |  ",
            r"| | | || |_| || (_| || |   | (_) || | | | _| |_ ",
            r"\_| |_/ \__, | \__,_||_|    \___/ \_| |_/ \___/ ",
            r"         __/ |                                  ",
            r"        |___/                                   ",
        ]
        rainbow = [RED, YEL, GRN, CYN, BLU, DIM]
        for line in ascii_lines:
            colored = ""
            for i, ch in enumerate(line):
                color = rainbow[i % len(rainbow)]
                colored += f"{color}{ch}"
            p(f"  {colored}{RST}")

    def _print_banner(self):
        self._print_ascii_banner()
        p()
        user_list = ", ".join(str(uid) for uid in self.config.allowed_ids())
        p(f"{DIM}════════════════════════════════════════════════════{RST}")
        p(f"{CYN}  HydroAI · OJ 自动回复机器人{RST}")
        p(f"{DIM}════════════════════════════════════════════════════{RST}")
        p()
        p(f"  {YEL}账号{RST}      {self.config.oj['username']}")
        p(f"  {YEL}AI 模型{RST}   {self.config.ai['model']}")
        p(f"  {YEL}轮询间隔{RST}  {self.config.poll_interval} 秒")
        p(f"  {YEL}白名单{RST}    {user_list}")
        p(f"  {YEL}管理员{RST}    {self.config.admin_id}")
        p(f"  {YEL}记忆轮数{RST}  {self.memory.max_rounds} 轮")
        p(f"  {DIM}Ctrl+C 停止{RST}")
        p()

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
        p(f"  {DIM}──────────────────────────────────────────────{RST}")
        p(f"  {YEL}[{now}]{RST}  {GRN}{sender_name}{RST}(ID:{sender})")

        content = content.strip()
        p(f"    {DIM}发{RST}  {content}")

        result = parse(content, sender, self.config)

        if result.reply is not None:
            reply_text = result.reply
        elif result.status_request:
            reply_text = self._get_status_report()
        else:
            matched = [w for w in self.config.blocked_words if w in content]
            if matched:
                words_str = "、".join(f"「{w}」" for w in matched)
                reply_text = f"消息包含屏蔽词 {words_str}，已忽略"
                p(f"    {YEL}⛔ 触发屏蔽词 {words_str}{RST}")
            else:
                p(f"    {DIM}AI 回复中...{RST}")
                history = self.memory.history(sender)

                # 管理员：追加动作指令提示
                if sender == self.config.admin_id:
                    _sys_extra = {"role": "system", "content": ADMIN_ACTION_PROMPT.strip()}
                    history = [_sys_extra] + history if history else [_sys_extra]

                reply_text = self.ai.ask(content, history=history)

                if reply_text is None:
                    reply_text = "AI 回复失败，请稍后重试"
                else:
                    self.memory.add(sender, "user", content)

                    # 解析并执行 AI 动作指令（仅管理员）
                    if sender == self.config.admin_id:
                        reply_text = execute_actions(reply_text, self.config)

                    for w in self.config.blocked_words:
                        if w in reply_text:
                            reply_text = reply_text.replace(w, "*" * len(w))
                            p(f"    {YEL}⛔ AI输出含屏蔽词，已打码{RST}")
                    self.memory.add(sender, "assistant", reply_text)

        p(f"    {CYN}←{RST}  {reply_text}")

        self._send_reply(sender, reply_text)

        with self.state.lock:
            self.state.messages_processed += 1

        if content == "#申请" and not self.config.is_allowed(sender) and sender != self.config.admin_id:
            self._notify_admin(sender, sender_name)

    def _send_reply(self, to_uid: int, text: str, retries: int = 2):
        """发送回复（失败重试）"""
        for attempt in range(retries + 1):
            ok, resp = self.oj.send_message(to_uid, text)
            if ok:
                p(f"    {GRN}✓  已发送{RST}")
                mdoc = resp.get("mdoc", {})
                if mdoc.get("_id"):
                    self.seen_ids.add(mdoc["_id"])
                return
            logger.warning(f"发送失败，正在重试 ({attempt+1}/{retries})")
            time.sleep(1)
        p(f"    {RED}✗  发送失败（已重试 {retries} 次）{RST}")

    def _notify_admin(self, user_id: int, user_name: str):
        """通知管理员有新申请"""
        msg = (
            f"【申请】用户 {user_name}(ID:{user_id}) 申请加入白名单\n"
            f"输入 #同意申请 {user_id} 批准"
        )
        ok, _ = self.oj.send_message(self.config.admin_id, msg)
        if ok:
            p(f"    {DIM}· 已通知管理员{RST}")

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

        # 运行时间
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

        # DeepSeek 余额
        balance = self._check_deepseek_balance(self.config.ai["api_key"])

        lines = [
            "===== HydroAI 运行状态 =====",
            f"运行时长: {uptime_str}",
            f"已处理消息: {processed} 条",
            f"活跃对话: {active} 个用户",
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
        p(f"\n  {YEL}· 正在停止...{RST}")

    @staticmethod
    def _pause():
        try:
            input()
        except Exception:
            pass
