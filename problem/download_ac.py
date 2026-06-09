"""
下载 2023hyl 所有 AC 题目的源代码
从题库列表 /p 逐页解析 AC 状态，再从 /record/{id} 提取代码
保存为 problem/solutions/{题目id}.cpp
"""

import json
import os
import re
import requests
import time

BASE = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE, "solutions")

OJ_URL = "http://xiaokonglong.net"
USERNAME = "2023hyl"
PASSWORD = "825685"


def login(session):
    r = session.post(f"{OJ_URL}/login",
        json={"uname": USERNAME, "password": PASSWORD, "rememberme": True},
        allow_redirects=False, timeout=15)
    return r.status_code in (200, 302)


def get_ac_from_problem_list(session):
    """逐页爬 /p，收集所有 AC 题目的 pid 和 record_id"""
    ac_list = []  # [(pid, record_id), ...]
    page = 1
    while True:
        r = session.get(f"{OJ_URL}/p", params={"page": page}, timeout=15)
        html = r.text
        count = 0
        for tr in re.finditer(
            r'<tr[^>]*data-pid="(\d+)"[^>]*>.*?</tr>', html, re.DOTALL
        ):
            tr_html = tr.group(0)
            if 'class="record-status--text pass"' in tr_html:
                pid = tr.group(1)
                rm = re.search(r'href="/record/([^"]+)"', tr_html)
                if rm:
                    ac_list.append((int(pid), rm.group(1)))
                    count += 1
        print(f"  第 {page} 页: {count} 个 AC", flush=True)
        if 'class="pager__item next link"' not in html:
            break
        page += 1
        time.sleep(0.3)
    return ac_list


def get_code(session, record_id):
    """从记录 API 获取提交代码"""
    try:
        r = session.get(f"{OJ_URL}/record/{record_id}",
            headers={"Accept": "application/json"}, timeout=10)
        if r.status_code != 200:
            return None
        code = r.json().get("rdoc", {}).get("code", "") or ""
        return code if code else None
    except Exception:
        return None


def main():
    print("=" * 50, flush=True)
    print("Hydro 题解下载器", flush=True)
    print(f"用户: {USERNAME}", flush=True)
    print("=" * 50, flush=True)

    session = requests.Session()
    if not login(session):
        print("登录失败!", flush=True)
        return
    print("登录成功", flush=True)

    # 1. 从题库列表爬 AC 状态
    print("\n扫描题库 AC 状态...", flush=True)
    ac_list = get_ac_from_problem_list(session)
    print(f"共找到 {len(ac_list)} 个 AC 题目\n", flush=True)

    if not ac_list:
        return

    os.makedirs(SAVE_DIR, exist_ok=True)
    pids = [pid for pid, _ in ac_list]

    # 2. 下载代码
    print("下载代码...", flush=True)
    saved = 0
    failed = 0
    for i, (pid, rid) in enumerate(ac_list, 1):
        code = get_code(session, rid)
        if code:
            with open(os.path.join(SAVE_DIR, f"{pid}.cpp"), "w", encoding="utf-8") as f:
                f.write(code)
            saved += 1
        else:
            failed += 1
        print(f"  [{i}/{len(ac_list)}] {pid}.cpp {'OK' if code else 'X'}", flush=True)
        time.sleep(0.2)

    # 3. 保存结果
    with open(os.path.join(SAVE_DIR, "_ac_list.json"), "w", encoding="utf-8") as f:
        json.dump({
            "total": len(ac_list), "saved": saved, "failed": failed,
            "problems": pids,
        }, f, ensure_ascii=False, indent=2)

    print(f"\n完成! 保存: {saved}, 失败: {failed}", flush=True)
    print(f"目录: {SAVE_DIR}", flush=True)


if __name__ == "__main__":
    main()
