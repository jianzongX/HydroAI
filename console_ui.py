"""
控制台 UI 模块 — 统一管理所有终端输出格式
"""

import sys
from datetime import datetime as _datetime

# ── ANSI 颜色常量 ──
RST = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[90m"
RED = "\033[91m"
GRN = "\033[92m"
YEL = "\033[93m"
BLU = "\033[94m"
MAG = "\033[95m"
CYN = "\033[96m"


def _now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def _p(*args, **kwargs):
    """print + 强制刷新"""
    kwargs["flush"] = True
    print(*args, **kwargs)


class Console:
    """控制台输出统一接口"""

    # ── 系统级消息 ──

    @staticmethod
    def info(msg: str):
        """信息 [时间] msg"""
        _p(f"  {BLU}·{RST} {msg}")

    @staticmethod
    def ok(msg: str):
        """成功 """
        _p(f"  {GRN}✔ {RST}{msg}")

    @staticmethod
    def warn(msg: str):
        """警告 """
        _p(f"  {YEL}⚠ {RST}{msg}")

    @staticmethod
    def error(msg: str):
        """错误 """
        _p(f"  {RED}✘ {RST}{msg}")

    @staticmethod
    def dim(msg: str):
        """灰色辅助信息"""
        _p(f"  {DIM}{msg}{RST}")

    @staticmethod
    def plain(msg: str = ""):
        """无前缀纯文本"""
        _p(f"  {msg}")

    @staticmethod
    def divider(style: str = "light"):
        """分隔线"""
        if style == "heavy":
            _p(f"  {DIM}{'═' * 50}{RST}")
        else:
            _p(f"  {DIM}{'─' * 50}{RST}")

    @staticmethod
    def blank():
        """空行"""
        _p()

    # ── 消息收发 ──

    @staticmethod
    def msg_in(time: str, sender_name: str, sender_id: int, content: str):
        """收到消息"""
        _p(f"  {DIM}┌─ [{time}]{RST} {GRN}{sender_name}{RST} (ID:{sender_id})")
        # 内容换行处理
        for line in content.split("\n"):
            _p(f"  {DIM}│{RST}  {line}")

    @staticmethod
    def msg_out(content: str, status: str = ""):
        """发出回复"""
        for i, line in enumerate(content.split("\n")):
            prefix = f"  {DIM}└─{RST}" if i == 0 else f"  {DIM}  {RST}"
            _p(f"{prefix} {CYN}→{RST}  {line}")
        if status:
            _p(f"       {DIM}{status}{RST}")

    @staticmethod
    def think_start():
        """AI 思考中"""
        _p(f"  {DIM}  ↻ AI 回复中...{RST}")

    @staticmethod
    def think_done(tokens: int = 0):
        """AI 回复完成"""
        if tokens:
            _p(f"  {DIM}  ✔ AI 回复完成 [{tokens} tokens]{RST}")
        else:
            _p(f"  {DIM}  ✔ AI 回复完成{RST}")

    @staticmethod
    def blocked(content: str):
        """屏蔽词触发"""
        _p(f"  {YEL}  ⊘ 触发屏蔽词: {content}{RST}")

    @staticmethod
    def sent(ok: bool, retries: int = 0):
        """发送结果"""
        if ok:
            _p(f"  {GRN}  ✔ 已发送{RST}")
        else:
            _p(f"  {RED}  ✘ 发送失败 (重试 {retries} 次){RST}")

    @staticmethod
    def notify(msg: str):
        """系统通知"""
        _p(f"  {DIM}  · {msg}{RST}")

    @staticmethod
    def heartbeat(processed: int, users: int):
        """心跳"""
        _p(f"  {DIM}  ♥ 心跳 | 已处理 {processed} 条 | {users} 个活跃用户{RST}")

    # ── 启动横幅 ──

    @staticmethod
    def banner(config):
        """打印启动信息"""
        banner_lines = [
            r"  _   _             _                ___   _____ ",
            r" | | | |           | |              / _ \ |_   _|",
            r" | |_| | _   _   __| | _ __   ___  / /_\ \  | |  ",
            r" |  _  || | | | / _` || '__| / _ \ |  _  |  | |  ",
            r" | | | || |_| || (_| || |   | (_) || | | | _| |_ ",
            r" \_| |_/ \__, | \__,_||_|    \___/ \_| |_/ \___/ ",
            r"          __/ |                                  ",
            r"         |___/                                   ",
        ]
        rainbow = [RED, YEL, GRN, CYN, BLU, MAG]
        for line in banner_lines:
            colored = ""
            for i, ch in enumerate(line):
                colored += f"{rainbow[i % len(rainbow)]}{ch}"
            _p(f"  {colored}{RST}")
        Console.blank()

        user_list = ", ".join(str(uid) for uid in config.allowed_ids())
        now = _datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Console.divider("heavy")
        Console.plain(f"{CYN}  HydroAI · OJ AI 自动回复机器人{RST}")
        Console.divider("heavy")
        Console.blank()
        Console.info(f"系统时间:  {now}")
        Console.info(f"OJ 账号:   {config.oj['username']}")
        Console.info(f"AI 模型:   {config.ai['model']}")
        Console.info(f"轮询间隔:  {config.poll_interval} 秒")
        Console.info(f"白名单:    {user_list}")
        Console.info(f"管理员:    {config.admin_id}")
        Console.dim("  Ctrl+C 停止")
        Console.blank()

    # ── 辅助 ──

    @staticmethod
    def setup_ansi():
        """启用 Windows 终端 ANSI 支持"""
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
