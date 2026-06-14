"""
命令解析模块 — 纯自然语言管理命令

所有管理操作通过自然语言触发，支持多种表达方式。
匹配逻辑：先尝试精确命令 → 自然语言模式 → 交给 AI
"""

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

    def __init__(self, reply: str | None = None, save_config: bool = False, status_request: bool = False):
        self.reply = reply
        self.save_config = save_config
        self.status_request = status_request


# ── AI 管理员动作指令提示 ──

ADMIN_ACTION_PROMPT = """
你可以通过动作指令执行各种操作。动作指令放在回复末尾，一行一个：

📋 管理操作：
[ACTION: add_whitelist <用户ID>]  添加用户到白名单
[ACTION: remove_whitelist <用户ID>]  从白名单移除用户
[ACTION: add_blocked <词>]  添加屏蔽词
[ACTION: remove_blocked <词>]  删除屏蔽词
[ACTION: list_whitelist]  查看白名单和屏蔽词列表
[ACTION: approve <用户ID>]  同意用户的加入申请
[ACTION: status]  查看机器人运行状态

🌐 查询工具：
[ACTION: search <搜索词>]  联网搜索最新信息
[ACTION: get_time]  获取当前准确时间

当用户问的问题需要最新信息时，使用 search 去搜索。
当用户问现在几点、今天几号时，使用 get_time。
例：用户问"今天比特币价格" → AI搜索 → search 比特币价格 + 把结果回复给用户
例：用户问"现在几点" → AI用 get_time 获取时间后回复
"""


def execute_actions(text: str, config: Config) -> str:
    """解析并执行 AI 回复中的 [ACTION:xxx] 指令，返回执行结果文本"""
    results = []

    for m in re.finditer(r'\[ACTION:\s*(\w+)\s*(.*?)\s*\]', text):
        cmd = m.group(1).strip()
        arg = m.group(2).strip()
        r = _execute_single(cmd, arg, config)
        results.append(r)

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
        if cmd in ("add_whitelist", "add_user"):
            uid = int(arg)
            if config.is_allowed(uid):
                return f"用户 {uid} 已在白名单中"
            config.add_user(uid)
            config.save()
            return f"已添加用户 {uid} 到白名单"

        elif cmd in ("remove_whitelist", "remove_user"):
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

        elif cmd in ("approve", "agree"):
            uid = int(arg)
            if uid == config.admin_id:
                return "管理员无需申请"
            if config.is_allowed(uid):
                return f"用户 {uid} 已在白名单中"
            config.add_user(uid)
            config.save()
            return f"已同意申请，用户 {uid} 已加入白名单"

        elif cmd in ("status", "stats"):
            return "[STATUS_REQUEST]"

        elif cmd == "search":
            if not arg:
                return "请输入搜索词"
            # 返回标记，由 Bot 实际执行搜索
            return f"[SEARCH: {arg}]"

        elif cmd == "get_time":
            from web_tools import get_current_time
            now = get_current_time()
            return f"[当前时间: {now}]"

        else:
            return f"未知指令: {cmd}"
    except ValueError:
        return f"参数格式错误: {arg}"
    except Exception as e:
        return f"执行失败: {e}"


# ══════════════════════════════════════════════════
#  自然语言解析主函数
# ══════════════════════════════════════════════════

def parse(content: str, sender_id: int, config: Config) -> CommandResult:
    """
    解析站内消息：
    - 非白名单 → 仅「#申请」
    - 白名单非管理员 → 全部交 AI
    - 管理员 → 自然语言命令匹配 / AI + 动作指令
    """
    is_admin = sender_id == config.admin_id
    is_allowed = config.is_allowed(sender_id)
    content = content.strip()

    # ── 非白名单用户 ──
    if not is_allowed and not is_admin:
        if content == "#申请":
            return CommandResult(reply="你的申请已提交，请等待管理员审核")
        return CommandResult(reply="你还不在白名单中，输入 #申请 可提交加入申请")

    # ── 白名单非管理员 ──
    if not is_admin:
        return CommandResult(reply=None)

    # ══════════════════════════════════════════════
    #  管理员：自然语言解析
    # ══════════════════════════════════════════════

    reply = _match_admin_command(content, config)
    if reply is not None:
        return reply

    # 无匹配 → 交给 AI
    return CommandResult(reply=None)


