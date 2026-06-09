"""
小恐龙 OJ · AI 自动回复机器人（集成 Web 管理面板）

功能: 监听站内消息，用 AI 自动回复（流式），Web 面板管理
运行: python main.py          (脚本)
      双击【小恐龙OJ机器人.exe】 (打包版)
停止: Ctrl+C | Web 面板「停止 Bot」
配置: settings.json（与程序同目录）
"""

import logging
import logging.handlers
import os
import sys
import time


def _setup_logging():
    """日志配置 — 保留最近 100 行"""
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    log_path = os.path.join(base, "bot.log")

    # RotatingFileHandler：约 100 行后轮转
    file_handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=10240, backupCount=1, encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter("%(message)s"))

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(file_handler)
    root.addHandler(console_handler)


def _enable_ansi():
    """启用 Windows 终端 ANSI 转义序列支持"""
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


def main():
    # 先安装控制台缓冲区，再初始化日志（让日志也走缓冲区）
    try:
        from web_server import console
        console.install()
    except Exception:
        pass

    _setup_logging()
    _enable_ansi()

    from config import Config
    from bot import Bot
    from web_server import BotState, start_thread

    config = Config()
    bot_state = BotState()
    bot_state.start_event.set()  # 首次自动启动

    # 后台启动 Web 管理面板
    try:
        start_thread(bot_state=bot_state)
    except Exception as e:
        logging.getLogger(__name__).warning(f"Web 面板启动失败: {e}")

    # ── 主循环（支持重启） ──
    while True:
        # 等待启动信号（首次自动触发）
        bot_state.start_event.wait()
        bot_state.start_event.clear()

        with bot_state.lock:
            bot_state.running = True
            bot_state.status_text = "启动中..."
            bot_state.messages_processed = 0
            bot_state.active_users = 0

        bot = Bot(config, bot_state=bot_state)
        bot.run()

        with bot_state.lock:
            bot_state.running = False
            bot_state.status_text = "已停止"

        # 短暂休眠防止 CPU 空转
        time.sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  \033[93m· 程序已退出\033[0m", flush=True)
    except Exception as e:
        import traceback
        print(f"\n  \033[91m[错误]\033[0m 程序异常崩溃!", flush=True)
        print(f"  \033[91m[错误]\033[0m {e}", flush=True)
        traceback.print_exc()
        print(f"\n  \033[90m按 Enter 退出...\033[0m", flush=True)
        try:
            input()
        except Exception:
            pass
        sys.exit(1)
