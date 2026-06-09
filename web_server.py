"""
Web 管理面板（可作为线程集成到 Bot 中运行）
"""

import json
import os
import re
import sys
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

SETTINGS_PATH = os.path.join(BASE, "settings.json")
PORT = 8080

MAX_LOG = 200  # 保留最近 200 行控制台输出


# ========== 控制台输出捕获 ==========

class ConsoleBuffer:
    """捕获 print / stdout 输出，保留最近 N 行"""

    def __init__(self, max_lines: int = MAX_LOG):
        self.max_lines = max_lines
        self.buffer: list[str] = []
        self.lock = threading.Lock()
        self._real_stdout = None

    def write(self, text: str):
        with self.lock:
            self.buffer.append(text)
            if len(self.buffer) > self.max_lines * 2:
                self.buffer = self.buffer[-self.max_lines:]
        # 同时输出到真正的终端
        if self._real_stdout:
            try:
                self._real_stdout.write(text)
                self._real_stdout.flush()
            except Exception:
                pass

    def flush(self):
        if self._real_stdout:
            try:
                self._real_stdout.flush()
            except Exception:
                pass

    def get_lines(self, n: int = 100) -> list[str]:
        with self.lock:
            full = "".join(self.buffer)
            lines = full.splitlines(keepends=True)
            flat = []
            for l in lines:
                flat.extend(l.split("\n"))
            # 去掉 ANSI 转义码 + 空行
            import re as _re
            flat = [_re.sub(r"\033\[[0-9;]*m", "", x).rstrip("\r") for x in flat if x.strip()]
            if len(flat) > n:
                flat = flat[-n:]
            return flat

    def install(self):
        """替换 sys.stdout 为缓冲区"""
        self._real_stdout = sys.stdout
        sys.stdout = self

    def uninstall(self):
        """恢复"""
        if self._real_stdout:
            sys.stdout = self._real_stdout
            self._real_stdout = None


# 全局单例（由 main.py 在日志初始化前调用 install）
console = ConsoleBuffer()


# ========== 共享状态 ==========

class BotState:
    def __init__(self):
        self.lock = threading.Lock()
        self.running = False
        self.status_text = "启动中..."
        self.messages_processed = 0
        self.active_users = 0
        self.started_at = datetime.now().isoformat()
        self.thinking_content = ""
        self.start_event = threading.Event()

    def snapshot(self) -> dict:
        with self.lock:
            return {
                "running": self.running,
                "status_text": self.status_text,
                "messages_processed": self.messages_processed,
                "active_users": self.active_users,
                "started_at": self.started_at,
                "thinking_content": self.thinking_content,
            }

    def set_thinking(self, text: str):
        with self.lock:
            self.thinking_content = text

    def clear_thinking(self):
        with self.lock:
            self.thinking_content = ""

    def request_start(self):
        self.start_event.set()


# ========== Config 辅助 ==========

def load_config() -> dict:
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(data: dict) -> bool:
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception:
        return False


# ========== Handler 工厂 ==========