def _match_admin_command(text: str, config: Config) -> CommandResult | None:
    """尝试匹配管理员自然语言命令，匹配不到返回 None"""

    # ═══ 白名单操作 ═══

    # 添加用户到白名单
    # "把222加到白名单" "添加用户123" "将456加入白名单" "加上789"
    m = re.search(
        r'(?:把|将|给)\s*(\d+)\s*(?:添加|加入|加到|加进|放进|拉进|加到)'
        r'\s*(?:到)?\s*(?:白名单|名单|列表)',
        text,
    )
    if m:
        return _add(m.group(1).strip(), config)

    m = re.search(
        r'(?:添加|加入|允许|通过)\s*(?:用户)?\s*(\d+)\s*(?:到)?\s*(?:白名单|名单|列表)?',
        text,
    )
    if m:
        return _add(m.group(1).strip(), config)

    m = re.search(r'^(?:添加|加入|允许|通过)\s*(\d+)\s*$', text)
    if m:
        return _add(m.group(1).strip(), config)

    # 从白名单删除
    # "把222从白名单移除" "删除用户123" "踢出222"
    m = re.search(
        r'(?:把|将)\s*(\d+)\s*从\s*(?:白名单|名单|列表)(?:中)?\s*(?:移除|删除|踢出|去掉|移出)',
        text,
    )
    if m:
        return _remove(m.group(1).strip(), config)

    m = re.search(
        r'(?:移除|删除|踢出|去掉|移出)\s*(?:用户)?\s*(\d+)\s*(?:从)?\s*(?:白名单|名单|列表)?',
        text,
    )
    if m:
        return _remove(m.group(1).strip(), config)

    # 同意加入申请
    m = re.search(
        r'(?:同意|批准|通过)\s*(?:申请)?\s*(?:加入)?\s*(\d+)',
        text,
    )
    if m:
        return _approve(m.group(1).strip(), config)

    # 查看白名单
    # "查看白名单" "白名单有哪些人" "列表" "谁在白名单里"
    if re.search(
        r'(?:查看|显示|列出?|看看|查一下|有哪些|都是谁)\s*(?:一下)?\s*'
        r'(?:白名单|名单|列表|用户列表)',
        text,
    ):
        return _list(config)

    if re.search(r'^(?:白名单|名单|列表)\s*$', text):
        return _list(config)

    if re.search(r'谁在.*(?:白名单|名单)', text):
        return _list(config)

    # ═══ 屏蔽词操作 ═══

    # 添加屏蔽词
    m = re.search(
        r'(?:添加|加入|增加|设置)\s*(?:屏蔽词|过滤词|敏感词)\s*(.+)',
        text,
    )
    if m:
        word = m.group(1).strip().rstrip("。，,.;；")
        if word and not re.match(r'^\d+$', word):
            return _add_blocked(word, config)

    m = re.search(
        r'屏蔽\s*(.+)',
        text,
    )
    if m:
        word = m.group(1).strip().rstrip("。，,.;；")
        if word and len(word) <= 10 and not re.match(r'^\d+$', word):
            return _add_blocked(word, config)

    # 删除屏蔽词
    m = re.search(
        r'(?:删除|移除|取消|去掉)\s*(?:屏蔽词|过滤词|敏感词)\s*(.+)',
        text,
    )
    if m:
        word = m.group(1).strip().rstrip("。，,.;；")
        if word:
            return _remove_blocked(word, config)

    # 查看屏蔽词
    if re.search(
        r'(?:查看|显示|列出?|看看|查一下)\s*(?:一下)?\s*(?:屏蔽词|过滤词|敏感词)',
        text,
    ):
        return _list(config)

    if re.search(r'屏蔽词\s*(?:列表|有哪些|都是什么)', text):
        return _list(config)

    # ═══ 状态查询 ═══

    # 查看状态/运行信息
    status_patterns = [
        r'(?:查看|显示|查询|报告|看看|展示)\s*(?:一下)?\s*(?:状态|统计|运行|概况|信息|情况)',
        r'运行状态',
        r'(?:运行|跑了|启动|开机).*(?:多久|多长时间|时间|几个小时)',
        r'(?:处理|回复|回答|收了).*(?:多少|几条|几个|多少条).*(?:消息|信息|问题)',
        r'(?:实时|当前).*(?:状态|统计)',
        r'(?:剩余|还剩|查询|查一下|看看)\s*(?:额度|余额|金额|token|tokens|余量)',
        r'(?:还有|还剩).*(?:多少钱|多少额度)',
        r'状态怎么样',
        r'机器人.*(?:状态|情况)',
        r'搞了多少条',
        r'余额',
    ]
    for pat in status_patterns:
        if re.search(pat, text):
            return CommandResult(reply=None, status_request=True)

    # ═══ 帮助 ═══

    if re.search(r'(?:帮助|help|说明|功能|怎么用|使用说明)', text):
        return _help()

    # ═══ # 快捷命令 ═══

    if text.startswith("#添加 "):
        return _add(text[4:].strip(), config)
    if text.startswith("#删除 "):
        return _remove(text[4:].strip(), config)
    if text.startswith("#同意申请 "):
        return _approve(text[6:].strip(), config)
    if text.startswith("#设置 "):
        return _set(text[4:].strip(), config)
    if text.startswith("#添加屏蔽词 "):
        return _add_blocked(text[6:].strip(), config)
    if text.startswith("#删除屏蔽词 "):
        return _remove_blocked(text[6:].strip(), config)
    if text in ("#列表", "#list"):
        return _list(config)
    if text in ("#状态", "#status"):
        return CommandResult(reply=None, status_request=True)
    if text in ("#帮助", "#help"):
        return _help()
    if text == "#申请":
        return CommandResult(reply="申请已提交，请等待管理员审核")

    return None


