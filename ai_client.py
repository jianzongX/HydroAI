"""AI API 客户端 — 流式生成回复，思考内容写入共享状态供 Web 面板显示"""

import json
import logging
import time

import requests

from config import Config, RST, RED, GRN, DIM

logger = logging.getLogger(__name__)


class AiClient:
    """AI API 客户端 — 支持流式回复、重试，思考内容实时写入 BotState"""

    def __init__(self, config: Config, bot_state=None):
        self.config = config
        self._session = requests.Session()
        self._state = bot_state

    def ask(
        self,
        message: str,
        history: list | None = None,
        max_retries: int = 2,
    ) -> str | None:
        """
        调用 AI 生成回复（流式）
        思考过程实时写入 bot_state.thinking_content
        """
        for attempt in range(max_retries + 1):
            result = self._try_ask(message, history)
            if result is not None:
                return result
            if attempt < max_retries:
                wait = 2 ** attempt
                logger.warning(f"AI 请求失败，{wait}秒后重试 ({attempt+1}/{max_retries})")
                time.sleep(wait)
        return None

    def _try_ask(self, message: str, history: list | None) -> str | None:
        """单次 AI 请求"""
        # 清空上次思考内容
        if self._state:
            self._state.clear_thinking()

        try:
            messages = [{"role": "system", "content": self.config.ai_system_prompt}]
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": message})

            resp = self._session.post(
                self.config.ai["api_url"],
                json={
                    "model": self.config.ai["model"],
                    "messages": messages,
                    "max_tokens": self.config.ai.get("max_tokens", 4096),
                    "temperature": self.config.ai.get("temperature", 0.7),
                    "stream": True,
                },
                headers={
                    "Authorization": f"Bearer {self.config.ai['api_key']}",
                    "Content-Type": "application/json",
                },
                timeout=self.config.ai.get("timeout", 120),
                stream=True,
            )

            if resp.status_code != 200:
                print(f"    {RED}[错误]{RST} AI API: {resp.status_code}: {resp.text[:200]}", flush=True)
                return None

            content = ""
            usage_info = None

            for raw_line in resp.iter_lines():
                if not raw_line:
                    continue
                line = raw_line.decode("utf-8").strip()
                if line == "data: [DONE]":
                    break
                if not line.startswith("data: "):
                    continue

                try:
                    chunk = json.loads(line[6:])
                except json.JSONDecodeError:
                    continue

                if "usage" in chunk and chunk["usage"]:
                    usage_info = chunk["usage"]

                choices = chunk.get("choices", [])
                if not choices:
                    continue

                delta = choices[0].get("delta", {})

                # 推理内容 → 写入共享状态（供 Web 面板实时显示）
                rc = delta.get("reasoning_content", "")
                if rc and self._state:
                    self._state.set_thinking(
                        (self._state.snapshot()["thinking_content"] or "") + rc
                    )

                # 实际回复内容
                c = delta.get("content", "")
                if c:
                    content += c

            content = content.strip()
            if not content:
                content = "(AI 返回了空回复)"

            if usage_info:
                total = usage_info.get("total_tokens", 0)
                content += f" [消耗 {total} tokens]"
                print(f"    {DIM}[消耗 {total} tokens]{RST}", flush=True)

            return content

        except requests.exceptions.Timeout:
            print(f"    {RED}[错误]{RST} AI 请求超时", flush=True)
            return None
        except requests.exceptions.ConnectionError:
            print(f"    {RED}[错误]{RST} AI 网络连接失败", flush=True)
            return None
        except Exception as e:
            print(f"    {RED}[错误]{RST} AI 请求异常: {e}", flush=True)
            logger.exception("AI 请求异常详情")
            return None