def _make_handler(bot_state: BotState | None):

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        # ── GET ──
        def do_GET(self):
            path = urlparse(self.path).path

            if path == "/":
                self._html(DASHBOARD_HTML)
            elif path == "/api/config":
                self._json(self._read_config())
            elif path == "/api/status":
                self._json(self._get_status())
            elif path.startswith("/api/log"):
                qs = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
                lines = int(qs.get("lines", 100))
                self._json({"lines": self._read_log(lines)})
            else:
                self._json({"error": "Not found"}, 404)

        # ── POST ──
        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = {}

            path = urlparse(self.path).path
            if path == "/api/config":
                self._save_config(data)
            elif path == "/api/bot/start":
                self._bot_start()
            elif path == "/api/bot/stop":
                self._bot_stop()
            else:
                self._json({"error": "Not found"}, 404)

        # ═══════════════ 工具方法 ═══════════════

        def _html(self, content: str):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

        def _json(self, obj: dict, status=200):
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8"))

        def _read_config(self) -> dict:
            cfg = load_config()
            key = cfg.get("ai", {}).get("api_key", "")
            cfg["ai"]["api_key_masked"] = key[:3] + "****" + key[-4:] if key and len(key) > 8 else "****"
            cfg["ai"]["api_key"] = ""
            return cfg

        def _save_config(self, updates: dict):
            cfg = load_config()
            try:
                for k, v in updates.items():
                    if k in cfg and isinstance(cfg[k], dict) and isinstance(v, dict):
                        cfg[k].update(v)
                    else:
                        cfg[k] = v
                if "ai" in updates and "api_key" in updates.get("ai", {}):
                    nk = updates["ai"]["api_key"].strip()
                    if nk and not re.match(r'^sk-\w{3}\*{4}', nk):
                        cfg["ai"]["api_key"] = nk
                ok = save_config(cfg)
                self._json({"ok": ok, "message": "配置已保存" if ok else "保存失败"})
            except Exception as e:
                self._json({"ok": False, "message": str(e)}, 500)

        def _get_status(self) -> dict:
            cfg = load_config()
            state = bot_state.snapshot() if bot_state else {}
            return {
                "bot_running": bot_state.running if bot_state else False,
                "whitelist_count": len(cfg.get("bot", {}).get("allowed_user_ids", [])),
                "blocked_words_count": len(cfg.get("bot", {}).get("blocked_words", [])),
                "admin_id": cfg.get("bot", {}).get("admin_id", ""),
                "messages_processed": state.get("messages_processed", 0),
                "active_users": state.get("active_users", 0),
                "status_text": state.get("status_text", ""),
                "thinking_content": state.get("thinking_content", ""),
                "log_count": len(console.get_lines(9999)),
            }

        def _read_log(self, n: int = 100) -> list:
            return console.get_lines(n)

        def _log_line_count(self) -> int:
            if not os.path.exists(LOG_PATH):
                return 0
            try:
                with open(LOG_PATH, "r", encoding="utf-8") as f:
                    return sum(1 for _ in f)
            except Exception:
                return 0

        def _bot_start(self):
            if bot_state:
                bot_state.request_start()
                self._json({"ok": True, "message": "正在启动 Bot..."})
            else:
                self._json({"ok": False, "message": "Bot 状态不可用"})

        def _bot_stop(self):
            if bot_state:
                with bot_state.lock:
                    bot_state.running = False
                self._json({"ok": True, "message": "正在停止 Bot..."})
            else:
                self._json({"ok": False, "message": "Bot 状态不可用"})

    return Handler


# ========== 启动函数 ==========

def start(host="0.0.0.0", port=PORT, bot_state=None) -> HTTPServer:
    handler = _make_handler(bot_state)
    server = HTTPServer((host, port), handler)
    print(f"  \033[94m·\033[0m 管理面板: \033[92mhttp://localhost:{port}\033[0m")
    print(f"  \033[90m· 无密码保护，所有功能直接可用\033[0m")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
    return server


