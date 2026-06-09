"""命令解析模块 — 支持自然语言管理命令"""

import logging
import re

from config import Config

logger = logging.getLogger(__name__)


def mask_api_key(key: str) -> str:
    """打码 API Key，只显示前 3 和后 4 位"""
    if len(key) <= 10:
        return key[:3] + "****"
    return key[:3] + "****" + key[-4:]


class CommandResult:
    """命令解析结果"""

    def __init__(self, reply: str | None = None, save_config: bool = False):
        self.reply = reply
        self.save_config = save_config


# AI 管理员动作指令提示（追加在 system prompt 后面）
ADMIN_ACTION_PROMPT = """
你可以通过动作指令执行管理操作。动作指令放在回复末尾，一行一个：
[ACTION: add_whitelist <用户ID>]  添加用户到白名单
[ACTION: remove_whitelist <用户ID>]  从白名单移除用户
[ACTION: add_blocked <词>]  添加屏蔽词
[ACTION: remove_blocked <词>]  删除屏蔽词
[ACTION: list_whitelist]  查看白名单和屏蔽词
[ACTION: approve <用户ID>]  同意加入申请

例：回复"好的，已添加。\\n[ACTION: add_whitelist 222]"
"""


def execute_actions(text: str, config: Config) -> str:
    """解析并执行 AI 回复中的 [ACTION:xxx] 指令，返回执行结果文本"""
    results = []

    for m in re.finditer(r'\[ACTION:\s*(\w+)\s*(.*?)\s*\]', text):
        cmd = m.group(1).strip()
        arg = m.group(2).strip()
        r = _execute_single(cmd, arg, config)
        results.append(r)

    # 去掉原文本中的 action 标记
    cleaned = re.sub(r'\s*\[ACTION:\s*\w+\s*.*?\]\s*', '\n', text).strip()
    cleaned = re.sub(r'\n{2,}', '\n', cleaned)

    if results:
        result_text = '\n'.join(results)
        if cleaned:
            return f"{cleaned}\n\n---\n{result_text}"
        return result_text
    return cleaned


def _execute_single(cmd: str, arg: str, config: Config) -> str:
    """执行单条动作指令"""
    try:
        if cmd == "add_whitelist":
            uid = int(arg)
            if config.is_allowed(uid):
                return f"用户 {uid} 已在白名单中"
            config.add_user(uid)
            config.save()
            return f"已添加用户 {uid} 到白名单"

        elif cmd == "remove_whitelist":
            uid = int(arg)
            if not config.is_allowed(uid):
                return f"用户 {uid} 不在白名单中"
            if uid == config.admin_id:
                return "不能删除管理员自己"
            config.remove_user(uid)
            config.save()
            return f"已从白名单删除用户 {uid}"

        elif cmd == "add_blocked":
            if not arg:
                return "请输入要屏蔽的词"
            if arg in config.blocked_words:
                return f"屏蔽词「{arg}」已存在"
            config.blocked_words.append(arg)
            config.data["bot"]["blocked_words"] = config.blocked_words
            config.save()
            return f"已添加屏蔽词「{arg}」"

        elif cmd == "remove_blocked":
            if not arg:
                return "请输入要删除的屏蔽词"
            if arg not in config.blocked_words:
                return f"屏蔽词「{arg}」不存在"
            config.blocked_words.remove(arg)
            config.data["bot"]["blocked_words"] = config.blocked_words
            config.save()
            return f"已删除屏蔽词「{arg}」"

        elif cmd == "list_whitelist":
            lines = ["白名单："]
            for u in config.allowed_user_ids:
                uid = u if isinstance(u, int) else u["id"]
                note = "" if isinstance(u, int) else (u.get("note") or "")
                tag = " [管理员]" if uid == config.admin_id else ""
                ns = f" — {note}" if note else ""
                lines.append(f"  {uid}{tag}{ns}")
            if config.blocked_words:
                lines.append(f"屏蔽词：{'、'.join(f'「{w}」' for w in config.blocked_words)}")
            return "\n".join(lines)

        elif cmd == "approve":
            uid = int(arg)
            if uid == config.admin_id:
                return "管理员无需申请"
            if config.is_allowed(uid):
                return f"用户 {uid} 已在白名单中"
            config.add_user(uid)
            config.save()
            return f"已同意申请，用户 {uid} 已加入白名单"

        else:
            return f"未知指令: {cmd}"
    except ValueError:
        return f"参数格式错误: {arg}"
    except Exception as e:
        return f"执行失败: {e}"


