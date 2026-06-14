"""
Web 管理面板（可作为线程集成到 Bot 中运行）
"""

import json
import os
import re
import sys
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

SETTINGS_PATH = os.path.join(BASE, "settings.json")
HTML_PATH = os.path.join(BASE, "index.html")
PORT = 8080

MAX_LOG = 200  # 保留最近 200 行控制台输出


# ========== 控制台输出捕获 ==========

class ConsoleBuffer:
    """捕获 print / stdout 输出，保留最近 N 行"""

    def __init__(self, max_lines: int = MAX_LOG):
        self.max_lines = max_lines
        self.buffer: list[str] = []
        self.lock = threading.Lock()
        self._real_stdout = None

    def write(self, text: str):
        with self.lock:
            self.buffer.append(text)
            if len(self.buffer) > self.max_lines * 2:
                self.buffer = self.buffer[-self.max_lines:]
        # 同时输出到真正的终端
        if self._real_stdout:
            try:
                self._real_stdout.write(text)
                self._real_stdout.flush()
            except Exception:
                pass

    def flush(self):
        if self._real_stdout:
            try:
                self._real_stdout.flush()
            except Exception:
                pass

    def get_lines(self, n: int = 100) -> list[str]:
        with self.lock:
            full = "".join(self.buffer)
            lines = full.splitlines(keepends=True)
            flat = []
            for l in lines:
                flat.extend(l.split("\n"))
            # 去掉 ANSI 转义码 + 空行
            import re as _re
            flat = [_re.sub(r"\033\[[0-9;]*m", "", x).rstrip("\r") for x in flat if x.strip()]
            if len(flat) > n:
                flat = flat[-n:]
            return flat

    def install(self):
        """替换 sys.stdout 为缓冲区"""
        self._real_stdout = sys.stdout
        sys.stdout = self

    def uninstall(self):
        """恢复"""
        if self._real_stdout:
            sys.stdout = self._real_stdout
            self._real_stdout = None


# 全局单例（由 main.py 在日志初始化前调用 install）
console = ConsoleBuffer()


# ========== 共享状态 ==========

class BotState:
    def __init__(self):
        self.lock = threading.Lock()
        self.running = False
        self.status_text = "启动中..."
        self.messages_processed = 0
        self.active_users = 0
        self.started_at = datetime.now().isoformat()
        self.thinking_content = ""
        self.start_event = threading.Event()

    def snapshot(self) -> dict:
        with self.lock:
            return {
                "running": self.running,
                "status_text": self.status_text,
                "messages_processed": self.messages_processed,
                "active_users": self.active_users,
                "started_at": self.started_at,
                "thinking_content": self.thinking_content,
            }

    def set_thinking(self, text: str):
        with self.lock:
            self.thinking_content = text

    def clear_thinking(self):
        with self.lock:
            self.thinking_content = ""

    def request_start(self):
        self.start_event.set()


# ========== Config 辅助 ==========

def load_config() -> dict:
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(data: dict) -> bool:
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception:
        return False