def start_thread(host="0.0.0.0", port=PORT, bot_state=None) -> tuple[threading.Thread, HTTPServer]:
    handler = _make_handler(bot_state)
    server = HTTPServer((host, port), handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    print(f"  \033[94m·\033[0m 管理面板: \033[92mhttp://localhost:{port}\033[0m")
    print(f"  \033[90m· 无密码保护，所有功能直接可用\033[0m")
    return t, server


# ========== 仪表盘 HTML ==========

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HydroAI 管理面板</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif;background:#f6f7f9;color:#1c2127;padding:0}
.nav{background:#1c2127;color:#fff;padding:0 24px;height:48px;display:flex;align-items:center;gap:12px;box-shadow:0 1px 3px rgba(0,0,0,.15)}
.nav h1{font-size:16px;font-weight:600;color:#fff}
.container{max-width:960px;margin:0 auto;padding:20px 16px}
.tabs{display:flex;gap:0;margin-bottom:16px;border-bottom:2px solid #d1d5da}
.tab{padding:8px 20px;cursor:pointer;font-size:14px;color:#5f6b7c;border-bottom:2px solid transparent;margin-bottom:-2px}
.tab:hover{color:#2d72d2}
.tab.active{color:#2d72d2;border-bottom-color:#2d72d2;font-weight:600}
.pane{display:none}.pane.active{display:block}
.card{background:#fff;border:1px solid #d1d5da;border-radius:6px;padding:16px 20px;margin-bottom:12px}
.card h2{font-size:14px;color:#1c2127;margin-bottom:12px;font-weight:600}
.flex{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.badge{display:inline-block;padding:2px 8px;border-radius:3px;font-size:12px;font-weight:600}
.badge.green{background:#e6f7ec;color:#1c6e42}
.badge.red{background:#fce8e8;color:#cb3d3d}
.badge.gray{background:#f0f1f3;color:#5f6b7c}
label{display:block;font-size:13px;color:#5f6b7c;margin-bottom:4px}
input,textarea,select{width:100%;padding:7px 10px;border-radius:4px;border:1px solid #d1d5da;background:#fff;color:#1c2127;font-size:13px;outline:none;font-family:inherit}
input:focus,textarea:focus{border-color:#2d72d2;box-shadow:0 0 0 2px rgba(45,114,210,.15)}
textarea{resize:vertical;min-height:70px;font-size:13px}
.btn{padding:6px 14px;border-radius:4px;border:none;cursor:pointer;font-size:13px;font-weight:500}
.btn.primary{background:#2d72d2;color:#fff}.btn.primary:hover{background:#215db0}
.btn.danger{background:#cb3d3d;color:#fff}.btn.danger:hover{background:#b52d2d}
.btn.outline{background:#fff;color:#5f6b7c;border:1px solid #d1d5da}.btn.outline:hover{background:#f6f7f9}
.btn.green{background:#1c6e42;color:#fff}
.list-item{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #f0f1f3}
.list-item:last-child{border-bottom:none}
.tag{display:inline-block;padding:2px 8px;border-radius:3px;background:#f0f1f3;color:#1c2127;font-size:13px}
.log-box{background:#f6f7f9;border:1px solid #d1d5da;border-radius:4px;padding:10px;font-family:monospace;font-size:12px;line-height:1.6;max-height:400px;overflow-y:auto;white-space:pre-wrap}
.toast{position:fixed;bottom:20px;right:20px;padding:10px 18px;border-radius:6px;background:#1c2127;color:#fff;font-size:13px;transform:translateY(80px);opacity:0;transition:.3s;z-index:999}
.toast.show{transform:translateY(0);opacity:1}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:600px){.grid2{grid-template-columns:1fr}}
.stat-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px}
.stat-card{background:#f6f7f9;border:1px solid #d1d5da;border-radius:4px;padding:10px;text-align:center}
.stat-card .num{font-size:22px;font-weight:700;color:#2d72d2}
.stat-card .label{font-size:11px;color:#5f6b7c;margin-top:2px}
</style>
</head>
<body>
<div class="nav"><h1>HydroAI 管理面板</h1></div>
<div class="container">
<div class="tabs">
  <div class="tab active" data-tab="status">状态</div>
  <div class="tab" data-tab="whitelist">白名单</div>
  <div class="tab" data-tab="blocked">屏蔽词</div>
  <div class="tab" data-tab="ai">AI 设置</div>
  <div class="tab" data-tab="oj">OJ 配置</div>
  <div class="tab" data-tab="log">日志</div>
</div>

<div class="pane active" id="pane-status">
  <div class="card">
    <h2>运行状态</h2>
    <div class="flex" style="margin-bottom:10px;">
      <span class="badge gray" id="sb">检查中...</span>
      <span style="color:#5f6b7c;font-size:13px;" id="st"></span>
    </div>
    <div class="stat-row">
      <div class="stat-card"><div class="num" id="s1">-</div><div class="label">白名单</div></div>
      <div class="stat-card"><div class="num" id="s2">-</div><div class="label">屏蔽词</div></div>
      <div class="stat-card"><div class="num" id="s3">-</div><div class="label">已处理</div></div>
      <div class="stat-card"><div class="num" id="s4">-</div><div class="label">对话</div></div>
      <div class="stat-card"><div class="num" id="s5">-</div><div class="label">管理员</div></div>
    </div>
  </div>
  <div class="card">
    <h2>操作</h2>
    <div class="flex">
      <button class="btn green" id="bs">启动</button>
      <button class="btn danger" id="bp">停止</button>
    </div>
  </div>
  <div class="card" id="tc" style="display:none;">
    <h2>AI 思考</h2>
    <div class="log-box" id="tx" style="max-height:180px;color:#2d72d2;"></div>
  </div>
</div>
<div class="pane" id="pane-whitelist">
  <div class="card"><h2>白名单用户</h2><div id="wl"></div></div>
  <div class="card"><h2>添加用户</h2>
    <div class="flex"><input type="number" id="wi" placeholder="用户 ID" style="max-width:180px;"><button class="btn primary" id="wa">添加</button></div>
  </div>
</div>
<div class="pane" id="pane-blocked">
  <div class="card"><h2>屏蔽词列表</h2><div id="bw"></div></div>
  <div class="card"><h2>添加屏蔽词</h2>
    <div class="flex"><input type="text" id="bi" placeholder="输入要屏蔽的词" style="max-width:220px;"><button class="btn primary" id="ba">添加</button></div>
  </div>
</div>
<div class="pane" id="pane-ai">
  <div class="card"><h2>API 配置</h2>
    <div style="margin-bottom:10px;"><label>API 地址</label><input type="text" id="au"></div>
    <div style="margin-bottom:10px;"><label>API Key</label><input type="password" id="ak" placeholder="留空不变"><small style="color:#8f99a8;"> 当前: <span id="akm"></span></small></div>
    <div style="margin-bottom:10px;"><label>模型</label>
      <select id="am"><option value="deepseek-v4-flash">deepseek-v4-flash</option><option value="deepseek-v4-pro">deepseek-v4-pro</option></select>
    </div>
  </div>
  <div class="card"><h2>回复设置</h2>
    <div style="margin-bottom:10px;"><label>系统提示词</label><textarea id="ap" rows="4"></textarea></div>
    <div class="grid2"><div><label>最大 Token</label><input type="number" id="amt"></div><div><label>温度</label><input type="number" step="0.1" id="at"></div></div>
    <div style="margin-top:10px;"><label>超时 (秒)</label><input type="number" id="ato"></div>
  </div>
  <button class="btn primary" id="as">保存 AI 设置</button>
</div>
<div class="pane" id="pane-oj">
  <div class="card"><h2>OJ 账号</h2>
    <div style="margin-bottom:10px;"><label>服务器地址</label><input type="text" id="ou"></div>
    <div style="margin-bottom:10px;"><label>用户名</label><input type="text" id="oun"></div>
    <div style="margin-bottom:10px;"><label>密码</label><input type="password" id="op" placeholder="留空不变"></div>
    <div style="margin-bottom:10px;"><label>轮询间隔 (秒)</label><input type="number" id="opi"></div>
    <div style="margin-bottom:10px;"><label>管理员 ID</label><input type="number" id="oad"></div>
  </div>
  <button class="btn primary" id="os">保存 OJ 设置</button>
</div>
<div class="pane" id="pane-log">
  <div class="card">
    <div class="flex" style="justify-content:space-between;"><h2>运行日志</h2><button class="btn outline" id="lr">刷新</button></div>
    <div class="log-box" id="lc">加载中...</div>
  </div>
</div>
</div>
<div class="toast" id="toast"></div>
<script>
document.querySelectorAll(".tab").forEach(function(t){t.addEventListener("click",function(){document.querySelectorAll(".tab").forEach(function(x){x.classList.remove("active")});document.querySelectorAll(".pane").forEach(function(x){x.classList.remove("active")});t.classList.add("active");document.getElementById("pane-"+t.dataset.tab).classList.add("active");if(t.dataset.tab==="log")ll()})})
function tt(m,t){var e=document.getElementById("toast");e.textContent=m;e.className="toast "+(t||"success");setTimeout(function(){e.classList.add("show")},10);setTimeout(function(){e.classList.remove("show")},3000)}
async function ap(u,o){return(await fetch(u,Object.assign({headers:{"Content-Type":"application/json"}},o||{}))).json()}
setInterval(async function(){var d=await ap("/api/status"),b=document.getElementById("sb");b.textContent=d.bot_running?" 运行中":" 已停止";b.className="badge "+(d.bot_running?"green":"red");document.getElementById("st").textContent=d.status_text||"";document.getElementById("s1").textContent=d.whitelist_count;document.getElementById("s2").textContent=d.blocked_words_count;document.getElementById("s3").textContent=d.messages_processed;document.getElementById("s4").textContent=d.active_users;document.getElementById("s5").textContent=d.admin_id;document.getElementById("bs").style.display=d.bot_running?"none":"";document.getElementById("bp").style.display=d.bot_running?"":"none";var tc=d.thinking_content||"",tC=document.getElementById("tc"),tX=document.getElementById("tx");if(tc){tC.style.display="";tX.textContent=tc;tX.scrollTop=tX.scrollHeight}else{tC.style.display="none"}},1500)
document.getElementById("bs").addEventListener("click",async function(){tt((await ap("/api/bot/start",{method:"POST",body:"{}"})).message)})
document.getElementById("bp").addEventListener("click",async function(){if(!confirm("确定停止？"))return;tt((await ap("/api/bot/stop",{method:"POST",body:"{}"})).message)})
var cf={};async function lc(){cf=await ap("/api/config");rW();rB();rA();rO()}
async function sc(u,m){var r=await ap("/api/config",{method:"POST",body:JSON.stringify(u)});tt(r.message,r.ok?"success":"error");if(r.ok)lc()}
function h(s){return String(s).replace(/[&<>"]/g,function(m){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]})}
function ui(u){return typeof u==="number"?u:u.id}function un(u){return typeof u==="number"?"":(u.note||"")}
function rW(){var l=document.getElementById("wl"),ra=cf.bot&&cf.bot.allowed_user_ids||[];if(ra.length&&typeof ra[0]==="number")ra=ra.map(function(i){return{id:i,note:""}});if(!ra.length){l.innerHTML='<div style="color:#8f99a8;">(空)</div>';return}var ad=cf.bot&&cf.bot.admin_id;l.innerHTML=ra.map(function(u){var id=ui(u),no=un(u),ia=id==ad;return'<div class="list-item"><div><span class="tag">'+id+'</span>'+(ia?' <span class="badge gray">管理员</span>':'')+(no?' <span style="color:#5f6b7c;font-size:12px;">&mdash; '+h(no)+'</span>':'')+'</div><div class="flex" style="gap:4px;"><button class="btn outline" onclick="eN('+id+')" style="padding:2px 8px;font-size:12px;">备注</button>'+(ia?'':'<button class="btn danger" onclick="rW2('+id+')" style="padding:2px 8px;font-size:12px;">删除</button>')+'</div></div>'}).join("")}
async function eN(id){var ra=cf.bot&&cf.bot.allowed_user_ids||[];var u=ra.find(function(x){return ui(x)===id});if(!u)return;var no=prompt("备注：",un(u));if(no===null)return;if(typeof u==="number")ra=ra.map(function(x){return x===id?{id:id,note:no}:x});else u.note=no;await sc({bot:{allowed_user_ids:ra}})}
async function rW2(id){var ra=cf.bot&&cf.bot.allowed_user_ids||[];ra=ra.filter(function(u){return ui(u)!==id});await sc({bot:{allowed_user_ids:ra}})}
document.getElementById("wa").addEventListener("click",async function(){var i=document.getElementById("wi"),id=parseInt(i.value);if(!id||isNaN(id)){tt("无效 ID","error");return}var ra=cf.bot&&cf.bot.allowed_user_ids||[];if(ra.some(function(u){return ui(u)===id})){tt("已在白名单","error");return}ra.push({id:id,note:""});await sc({bot:{allowed_user_ids:ra}});i.value=""})
function rB(){var l=document.getElementById("bw"),w=cf.bot&&cf.bot.blocked_words||[];if(!w.length){l.innerHTML='<div style="color:#8f99a8;">(空)</div>';return}l.innerHTML=w.map(function(x){return'<div class="list-item"><span>&laquo;'+h(x)+'&raquo;</span><button class="btn danger" onclick="rB2(\''+x.replace(/'/g,"")+'\')" style="padding:2px 8px;font-size:12px;">删除</button></div>'}).join("")}
async function rB2(w){var a=(cf.bot&&cf.bot.blocked_words||[]).filter(function(x){return x!==w});await sc({bot:{blocked_words:a}})}
document.getElementById("ba").addEventListener("click",async function(){var i=document.getElementById("bi"),w=i.value.trim();if(!w){tt("输入词","error");return}var ws=cf.bot&&cf.bot.blocked_words||[];if(ws.indexOf(w)!==-1){tt("已存在","error");return}ws.push(w);await sc({bot:{blocked_words:ws}});i.value=""})
function rA(){var a=cf.ai||{};document.getElementById("au").value=a.api_url||"";document.getElementById("akm").textContent=a.api_key_masked||"未设置";document.getElementById("ak").value="";var m=document.getElementById("am");if(a.model&&[].slice.call(m.options).some(function(o){return o.value===a.model}))m.value=a.model;document.getElementById("ap").value=a.system_prompt||"";document.getElementById("amt").value=a.max_tokens||4096;document.getElementById("at").value=a.temperature||0.7;document.getElementById("ato").value=a.timeout||120}
document.getElementById("as").addEventListener("click",async function(){var u={ai:{api_url:document.getElementById("au").value.trim(),api_key:document.getElementById("ak").value.trim(),model:document.getElementById("am").value,system_prompt:document.getElementById("ap").value.trim(),max_tokens:parseInt(document.getElementById("amt").value)||4096,temperature:parseFloat(document.getElementById("at").value)||0.7,timeout:parseInt(document.getElementById("ato").value)||120}};await sc(u)})
function rO(){var o=cf.oj||{},b=cf.bot||{};document.getElementById("ou").value=o.base_url||"";document.getElementById("oun").value=o.username||"";document.getElementById("op").value="";document.getElementById("opi").value=b.poll_interval_seconds||3;document.getElementById("oad").value=b.admin_id||""}
document.getElementById("os").addEventListener("click",async function(){var pw=document.getElementById("op").value.trim(),u={oj:{base_url:document.getElementById("ou").value.trim(),username:document.getElementById("oun").value.trim()},bot:{poll_interval_seconds:parseInt(document.getElementById("opi").value)||3,admin_id:parseInt(document.getElementById("oad").value)||214}};if(pw)u.oj.password=pw;await sc(u)})
async function ll(){var b=document.getElementById("lc");b.textContent="加载中...";var d=await ap("/api/log");b.textContent=(d.lines||[]).join("\n")||"(空)";b.scrollTop=b.scrollHeight}
document.getElementById("lr").addEventListener("click",ll);lc();
</script>
</body>
</html>"""

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            import ctypes
            k32 = ctypes.windll.kernel32
            h = k32.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            if k32.GetConsoleMode(h, ctypes.byref(mode)):
                k32.SetConsoleMode(h, mode.value | 0x0004)
        except Exception:
            pass
    print(f"  \033[94m·\033[0m 管理面板: \033[92mhttp://localhost:{PORT}\033[0m")
    print(f"  \033[90m· 无密码保护，所有功能直接可用\033[0m")
    start(bot_state=None)