def parse(content: str, sender_id: int, config: Config) -> CommandResult:
    """
    解析站内消息：
    - 非白名单 → 仅 #申请
    - 白名单（非管理员）→ 仅 AI
    - 管理员 → 自然语言 / #xxx 命令 → AI
    """
    is_admin = sender_id == config.admin_id
    is_allowed = config.is_allowed(sender_id)
    content = content.strip()

    # ── 非白名单用户：仅 #申请 ──
    if not is_allowed and not is_admin:
        if content == "#申请":
            return CommandResult(reply="申请已提交，请等待管理员审核")
        return CommandResult(reply="您不在白名单中，输入 #申请 提交加入申请")

    # ── 白名单非管理员：仅 AI ──
    if not is_admin:
        return CommandResult(reply=None)

    # ══ 管理员：自然语言命令 + #xxx 命令 ══

    # 自然语言：添加到白名单
    m = re.search(r'(?:把|将)\s*(\d+)\s*(?:添加|加入)\s*(?:到)?\s*白名单', content)
    if m:
        return _add(m.group(1).strip(), config)

    # 自然语言：从白名单移除
    m = re.search(r'(?:把|将)\s*(\d+)\s*从\s*(?:白名单中?)?\s*(?:移除|删除)', content)
    if m:
        return _remove(m.group(1).strip(), config)

    # 自然语言：添加屏蔽词
    m = re.search(r'(?:添加|加入)\s*屏蔽词\s*(.+)', content)
    if m:
        word = m.group(1).strip().rstrip("。，,.;；")
        if word:
            return _add_blocked(word, config)

    # 自然语言：删除屏蔽词
    m = re.search(r'(?:删除|移除)\s*屏蔽词\s*(.+)', content)
    if m:
        word = m.group(1).strip().rstrip("。，,.;；")
        if word:
            return _remove_blocked(word, config)

    # 自然语言：查看白名单 / 列表
    if re.search(r'(?:查看|显示|列出?)\s*(?:一下)?\s*白名单', content):
        return _list(config)

    # 自然语言：同意申请
    m = re.search(r'(?:同意|批准)\s*(?:申请)?\s*(\d+)', content)
    if m:
        return _approve(m.group(1).strip(), config)

    # 自然语言：查看屏蔽词
    if re.search(r'(?:查看|显示|列出?)\s*(?:一下)?\s*屏蔽词', content):
        return _list(config)

    # 保留 #xxx 命令（兼容旧操作习惯）
    if content.startswith("#添加 "):
        return _add(content[4:].strip(), config)
    if content.startswith("#删除 "):
        return _remove(content[4:].strip(), config)
    if content.startswith("#同意申请 "):
        return _approve(content[6:].strip(), config)
    if content.startswith("#设置 "):
        return _set(content[4:].strip(), config)
    if content.startswith("#添加屏蔽词 "):
        return _add_blocked(content[6:].strip(), config)
    if content.startswith("#删除屏蔽词 "):
        return _remove_blocked(content[6:].strip(), config)
    if content in ("#列表", "#list"):
        return _list(config)
    if content in ("#帮助", "#help"):
        return _help()

    # 无匹配 → AI
    return CommandResult(reply=None)


# ══════════════════════════════════════════
#  子命令实现
# ══════════════════════════════════════════

