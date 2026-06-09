"""
用 2022ssj 账号提交所有已下载的题解代码
C++14 + O2 优化
"""

import os
import re
import requests
import time

BASE = os.path.dirname(os.path.abspath(__file__))
SOLUTIONS_DIR = os.path.join(BASE, "solutions")

OJ_URL = "http://xiaokonglong.net"
USERNAME = "2022ssj"
PASSWORD = "deepseek"
LANG = "cc.cc14o2"


def login(session):
    r = session.post(f"{OJ_URL}/login",
        json={"uname": USERNAME, "password": PASSWORD, "rememberme": True},
        allow_redirects=False, timeout=15)
    return r.status_code in (200, 302)


def submit_code(session, pid, code):
    """提交代码，返回 (成功, 记录ID)"""
    try:
        r = session.post(f"{OJ_URL}/p/{pid}/submit",
            data={"lang": LANG, "code": code},
            headers={"Accept": "application/json"}, timeout=15)
        if r.status_code == 200:
            result = r.json()
            rid = result.get("rid", "")
            return True, rid
        return False, str(r.status_code)
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 50, flush=True)
    print("Hydro 题解批量提交器", flush=True)
    print(f"账号: {USERNAME}", flush=True)
    print(f"语言: {LANG}", flush=True)
    print("=" * 50, flush=True)

    session = requests.Session()
    if not login(session):
        print("登录失败!", flush=True)
        return
    print("登录成功\n", flush=True)

    # 读取所有 .cpp 文件
    files = []
    for fname in sorted(os.listdir(SOLUTIONS_DIR)):
        if not fname.endswith(".cpp"):
            continue
        pid = fname.replace(".cpp", "")
        if not pid.isdigit():
            continue
        fpath = os.path.join(SOLUTIONS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            code = f.read()
        files.append((int(pid), code))

    print(f"共 {len(files)} 个题解待提交\n", flush=True)

    success = 0
    failed = 0
    for i, (pid, code) in enumerate(files, 1):
        ok, rid = submit_code(session, pid, code)
        status = "OK" if ok else f"X ({rid})"
        print(f"  [{i}/{len(files)}] {pid}.cpp {status}", flush=True)
        if ok:
            success += 1
        else:
            failed += 1
        time.sleep(1)  # 避免请求过快

    print(f"\n完成! 成功: {success}, 失败: {failed}", flush=True)


if __name__ == "__main__":
    main()
