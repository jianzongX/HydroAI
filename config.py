"""配置管理模块 — 加载 / 保存 settings.json，提供全局设置访问"""

import json
import os
import sys

# ── 终端颜色常量 ──
RST = "\033[0m"
DIM = "\033[90m"
RED = "\033[91m"
GRN = "\033[92m"
YEL = "\033[93m"
BLU = "\033[94m"
CYN = "\033[96m"


def get_config_dir() -> str:
    """获取配置文件目录 — 优先 CWD（.bat 所在目录），回退 exe/脚本目录"""
    if os.path.exists(os.path.join(os.getcwd(), "settings.json")):
        return os.getcwd()
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _uid(u) -> int:
    """统一提取用户 ID（兼容 int 和 dict 格式）"""
    return u if isinstance(u, int) else u["id"]


class Config:
    """配置管理 — 封装 settings.json 的读写"""

    def __init__(self):
        self.config_dir = get_config_dir()
        self.config_path = os.path.join(self.config_dir, "settings.json")
        self.data = self._load()
        # 快捷引用（方便且保留类型提示）
        self.oj = self.data["oj"]
        self.ai = self.data["ai"]
        self.bot = self.data["bot"]

    # ── 属性快捷访问 ──

    @property
    def admin_id(self) -> int:
        return self.bot.get("admin_id", 214)

    @property
    def allowed_user_ids(self) -> list:
        """原始白名单数据（兼容新旧格式）"""
        return self.bot["allowed_user_ids"]

    def allowed_ids(self) -> list[int]:
        """返回纯净的 ID 列表（用于权限检查）"""
        return [_uid(u) for u in self.allowed_user_ids]

    def is_allowed(self, user_id: int) -> bool:
        """检查用户是否在白名单中"""
        return user_id in self.allowed_ids()

    def add_user(self, user_id: int, note: str = ""):
        """添加用户到白名单（自动统一为对象格式）"""
        self._migrate_users()
        # 检查是否已存在
        for u in self.allowed_user_ids:
            if _uid(u) == user_id:
                return
        self.allowed_user_ids.append({"id": user_id, "note": note})

    def remove_user(self, user_id: int) -> bool:
        """从白名单删除用户"""
        self._migrate_users()
        for u in list(self.allowed_user_ids):
            if _uid(u) == user_id:
                self.allowed_user_ids.remove(u)
                return True
        return False

    def user_note(self, user_id: int) -> str:
        """获取用户的备注"""
        for u in self.allowed_user_ids:
            if _uid(u) == user_id:
                if isinstance(u, dict):
                    return u.get("note", "")
        return ""

    def _migrate_users(self):
        """将旧格式 [int, int] 迁移为 [{id, note}, ...]"""
        if self.allowed_user_ids and isinstance(self.allowed_user_ids[0], int):
            self.bot["allowed_user_ids"] = [
                {"id": uid, "note": ""} for uid in self.allowed_user_ids
            ]

    @property
    def poll_interval(self) -> int:
        return self.bot["poll_interval_seconds"]

    @property
    def blocked_words(self) -> list:
        return self.bot.get("blocked_words", [])

    @property
    def ai_system_prompt(self) -> str:
        return self.ai["system_prompt"]

    # ── 持久化 ──

    def save(self) -> bool:
        """将当前配置写回 settings.json"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
                f.flush()
                os.fsync(f.fileno())
            print(f"  {GRN}· 配置已保存{RST}", flush=True)
            return True
        except Exception as e:
            print(f"  {RED}[错误]{RST} 保存配置失败: {e}", flush=True)
            return False

    # ── 内部 ──

    def _load(self) -> dict:
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"  {RED}[错误]{RST} 未找到配置文件: {self.config_path}", flush=True)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"  {RED}[错误]{RST} 配置文件格式错误: {e}", flush=True)
            sys.exit(1)
