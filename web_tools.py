"""
联网工具模块 — 搜索、时间查询等
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# ── 时间查询 ──

def get_current_time() -> str:
    """获取当前时间（北京时间）"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S (北京时间, UTC+8)")


def get_current_date() -> str:
    """获取当前日期"""
    now = datetime.now()
    return now.strftime("%Y年%m月%d日")


# ── 网页搜索 ──

def web_search(query: str, max_results: int = 5) -> str:
    """
    联网搜索，返回简洁的搜索结果文本
    使用 DuckDuckGo 搜索引擎（无需 API Key）
    """
    import urllib.parse
    import requests

    encoded = urllib.parse.quote(query)
    url = f"https://lite.duckduckgo.com/lite/?q={encoded}"

    try:
        resp = requests.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            },
            timeout=15,
        )
        if resp.status_code != 200:
            return f"[搜索失败: HTTP {resp.status_code}]"

        html = resp.text
        results = _parse_duckduckgo_lite(html, max_results)

        if not results:
            # 尝试 DuckDuckGo API
            return _try_duckduckgo_api(query)

        lines = [f"搜索结果: {query}"]
        for i, (title, snippet, link) in enumerate(results, 1):
            lines.append(f"{i}. {title}")
            if snippet:
                lines.append(f"   {snippet[:150]}")
            lines.append(f"   {link}")
        return "\n".join(lines[:12])  # 限制长度

    except requests.exceptions.Timeout:
        return "[搜索超时]"
    except requests.exceptions.ConnectionError:
        return _try_fallback_search(query)
    except Exception as e:
        logger.exception(f"搜索异常")
        return f"[搜索异常: {e}]"


def _parse_duckduckgo_lite(html: str, max_results: int) -> list:
    """解析 DuckDuckGo Lite 版 HTML 结果"""
    results = []
    # 查找结果表格中的链接和描述
    import re
    from urllib.parse import urlparse, urlunparse
    # DuckDuckGo Lite 结果在 <a> 标签中，紧跟着描述
    blocks = re.split(r'<tr>', html)
    seen_urls = set()
    for block in blocks:
        # 提取标题和链接
        m = re.search(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', block)
        if not m:
            continue
        raw_link = m.group(1)
        title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if not title or not raw_link or raw_link.startswith("#"):
            continue

        # 清理链接：确保有协议头
        link = raw_link
        if link.startswith("//"):
            link = "https:" + link
        elif not link.startswith("http"):
            continue  # 跳过非 http 链接

        # 去重
        if link in seen_urls:
            continue
        seen_urls.add(link)

        # 提取描述片段
        snippet = ""
        sm = re.search(r'<td class="result-snippet">(.*?)</td>', block)
        if sm:
            snippet = re.sub(r'<[^>]+>', '', sm.group(1)).strip()

        results.append((title, snippet, link))
        if len(results) >= max_results:
            break
    return results


def _try_duckduckgo_api(query: str) -> str:
    """备选：DuckDuckGo Instant Answer API"""
    import urllib.parse
    import requests

    try:
        encoded = urllib.parse.quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1"
        resp = requests.get(url, headers={"User-Agent": "HydroAI/1.0"}, timeout=10)
        if resp.status_code != 200:
            return f"[搜索失败: HTTP {resp.status_code}]"

        data = resp.json()
        parts = []

        abstract = data.get("AbstractText", "")
        if abstract:
            parts.append(f"摘要: {abstract[:500]}")

        source = data.get("AbstractSource", "")
        src_url = data.get("AbstractURL", "")
        if source and src_url:
            parts.append(f"来源: {source} ({src_url})")

        answer = data.get("Answer", "")
        if answer:
            parts.append(f"回答: {answer}")

        if parts:
            return f"搜索结果: {query}\n---\n" + "\n".join(parts)

        # 相关话题
        related = data.get("RelatedTopics", [])
        if related:
            lines = [f"搜索结果: {query}", "---"]
            for item in related[:5]:
                if isinstance(item, dict):
                    text = item.get("Text", "")
                    url_item = item.get("FirstURL", "")
                    if text:
                        lines.append(f"· {text[:200]}")
            return "\n".join(lines)

        return f"[未找到关于「{query}」的结果]"
    except Exception:
        return "[搜索服务暂不可用]"


def _try_fallback_search(query: str) -> str:
    """如果 DuckDuckGo 不可用（如在中国网络环境），尝试用 Bing"""
    import urllib.parse
    import requests

    try:
        encoded = urllib.parse.quote(f"{query} 2026")
        url = f"https://www.bing.com/search?q={encoded}"
        resp = requests.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36"
                ),
            },
            timeout=15,
        )
        if resp.status_code != 200:
            return "[搜索不可用: 网络受限]"

        import re
        results = []
        # 提取 Bing 搜索结果
        for block in re.split(r'<li class="b_algo">', resp.text):
            m = re.search(r'<a[^>]*href="(https?://[^"]*)"[^>]*>(.*?)</a>', block)
            if not m:
                continue
            link = m.group(1)
            title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
            sm = re.search(r'<p[^>]*>(.*?)</p>', block)
            snippet = re.sub(r'<[^>]+>', '', sm.group(1)).strip() if sm else ""
            results.append((title, snippet, link))
            if len(results) >= 5:
                break

        if results:
            lines = [f"搜索结果: {query}", "---"]
            for i, (t, s, l) in enumerate(results, 1):
                lines.append(f"{i}. {t}")
                if s:
                    lines.append(f"   {s[:200]}")
                lines.append(f"   {l}")
            return "\n".join(lines)

        return "[搜索结果为空]"
    except Exception:
        return "[网络搜索暂时不可用]"
