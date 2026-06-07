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
LOG_PATH = os.path.join(BASE, "bot.log")
PORT = 8080


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


def _check_pass(username: str, password: str) -> dict:
    """
    检查管理账号密码
    返回: {"ok": bool, "is_new": bool}
    - is_new=True 表示首次设置，已保存
    """
    cfg = load_config()
    stored_user = cfg.get("bot", {}).get("admin_username", "") or ""
    stored_pass = cfg.get("bot", {}).get("admin_password", "") or ""

    # 首次使用：没有存储的凭证 → 保存并解锁
    if not stored_user and not stored_pass and username and password:
        cfg.setdefault("bot", {})
        cfg["bot"]["admin_username"] = username
        cfg["bot"]["admin_password"] = password
        save_config(cfg)
        return {"ok": True, "is_new": True}

    return {"ok": username == stored_user and password == stored_pass, "is_new": False}


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
            elif path == "/api/check_pass":
                qs = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
                self._json(_check_pass(qs.get("user", ""), qs.get("pwd", "")))
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
                "log_count": self._log_line_count(),
                "has_password": bool(cfg.get("bot", {}).get("admin_password", "")),
            }

        def _read_log(self, n: int = 100) -> list:
            if not os.path.exists(LOG_PATH):
                return ["(暂无日志)"]
            try:
                with open(LOG_PATH, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                return [l.rstrip("\n\r") for l in lines[-n:]]
            except Exception:
                return ["(读取日志失败)"]

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
    print(f"  \033[90m· 首次使用请在页面设置管理密码\033[0m")
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
    print(f"  \033[90m· 首次使用请在页面设置管理密码\033[0m")
    return t, server


# ========== 仪表盘 HTML ==========

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>小恐龙OJ · 管理面板</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, "Segoe UI", "Noto Sans SC", sans-serif; background: #0f0f12; color: #d4d4d8; padding: 20px; }
  h1 { font-size: 22px; color: #a78bfa; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
  h1 small { font-size: 14px; color: #71717a; font-weight: normal; }
  .lock-bar { background: #18181b; border: 1px solid #27272a; border-radius: 10px; padding: 12px 20px; margin-bottom: 16px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
  .lock-bar .label { font-size: 13px; color: #a1a1aa; }
  .lock-bar input { padding: 6px 12px; border-radius: 6px; border: 1px solid #3f3f46; background: #0f0f12; color: #e4e4e7; font-size: 14px; outline: none; width: 200px; }
  .lock-bar input:focus { border-color: #a78bfa; }
  .tabs { display: flex; gap: 4px; margin-bottom: 20px; flex-wrap: wrap; }
  .tab { padding: 8px 18px; border-radius: 8px 8px 0 0; cursor: pointer; background: #18181b; color: #a1a1aa; border: 1px solid #27272a; border-bottom: none; font-size: 14px; }
  .tab:hover { background: #27272a; }
  .tab.active { background: #27272a; color: white; border-color: #a78bfa; }
  .pane { display: none; }
  .pane.active { display: block; }
  .card { background: #18181b; border: 1px solid #27272a; border-radius: 10px; padding: 16px 20px; margin-bottom: 16px; }
  .card h2 { font-size: 15px; color: #e4e4e7; margin-bottom: 12px; }
  .flex { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
  .badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }
  .badge.green { background: #065f46; color: #6ee7b7; }
  .badge.red { background: #7f1d1d; color: #fca5a5; }
  .badge.gray { background: #27272a; color: #a1a1aa; }
  label { display: block; font-size: 13px; color: #a1a1aa; margin-bottom: 4px; }
  input, textarea, select { width: 100%; padding: 8px 12px; border-radius: 6px; border: 1px solid #3f3f46; background: #0f0f12; color: #e4e4e7; font-size: 14px; outline: none; font-family: inherit; }
  input:focus, textarea:focus { border-color: #a78bfa; }
  textarea { resize: vertical; min-height: 80px; font-size: 13px; }
  .btn { padding: 7px 16px; border-radius: 6px; border: none; cursor: pointer; font-size: 13px; font-weight: 500; }
  .btn.primary { background: #7c3aed; color: white; }
  .btn.primary:hover { background: #6d28d9; }
  .btn.danger { background: #dc2626; color: white; }
  .btn.danger:hover { background: #b91c1c; }
  .btn.outline { background: transparent; color: #a1a1aa; border: 1px solid #3f3f46; }
  .btn.outline:hover { background: #27272a; color: white; }
  .btn.green { background: #059669; color: white; }
  .btn.green:hover { background: #047857; }
  .list-item { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #27272a; }
  .list-item:last-child { border-bottom: none; }
  .tag { display: inline-block; padding: 2px 10px; border-radius: 4px; background: #27272a; color: #d4d4d8; font-size: 13px; }
  .log-box { background: #09090b; border: 1px solid #27272a; border-radius: 6px; padding: 12px; font-family: monospace; font-size: 12px; line-height: 1.6; max-height: 400px; overflow-y: auto; white-space: pre-wrap; word-break: break-all; }
  .toast { position: fixed; bottom: 24px; right: 24px; padding: 12px 20px; border-radius: 8px; background: #18181b; border: 1px solid #3f3f46; color: #e4e4e7; font-size: 14px; transform: translateY(100px); opacity: 0; transition: .3s; z-index: 999; }
  .toast.show { transform: translateY(0); opacity: 1; }
  .toast.success { border-color: #059669; }
  .toast.error { border-color: #dc2626; }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  @media (max-width: 600px) { .grid2 { grid-template-columns: 1fr; } }
  .stat-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; }
  .stat-card { background: #0f0f12; border: 1px solid #27272a; border-radius: 8px; padding: 12px; text-align: center; }
  .stat-card .num { font-size: 24px; font-weight: 700; color: #a78bfa; }
  .stat-card .label { font-size: 12px; color: #71717a; margin-top: 4px; }
</style>
</head>
<body>

<h1>🦕 小恐龙OJ · 管理面板 <small>集成版</small></h1>

<div class="lock-bar">
  <span class="label" id="lock-label">🔒 已锁定</span>
  <input type="text" id="user-input" placeholder="管理账号" style="width:120px;" onkeydown="if(event.key==='Enter') document.getElementById('pwd-input').focus()">
  <input type="password" id="pwd-input" placeholder="管理密码" style="width:140px;" onkeydown="if(event.key==='Enter') unlock()">
  <button class="btn primary" id="unlock-btn" onclick="unlock()">解锁</button>
</div>

<div class="tabs">
  <div class="tab active" data-tab="status">📊 状态</div>
  <div class="tab" data-tab="whitelist">👥 白名单</div>
  <div class="tab" data-tab="blocked">🚫 屏蔽词</div>
  <div class="tab" data-tab="ai">🤖 AI 设置</div>
  <div class="tab" data-tab="oj">🔌 OJ 配置</div>
  <div class="tab" data-tab="log">📋 日志</div>
</div>

<div class="pane active" id="pane-status">
  <div class="card">
    <h2>运行状态</h2>
    <div class="flex" style="margin-bottom:12px;">
      <span id="status-badge" class="badge gray">检查中...</span>
      <span id="status-text" style="color:#71717a;font-size:13px;"></span>
    </div>
    <div class="stat-row">
      <div class="stat-card"><div class="num" id="s-whitelist">-</div><div class="label">白名单</div></div>
      <div class="stat-card"><div class="num" id="s-blocked">-</div><div class="label">屏蔽词</div></div>
      <div class="stat-card"><div class="num" id="s-msgs">-</div><div class="label">已处理消息</div></div>
      <div class="stat-card"><div class="num" id="s-users">-</div><div class="label">活跃对话</div></div>
      <div class="stat-card"><div class="num" id="s-admin">-</div><div class="label">管理员</div></div>
    </div>
  </div>
  <div class="card">
    <h2>操作</h2>
    <div class="flex">
      <button class="btn green" id="btn-start">▶ 启动 Bot</button>
      <button class="btn danger" id="btn-stop">⏹ 停止 Bot</button>
    </div>
  </div>
  <div class="card" id="thinking-card" style="display:none;">
    <h2>🧠 AI 思考过程</h2>
    <div class="log-box" id="thinking-content" style="max-height:200px;color:#a78bfa;"></div>
  </div>
</div>

<div class="pane" id="pane-whitelist">
  <div class="card"><h2>白名单用户</h2><div id="whitelist-list"></div></div>
  <div class="card">
    <h2>添加用户</h2>
    <div class="flex">
      <input type="number" id="wl-input" placeholder="用户 ID" style="max-width:200px;">
      <button class="btn primary" id="wl-add-btn">添加</button>
    </div>
  </div>
</div>

<div class="pane" id="pane-blocked">
  <div class="card"><h2>屏蔽词列表</h2><div id="blocked-list"></div></div>
  <div class="card">
    <h2>添加屏蔽词</h2>
    <div class="flex">
      <input type="text" id="bw-input" placeholder="输入要屏蔽的词" style="max-width:250px;">
      <button class="btn primary" id="bw-add-btn">添加</button>
    </div>
  </div>
</div>

<div class="pane" id="pane-ai">
  <div class="card">
    <h2>API 配置</h2>
    <div style="margin-bottom:12px;"><label>API 地址</label><input type="text" id="ai-api-url"></div>
    <div style="margin-bottom:12px;"><label>API Key</label><input type="password" id="ai-api-key" placeholder="留空不变"><small style="color:#71717a;">当前: <span id="ai-key-masked"></span></small></div>
    <div style="margin-bottom:12px;"><label>模型</label>
      <select id="ai-model"><option value="deepseek-v4-flash">deepseek-v4-flash</option><option value="deepseek-v4-pro">deepseek-v4-pro</option></select>
    </div>
  </div>
  <div class="card">
    <h2>回复设置</h2>
    <div style="margin-bottom:12px;"><label>系统提示词</label><textarea id="ai-prompt" rows="4"></textarea></div>
    <div class="grid2">
      <div><label>最大 Token</label><input type="number" id="ai-max-tokens"></div>
      <div><label>温度</label><input type="number" step="0.1" min="0" max="2" id="ai-temperature"></div>
    </div>
    <div style="margin-top:12px;"><label>超时 (秒)</label><input type="number" id="ai-timeout"></div>
  </div>
  <button class="btn primary" id="ai-save-btn">💾 保存 AI 设置</button>
</div>

<div class="pane" id="pane-oj">
  <div class="card">
    <h2>OJ 账号</h2>
    <div style="margin-bottom:12px;"><label>服务器地址</label><input type="text" id="oj-url"></div>
    <div style="margin-bottom:12px;"><label>用户名</label><input type="text" id="oj-username"></div>
    <div style="margin-bottom:12px;"><label>密码</label><input type="password" id="oj-password" placeholder="留空不变"></div>
    <div style="margin-bottom:12px;"><label>轮询间隔 (秒)</label><input type="number" id="oj-poll"></div>
    <div style="margin-bottom:12px;"><label>管理员 ID</label><input type="number" id="oj-admin"></div>
  </div>
  <button class="btn primary" id="oj-save-btn">💾 保存 OJ 设置</button>
</div>

<div class="pane" id="pane-log">
  <div class="card">
    <div class="flex" style="justify-content:space-between;"><h2>运行日志</h2><button class="btn outline" id="log-refresh-btn">🔄 刷新</button></div>
    <div class="log-box" id="log-content">加载中...</div>
  </div>
</div>
<div class="toast" id="toast"></div>

<script>
var authed = false;

document.querySelectorAll('.tab').forEach(function(tab){
  tab.addEventListener('click',function(){
    document.querySelectorAll('.tab').forEach(function(t){t.classList.remove('active')});
    document.querySelectorAll('.pane').forEach(function(p){p.classList.remove('active')});
    tab.classList.add('active');
    document.getElementById('pane-'+tab.dataset.tab).classList.add('active');
    if(tab.dataset.tab==='log')loadLog();
  });
});

function toast(m,t){
  var e=document.getElementById('toast');
  e.textContent=m;e.className='toast '+(t||'success');
  setTimeout(function(){e.classList.add('show')},10);
  setTimeout(function(){e.classList.remove('show')},3000);
}

async function api(u,o){
  var r=await fetch(u,Object.assign({headers:{'Content-Type':'application/json'}},o||{}));
  return r.json();
}

function requireAuth(){
  if(!authed){toast('请先输入管理密码解锁','error');return false}
  return true;
}

async function unlock(){
  var user=document.getElementById('user-input').value.trim();
  var pwd=document.getElementById('pwd-input').value;
  if(!user||!pwd){toast('请输入管理账号和密码','error');return}
  var r=await api('/api/check_pass?user='+encodeURIComponent(user)+'&pwd='+encodeURIComponent(pwd));
  if(r.ok){
    authed=true;
    document.getElementById('lock-label').textContent='🔓 已解锁'+(r.is_new?'（已保存为新管理员）':'');
    document.getElementById('user-input').value='';document.getElementById('user-input').style.display='none';
    document.getElementById('pwd-input').value='';document.getElementById('pwd-input').style.display='none';
    document.getElementById('unlock-btn').style.display='none';
    toast(r.is_new?'已保存为新管理员':'解锁成功');
    loadConfig();
  }else{
    toast('账号或密码错误','error');
  }
}

async function refreshStatus(){
  var d=await api('/api/status');
  var r=d.bot_running;
  var b=document.getElementById('status-badge');
  b.textContent=r?'● 运行中':'○ 已停止';
  b.className='badge '+(r?'green':'red');
  document.getElementById('status-text').textContent=d.status_text||'';
  document.getElementById('s-whitelist').textContent=d.whitelist_count;
  document.getElementById('s-blocked').textContent=d.blocked_words_count;
  document.getElementById('s-msgs').textContent=d.messages_processed;
  document.getElementById('s-users').textContent=d.active_users;
  document.getElementById('s-admin').textContent=d.admin_id;
  document.getElementById('btn-start').style.display=r?'none':'';
  document.getElementById('btn-stop').style.display=r?'':'none';

  // 思考过程（仅解锁后显示）
  var tc=d.thinking_content||'';
  var tC=document.getElementById('thinking-card'),tX=document.getElementById('thinking-content');
  if(tc&&authed){tC.style.display='';tX.textContent=tc;tX.scrollTop=tX.scrollHeight}else{tC.style.display='none'}
}
setInterval(refreshStatus,1500);

document.getElementById('btn-start').addEventListener('click',async function(){
  if(!requireAuth())return;
  var r=await api('/api/bot/start',{method:'POST',body:'{}'});toast(r.message);
});
document.getElementById('btn-stop').addEventListener('click',async function(){
  if(!requireAuth())return;
  if(!confirm('确定要停止 Bot 吗？'))return;
  var r=await api('/api/bot/stop',{method:'POST',body:'{}'});toast(r.message);
});

var config={};
async function loadConfig(){
  if(!authed)return;
  config=await api('/api/config');
  renderWhitelist();renderBlocked();renderAI();renderOJ();
}
async function saveConfig(u,m){
  if(!requireAuth())return;
  var r=await api('/api/config',{method:'POST',body:JSON.stringify(u)});
  toast(r.message,r.ok?'success':'error');if(r.ok)loadConfig();
}

function escHtml(s){return String(s).replace(/[&<>"]/g,function(m){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]})}
function uid(u){return typeof u==='number'?u:u.id}
function unote(u){return typeof u==='number'?'':(u.note||'')}

function renderWhitelist(){
  var l=document.getElementById('whitelist-list');
  if(!authed){l.innerHTML='<div style="color:#71717a;">请输入密码解锁后查看</div>';return}
  var raw=config.bot&&config.bot.allowed_user_ids||[];
  if(raw.length&&typeof raw[0]==='number')raw=raw.map(function(id){return{id:id,note:''}});
  if(!raw.length){l.innerHTML='<div style="color:#71717a;">(空)</div>';return}
  var admin=config.bot&&config.bot.admin_id;
  l.innerHTML=raw.map(function(u){
    var id=uid(u),note=unote(u),isA=id==admin;
    return '<div class="list-item"><div><span class="tag">'+id+'</span>'+
      (isA?' <span class="badge gray">管理员</span>':'')+
      (note?' <span style="color:#a1a1aa;font-size:13px;">— '+escHtml(note)+'</span>':'')+
      '</div><div class="flex" style="gap:6px;">'+
      '<button class="btn outline" onclick="editNote('+id+')" style="padding:2px 10px;font-size:12px;">✏️ 备注</button>'+
      (isA?'':'<button class="btn danger" onclick="removeWL('+id+')" style="padding:2px 10px;font-size:12px;">删除</button>')+
      '</div></div>'
  }).join('')
}
async function editNote(id){
  if(!requireAuth())return;
  var raw=config.bot&&config.bot.allowed_user_ids||[];
  var u=raw.find(function(x){return uid(x)===id});
  if(!u)return;
  var note=prompt('为用户 '+id+' 设置备注：',unote(u));
  if(note===null)return;
  if(typeof u==='number'){raw=raw.map(function(x){return x===id?{id:id,note:note}:x})}
  else u.note=note;
  await saveConfig({bot:{allowed_user_ids:raw}})
}
async function removeWL(id){
  if(!requireAuth())return;
  var raw=config.bot&&config.bot.allowed_user_ids||[];
  raw=raw.filter(function(u){return uid(u)!==id});
  await saveConfig({bot:{allowed_user_ids:raw}})
}
document.getElementById('wl-add-btn').addEventListener('click',async function(){
  if(!requireAuth())return;
  var inp=document.getElementById('wl-input'),id=parseInt(inp.value);
  if(!id||isNaN(id)){toast('请输入有效 ID','error');return}
  var raw=config.bot&&config.bot.allowed_user_ids||[];
  if(raw.some(function(u){return uid(u)===id})){toast('用户已在白名单中','error');return}
  raw.push({id:id,note:''});
  await saveConfig({bot:{allowed_user_ids:raw}});inp.value=''
});
function renderBlocked(){
  var l=document.getElementById('blocked-list');
  if(!authed){l.innerHTML='<div style="color:#71717a;">请输入密码解锁后查看</div>';return}
  var w=config.bot&&config.bot.blocked_words||[];
  if(!w.length){l.innerHTML='<div style="color:#71717a;">(空)</div>';return}
  l.innerHTML=w.map(function(x){return '<div class="list-item"><span>«'+escHtml(x)+'»</span><button class="btn danger" onclick="removeBW(\''+x.replace(/'/g,"\\'")+'\')" style="padding:2px 10px;font-size:12px;">删除</button></div>'}).join('')
}
async function removeBW(word){
  if(!requireAuth())return;
  var w=(config.bot&&config.bot.blocked_words||[]).filter(function(x){return x!==word});
  await saveConfig({bot:{blocked_words:w}})
}
document.getElementById('bw-add-btn').addEventListener('click',async function(){
  if(!requireAuth())return;
  var inp=document.getElementById('bw-input'),w=inp.value.trim();
  if(!w){toast('请输入要屏蔽的词','error');return}
  var words=config.bot&&config.bot.blocked_words||[];
  if(words.indexOf(w)!==-1){toast('屏蔽词已存在','error');return}
  words.push(w);await saveConfig({bot:{blocked_words:words}});inp.value=''
});
function renderAI(){
  if(!authed)return;
  var a=config.ai||{};
  document.getElementById('ai-api-url').value=a.api_url||'';
  document.getElementById('ai-key-masked').textContent=a.api_key_masked||'未设置';
  document.getElementById('ai-api-key').value='';
  var m=document.getElementById('ai-model');
  if(a.model&&[].slice.call(m.options).some(function(o){return o.value===a.model}))m.value=a.model;else m.value='deepseek-v4-flash';
  document.getElementById('ai-prompt').value=a.system_prompt||'';
  document.getElementById('ai-max-tokens').value=a.max_tokens||4096;
  document.getElementById('ai-temperature').value=a.temperature||0.7;
  document.getElementById('ai-timeout').value=a.timeout||120;
}
document.getElementById('ai-save-btn').addEventListener('click',async function(){
  if(!requireAuth())return;
  var u={ai:{api_url:document.getElementById('ai-api-url').value.trim(),api_key:document.getElementById('ai-api-key').value.trim(),model:document.getElementById('ai-model').value,system_prompt:document.getElementById('ai-prompt').value.trim(),max_tokens:parseInt(document.getElementById('ai-max-tokens').value)||4096,temperature:parseFloat(document.getElementById('ai-temperature').value)||0.7,timeout:parseInt(document.getElementById('ai-timeout').value)||120}};
  await saveConfig(u,'AI 设置已保存')
});
function renderOJ(){
  if(!authed)return;
  var o=config.oj||{},b=config.bot||{};
  document.getElementById('oj-url').value=o.base_url||'';
  document.getElementById('oj-username').value=o.username||'';
  document.getElementById('oj-password').value='';
  document.getElementById('oj-poll').value=b.poll_interval_seconds||3;
  document.getElementById('oj-admin').value=b.admin_id||'';
}
document.getElementById('oj-save-btn').addEventListener('click',async function(){
  if(!requireAuth())return;
  var pw=document.getElementById('oj-password').value.trim();
  var u={oj:{base_url:document.getElementById('oj-url').value.trim(),username:document.getElementById('oj-username').value.trim()},bot:{poll_interval_seconds:parseInt(document.getElementById('oj-poll').value)||3,admin_id:parseInt(document.getElementById('oj-admin').value)||214}};
  if(pw)u.oj.password=pw;
  await saveConfig(u,'OJ 设置已保存')
});
async function loadLog(){
  if(!authed){document.getElementById('log-content').textContent='请解锁后查看日志';return}
  var b=document.getElementById('log-content');b.textContent='加载中...';
  var d=await api('/api/log');b.textContent=(d.lines||[]).join('\n')||'(空)';b.scrollTop=b.scrollHeight
}
document.getElementById('log-refresh-btn').addEventListener('click',loadLog);
loadConfig();
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
    print(f"  \033[90m· 首次使用请在页面设置管理密码\033[0m")
    start(bot_state=None)