def _help() -> CommandResult:
    return CommandResult(reply="可直接用自然语言管理，例如：\n"
                               "「把222添加到白名单」\n"
                               "「把223从白名单移除」\n"
                               "「添加屏蔽词 XX」\n"
                               "「查看白名单」")


def _add(target: str, config: Config) -> CommandResult:
    try:
        uid = int(target)
    except ValueError:
        return CommandResult(reply="格式错误，请指定用户 ID")
    if config.is_allowed(uid):
        return CommandResult(reply=f"用户 {uid} 已在白名单中")
    config.add_user(uid)
    config.save()
    return CommandResult(reply=f"✅ 已添加用户 {uid} 到白名单", save_config=True)


def _remove(target: str, config: Config) -> CommandResult:
    try:
        uid = int(target)
    except ValueError:
        return CommandResult(reply="格式错误，请指定用户 ID")
    if not config.is_allowed(uid):
        return CommandResult(reply=f"用户 {uid} 不在白名单中")
    if uid == config.admin_id:
        return CommandResult(reply="不能删除管理员自己")
    config.remove_user(uid)
    config.save()
    return CommandResult(reply=f"✅ 已从白名单删除用户 {uid}", save_config=True)


def _list(config: Config) -> CommandResult:
    lines = ["📋 白名单："]
    for u in config.allowed_user_ids:
        uid = u if isinstance(u, int) else u["id"]
        note = "" if isinstance(u, int) else (u.get("note") or "")
        tag = " [管理员]" if uid == config.admin_id else ""
        note_str = f" — {note}" if note else ""
        lines.append(f"  {uid}{tag}{note_str}")
    if config.blocked_words:
        lines.append(f"\n🚫 屏蔽词：{'、'.join(f'「{w}」' for w in config.blocked_words)}")
    if len(lines) == 1:
        lines.append("  (空)")
    return CommandResult(reply="\n".join(lines))


def _approve(target: str, config: Config) -> CommandResult:
    try:
        uid = int(target)
    except ValueError:
        return CommandResult(reply="格式错误，请指定用户 ID")
    if uid == config.admin_id:
        return CommandResult(reply="管理员无需申请")
    if config.is_allowed(uid):
        return CommandResult(reply=f"用户 {uid} 已在白名单中")
    config.add_user(uid)
    config.save()
    return CommandResult(reply=f"✅ 已同意申请，用户 {uid} 已加入白名单", save_config=True)


def _set(args: str, config: Config) -> CommandResult:
    if args.startswith("api "):
        new_key = args[4:].strip()
        if not new_key:
            return CommandResult(reply="请指定 API Key，格式: #设置 api sk-xxx")
        config.ai["api_key"] = new_key
        config.save()
        masked = mask_api_key(new_key)
        return CommandResult(reply=f"API Key 已更新: {masked}", save_config=True)
    return CommandResult(reply="未知设置，可用: #设置 api <key>")


def _add_blocked(word: str, config: Config) -> CommandResult:
    if not word:
        return CommandResult(reply="请输入要屏蔽的词")
    if word in config.blocked_words:
        return CommandResult(reply=f"屏蔽词「{word}」已存在")
    config.blocked_words.append(word)
    config.data["bot"]["blocked_words"] = config.blocked_words
    config.save()
    return CommandResult(reply=f"✅ 已添加屏蔽词「{word}」", save_config=True)


def _remove_blocked(word: str, config: Config) -> CommandResult:
    if not word:
        return CommandResult(reply="请输入要删除的屏蔽词")
    if word not in config.blocked_words:
        return CommandResult(reply=f"屏蔽词「{word}」不存在")
    config.blocked_words.remove(word)
    config.data["bot"]["blocked_words"] = config.blocked_words
    config.save()
    return CommandResult(reply=f"✅ 已删除屏蔽词「{word}」", save_config=True)
