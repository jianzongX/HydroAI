"""OJ 站内信 API 封装 — 登录、获取消息、发送消息（延迟创建 session）"""

import json
import logging
import time

import requests

from config import Config
from console_ui import RST, RED, GRN, BLU, YEL, DIM

logger = logging.getLogger(__name__)


class OjClient:
    """小恐龙 OJ 站内消息客户端"""

    def __init__(self, config: Config):
        self.config = config
        self.session = None
        self.my_id: int | None = None

    def _ensure_session(self):
        if self.session is None:
            self.session = requests.Session()

    def close_session(self):
        if self.session:
            try:
                self.session.close()
            except Exception:
                pass
        self.session = None

    # ── 登录 ──

    def login(self) -> bool:
        """登录 OJ，返回是否成功"""
        self._ensure_session()
        try:
            resp = self.session.post(
                f"{self.config.oj['base_url']}/login",
                json={
                    "uname": self.config.oj["username"],
                    "password": self.config.oj["password"],
                    "rememberme": True,
                },
                allow_redirects=False,
                timeout=15,
            )
        except requests.exceptions.Timeout:
            print(f"  {RED}[错误]{RST} OJ 登录超时（15秒）", flush=True)
            return False
        except requests.exceptions.ConnectionError:
            print(f"  {RED}[错误]{RST} OJ 网络连接失败", flush=True)
            return False
        if resp.status_code not in (200, 302):
            print(f"  {RED}[错误]{RST} 登录失败: {resp.status_code}", flush=True)
            return False
        print(f"  {BLU}·{RST} OJ 登录成功", flush=True)
        return True

    def ensure_login(self) -> bool:
        """确保已登录，过期则自动重登"""
        if self.my_id:
            return True
        if self.login():
            self.my_id = self.fetch_my_id()
            return self.my_id is not None
        return False

    # ── 消息获取 ──

    def fetch_messages(self) -> dict | None:
        """获取所有消息"""
        self._ensure_session()
        try:
            resp = self.session.get(
                f"{self.config.oj['base_url']}/home/messages",
                headers={"Accept": "application/json"},
                timeout=15,
            )
            if resp.status_code == 200:
                return resp.json()
            logger.warning(f"获取消息返回 {resp.status_code}")
            return None
        except requests.exceptions.ConnectionError:
            logger.warning("获取消息 — 网络连接失败")
            return None
        except Exception as e:
            logger.error(f"获取消息异常: {e}")
            return None

    def fetch_my_id(self) -> int | None:
        """获取当前登录用户 ID"""
        data = self.fetch_messages()
        if not data:
            return None
        user_ctx = data.get("UserContext", {})
        if isinstance(user_ctx, str):
            try:
                user_ctx = json.loads(user_ctx)
            except json.JSONDecodeError:
                return None
        return user_ctx.get("_id")

    # ── 消息发送 ──

    def send_message(self, to_uid: int, content: str) -> tuple[bool, dict]:
        """发送消息，返回 (成功与否, 响应JSON)"""
        self._ensure_session()
        try:
            resp = self.session.post(
                f"{self.config.oj['base_url']}/home/messages",
                data={
                    "operation": "send",
                    "uid": str(to_uid),
                    "content": content,
                },
                headers={"Accept": "application/json"},
                timeout=15,
            )
            if resp.status_code == 200:
                return True, resp.json()
            if resp.status_code in (401, 403):
                logger.warning(f"发送消息 — 会话过期({resp.status_code})")
                self.my_id = None
            return False, {}
        except requests.exceptions.Timeout:
            logger.warning("发送消息超时")
            return False, {}
        except requests.exceptions.ConnectionError:
            logger.warning("发送消息 — 网络连接失败")
            return False, {}
        except Exception as e:
            logger.error(f"发送消息异常: {e}")
            return False, {}