# ══════════════════════════════════════════════════
#  子命令实现
# ══════════════════════════════════════════════════

def _help() -> CommandResult:
    return CommandResult(
        reply="🔹 直接用自然语言管理机器人：\n\n"
        "📋 白名单管理：\n"
        "  「把222加入白名单」「删除用户123」「白名单有哪些人」\n\n"
        "🚫 屏蔽词管理：\n"
        "  「添加屏蔽词广告」「删除屏蔽词推广」\n\n"
        "📊 状态查询：\n"
        "  「查看状态」「运行了多久」「余额还剩多少」\n\n"
        "⚡ 其他：\n"
        "  「同意申请 222」「帮助」\n\n"
        "也可以直接说话，AI 会自动帮你处理。"
    )


def _add(target: str, config: Config) -> CommandResult:
    try:
        uid = int(target)
    except ValueError:
        return CommandResult(reply="格式不对哦，请输入用户 ID，例如「把222加入白名单」")
    if config.is_allowed(uid):
        return CommandResult(reply=f"用户 {uid} 已经在白名单里了")
    config.add_user(uid)
    config.save()
    return CommandResult(reply=f"✅ 已添加用户 {uid} 到白名单", save_config=True)


def _remove(target: str, config: Config) -> CommandResult:
    try:
        uid = int(target)
    except ValueError:
        return CommandResult(reply="格式不对哦，请输入用户 ID，例如「把222从白名单移除」")
    if not config.is_allowed(uid):
        return CommandResult(reply=f"用户 {uid} 不在白名单中")
    if uid == config.admin_id:
        return CommandResult(reply="不能删除管理员自己哦")
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
        lines.append("  (还没有人)")
    return CommandResult(reply="\n".join(lines))


def _approve(target: str, config: Config) -> CommandResult:
    try:
        uid = int(target)
    except ValueError:
        return CommandResult(reply="格式不对哦，请输入用户 ID")
    if uid == config.admin_id:
        return CommandResult(reply="管理员不用申请啦")
    if config.is_allowed(uid):
        return CommandResult(reply=f"用户 {uid} 已经在白名单中了")
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
    return CommandResult(reply="未知设置项，可用: #设置 api <key>")


def _add_blocked(word: str, config: Config) -> CommandResult:
    if not word:
        return CommandResult(reply="请输入要屏蔽的词")
    if word in config.blocked_words:
        return CommandResult(reply=f"「{word}」已经在屏蔽词列表里了")
    config.blocked_words.append(word)
    config.data["bot"]["blocked_words"] = config.blocked_words
    config.save()
    return CommandResult(reply=f"✅ 已添加屏蔽词「{word}»", save_config=True)


def _remove_blocked(word: str, config: Config) -> CommandResult:
    if not word:
        return CommandResult(reply="请输入要删除的屏蔽词")
    if word not in config.blocked_words:
        return CommandResult(reply=f"屏蔽词「{word}」不存在")
    config.blocked_words.remove(word)
    config.data["bot"]["blocked_words"] = config.blocked_words
    config.save()
    return CommandResult(reply=f"✅ 已删除屏蔽词「{word}»", save_config=True)