def load_html() -> str:
    """从 index.html 文件读取页面，不存在时返回内嵌备用页面"""
    try:
        with open(HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "<!DOCTYPE html><html><head><meta charset='utf-8'><title>HydroAI</title></head><body><h1>HydroAI 管理面板</h1><p>页面文件 index.html 未找到。</p></body></html>"


# ========== Handler 工厂 ==========

def _make_handler(bot_state: BotState | None):

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        # ── GET ──
        def do_GET(self):
            path = urlparse(self.path).path

            if path == "/":
                self._html(load_html())
            elif path == "/api/config":
                self._json(self._read_config())
            elif path == "/api/status":
                self._json(self._get_status())
            elif path.startswith("/api/log"):
                qs = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
                lines = int(qs.get("lines", 100))
                self._json({"lines": self._read_log(lines)})
            else:
                self._json({"error": "Not found"}, 404)

        # ── POST ──
        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = {}

            path = urlparse(self.path).path
            if path == "/api/config":
                self._save_config(data)
            elif path == "/api/bot/start":
                self._bot_start()
            elif path == "/api/bot/stop":
                self._bot_stop()
            else:
                self._json({"error": "Not found"}, 404)

        # ═══════════════ 工具方法 ═══════════════

        def _html(self, content: str):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

        def _json(self, obj: dict, status=200):
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8"))

        def _read_config(self) -> dict:
            cfg = load_config()
            key = cfg.get("ai", {}).get("api_key", "")
            cfg["ai"]["api_key_masked"] = key[:3] + "****" + key[-4:] if key and len(key) > 8 else "****"
            cfg["ai"]["api_key"] = ""
            return cfg

        def _save_config(self, updates: dict):
            cfg = load_config()
            try:
                for k, v in updates.items():
                    if k in cfg and isinstance(cfg[k], dict) and isinstance(v, dict):
                        cfg[k].update(v)
                    else:
                        cfg[k] = v
                if "ai" in updates and "api_key" in updates.get("ai", {}):
                    nk = updates["ai"]["api_key"].strip()
                    if nk and not re.match(r'^sk-\w{3}\*{4}', nk):
                        cfg["ai"]["api_key"] = nk
                ok = save_config(cfg)
                self._json({"ok": ok, "message": "配置已保存" if ok else "保存失败"})
            except Exception as e:
                self._json({"ok": False, "message": str(e)}, 500)

        def _get_status(self) -> dict:
            cfg = load_config()
            state = bot_state.snapshot() if bot_state else {}
            return {
                "bot_running": bot_state.running if bot_state else False,
                "whitelist_count": len(cfg.get("bot", {}).get("allowed_user_ids", [])),
                "blocked_words_count": len(cfg.get("bot", {}).get("blocked_words", [])),
                "admin_id": cfg.get("bot", {}).get("admin_id", ""),
                "messages_processed": state.get("messages_processed", 0),
                "active_users": state.get("active_users", 0),
                "status_text": state.get("status_text", ""),
                "thinking_content": state.get("thinking_content", ""),
                "log_count": len(console.get_lines(9999)),
            }

        def _read_log(self, n: int = 100) -> list:
            return console.get_lines(n)

        def _log_line_count(self) -> int:
            if not os.path.exists(LOG_PATH):
                return 0
            try:
                with open(LOG_PATH, "r", encoding="utf-8") as f:
                    return sum(1 for _ in f)
            except Exception:
                return 0

        def _bot_start(self):
            if bot_state:
                bot_state.request_start()
                self._json({"ok": True, "message": "正在启动 Bot..."})
            else:
                self._json({"ok": False, "message": "Bot 状态不可用"})

        def _bot_stop(self):
            if bot_state:
                with bot_state.lock:
                    bot_state.running = False
                self._json({"ok": True, "message": "正在停止 Bot..."})
            else:
                self._json({"ok": False, "message": "Bot 状态不可用"})

    return Handler


# ========== 启动函数 ==========

def start(host="0.0.0.0", port=PORT, bot_state=None) -> HTTPServer:
    handler = _make_handler(bot_state)
    server = HTTPServer((host, port), handler)
    print(f"  \033[94m·\033[0m 管理面板: \033[92mhttp://localhost:{port}\033[0m")
    print(f"  \033[90m· 无密码保护，所有功能直接可用\033[0m")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
    return server


def start_thread(host="0.0.0.0", port=PORT, bot_state=None) -> tuple[threading.Thread, HTTPServer]:
    handler = _make_handler(bot_state)
    server = HTTPServer((host, port), handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    print(f"  \033[94m·\033[0m 管理面板: \033[92mhttp://localhost:{port}\033[0m")
    print(f"  \033[90m· 无密码保护，所有功能直接可用\033[0m")
    return t, server


if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            import ctypes
            k32 = ctypes.windll.kernel32
            h = k32.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            if k32.GetConsoleMode(h, ctypes.byref(mode)):
                k32.SetConsoleMode(h, mode.value | 0x0004)
        except Exception:
            pass
    print(f"  \033[94m·\033[0m 管理面板: \033[92mhttp://localhost:{PORT}\033[0m")
    print(f"  \033[90m· 无密码保护，所有功能直接可用\033[0m")
    start(bot_state=None)
