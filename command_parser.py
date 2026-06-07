"""命令解析模块 — 解析站内消息中的 #xxx 命令"""

import logging

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
        self.reply = reply          # 回复文本，None 表示不走命令（交给 AI）
        self.save_config = save_config  # 是否需要持久化配置


def parse(content: str, sender_id: int, config: Config) -> CommandResult:
    """
    解析站内消息中的命令

    参数:
        content:   消息文本
        sender_id: 发送者用户 ID
        config:    配置对象

    返回:
        CommandResult — reply=None 表示无匹配命令，交给 AI 回复
    """
    is_admin = sender_id == config.admin_id
    is_allowed = config.is_allowed(sender_id)

    content = content.strip()

    # ── 非白名单用户 ──
    if not is_allowed and not is_admin:
        if content == "#申请":
            # 申请消息由 Bot 自行通知管理员，这里只返回对用户的回复
            return CommandResult(reply="申请已提交，请等待管理员审核")
        return CommandResult(reply="您不在白名单中，输入 #申请 提交加入申请")

    # ── 帮助（所有人可见） ──
    if content in ("#帮助", "#help"):
        return _help(is_admin)

    # ── 以下仅管理员命令 ──
    if not is_admin:
        return CommandResult(reply=None)  # 走 AI

    if content.startswith("#添加 "):
        return _add(content[4:].strip(), config)
    if content.startswith("#删除 "):
        return _remove(content[4:].strip(), config)
    if content == "#列表":
        return _list(config)
    if content.startswith("#同意申请 "):
        return _approve(content[6:].strip(), config)
    if content.startswith("#设置 "):
        return _set(content[4:].strip(), config)
    if content.startswith("#添加屏蔽词 "):
        return _add_blocked(content[6:].strip(), config)
    if content.startswith("#删除屏蔽词 "):
        return _remove_blocked(content[6:].strip(), config)

    # 无匹配 → AI
    return CommandResult(reply=None)


# ══════════════════════════════════════════
#  子命令实现
# ══════════════════════════════════════════

def _help(is_admin: bool) -> CommandResult:
    text = "可用命令:\n#帮助/#help - 查看此帮助\n#申请 - 提交加入白名单申请"
    if is_admin:
        text += (
            "\n#同意申请 <用户ID> - 批准用户加入白名单"
            "\n#添加 <用户ID> - 添加用户到白名单"
            "\n#删除 <用户ID> - 从白名单删除用户"
            "\n#列表 - 查看白名单和屏蔽词"
            "\n#添加屏蔽词 <词> - 添加屏蔽词"
            "\n#删除屏蔽词 <词> - 删除屏蔽词"
            "\n#设置 api <key> - 更新 API Key"
        )
    return CommandResult(reply=text)


def _add(target: str, config: Config) -> CommandResult:
    try:
        uid = int(target)
    except ValueError:
        return CommandResult(reply="格式错误，请使用: #添加 用户ID")

    if config.is_allowed(uid):
        return CommandResult(reply=f"用户 {uid} 已在白名单中")
    config.add_user(uid)
    config.save()
    return CommandResult(reply=f"已添加用户 {uid} 到白名单", save_config=True)


def _remove(target: str, config: Config) -> CommandResult:
    try:
        uid = int(target)
    except ValueError:
        return CommandResult(reply="格式错误，请使用: #删除 用户ID")

    if not config.is_allowed(uid):
        return CommandResult(reply=f"用户 {uid} 不在白名单中")
    if uid == config.admin_id:
        return CommandResult(reply="不能删除管理员自己")
    config.remove_user(uid)
    config.save()
    return CommandResult(reply=f"已从白名单删除用户 {uid}", save_config=True)


def _list(config: Config) -> CommandResult:
    names = ", ".join(str(uid) for uid in config.allowed_ids())
    bws = config.blocked_words
    bw_text = ", ".join(f"「{w}」" for w in bws)
    reply = f"白名单: {names}"
    if bw_text:
        reply += f"\n屏蔽词: {bw_text} ({len(bws)}个)"
    return CommandResult(reply=reply)


def _approve(target: str, config: Config) -> CommandResult:
    try:
        uid = int(target)
    except ValueError:
        return CommandResult(reply="格式错误，请使用: #同意申请 用户ID")

    if uid == config.admin_id:
        return CommandResult(reply="管理员无需申请")
    if config.is_allowed(uid):
        return CommandResult(reply=f"用户 {uid} 已在白名单中")
    config.add_user(uid)
    config.save()
    return CommandResult(reply=f"已同意申请，用户 {uid} 已加入白名单", save_config=True)


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
    return CommandResult(reply=f"已添加屏蔽词「{word}」", save_config=True)


def _remove_blocked(word: str, config: Config) -> CommandResult:
    if not word:
        return CommandResult(reply="请输入要删除的屏蔽词")
    if word not in config.blocked_words:
        return CommandResult(reply=f"屏蔽词「{word}」不存在")
    config.blocked_words.remove(word)
    config.data["bot"]["blocked_words"] = config.blocked_words
    config.save()
    return CommandResult(reply=f"已删除屏蔽词「{word}」", save_config=True)
