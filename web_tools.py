"""
工具模块 — 时间查询等
"""

from datetime import datetime


def get_current_time() -> str:
    """获取当前时间（北京时间）"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S (北京时间, UTC+8)")


def get_current_date() -> str:
    """获取当前日期"""
    now = datetime.now()
    return now.strftime("%Y年%m月%d日")
