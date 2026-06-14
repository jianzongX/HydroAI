# 🦕 HydroAI 使用教程

> Hydro OJ 站内消息 AI 自动回复机器人 + Web 管理面板

---

## 📦 部署结构

```
/opt/HydroAI/
├── main.py              入口文件
├── bot.py               机器人主逻辑（消息轮询、AI 回复）
├── config.py            配置管理（settings.json 读写）
├── ai_client.py         AI API 客户端（DeepSeek 流式回复）
├── oj_client.py         OJ 站内信 API 封装（登录、收发消息）
├── command_parser.py    自然语言命令解析
├── console_ui.py        控制台 UI 统一管理
├── web_tools.py         工具函数（时间查询）
├── web_server.py        Web 管理面板（端口 8080）
├── settings.json        配置文件（含 OJ 账号、AI API Key、白名单等）
├── venv/                Python 虚拟环境
└── bot.log              运行日志
```

---

## 🚀 启动与停止

### 服务方式（推荐，开机自启）

```bash
# 查看状态
systemctl status hydroai

# 重启
systemctl restart hydroai

# 停止
systemctl stop hydroai

# 查看实时日志
journalctl -u hydroai -f
```

### 前台方式（调试用）

```bash
cd /opt/HydroAI && source venv/bin/activate
python main.py
```

---

## 🌐 Web 管理面板

浏览器打开：**http://192.168.0.108:8080**

功能：
- 查看机器人运行状态
- 启动 / 停止 Bot
- 管理白名单（添加/删除/备注）
- 管理屏蔽词
- 修改 AI 配置（API Key、模型、提示词等）
- 修改 OJ 配置（账号密码、轮询间隔）
- 实时运行日志

---

## 💬 站内消息管理（管理员）

所有管理操作支持自然语言，在 OJ 站内信直接对 Bot 说：

### 白名单管理

| 你说 | 效果 |
|---|---|
| `把222加入白名单` | 添加用户 222 |
| `添加用户123` | 同上 |
| `允许456` | 同上 |
| `把222从白名单移除` | 删除用户 222 |
| `踢出123` | 同上 |
| `删除用户456` | 同上 |
| `白名单有哪些人` | 查看白名单列表 |
| `列表` | 同上 |
| `同意申请 222` | 批准用户 222 的加入申请 |

### 屏蔽词管理

| 你说 | 效果 |
|---|---|
| `添加屏蔽词广告` | 添加屏蔽词「广告」 |
| `屏蔽一下推广` | 同上（简短形式） |
| `删除屏蔽词广告` | 删除屏蔽词 |
| `查看屏蔽词` | 查看所有屏蔽词 |

### 状态查询

| 你说 | 效果 |
|---|---|
| `#状态` 或 `#status` | 查看完整运行状态 |
| `运行了多久` | 查看运行时长 |
| `处理了多少消息` | 查看已处理消息数 |
| `余额还剩多少` | 查询 DeepSeek 余额 |

### # 快捷命令

| 命令 | 效果 |
|---|---|
| `#添加 222` | 添加白名单 |
| `#删除 222` | 删除白名单 |
| `#同意申请 222` | 批准申请 |
| `#列表` / `#list` | 查看列表 |
| `#状态` / `#status` | 查看状态 |
| `#帮助` / `#help` | 查看帮助 |
| `#添加屏蔽词 xxx` | 添加屏蔽词 |
| `#删除屏蔽词 xxx` | 删除屏蔽词 |
| `#设置 api sk-xxx` | 更新 API Key |

---

## 👥 用户权限

| 身份 | 权限 |
|---|---|
| **管理员** (`admin_id`) | 全部管理操作 + AI 对话 |
| **白名单用户** | AI 对话 |
| **非白名单用户** | 仅能发送 `#申请` |

非白名单用户发送 `#申请` 后，管理员会收到通知：
```
【申请】用户 xxx(ID:123) 申请加入白名单
输入 #同意申请 123 批准
```

---

## ⚙️ 配置文件 (`settings.json`)

```json
{
    "oj": {
        "username": "你的 OJ 用户名",
        "password": "你的 OJ 密码",
        "base_url": "https://hydro.ac"
    },
    "ai": {
        "api_key": "sk-你的 DeepSeek API Key",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-v4-flash",
        "system_prompt": "AI 的系统提示词",
        "max_tokens": 4096,
        "temperature": 0.7,
        "timeout": 120
    },
    "bot": {
        "admin_id": 214,
        "allowed_user_ids": [
            {"id": 214, "note": "管理员"},
            {"id": 222, "note": ""}
        ],
        "poll_interval_seconds": 3,
        "blocked_words": ["广告", "推广"]
    }
}
```

首次运行会自动生成默认配置，填写后重启服务即可。

---

## 🖥️ NanoPC 屏幕显示

屏幕（tty1）会自动显示 Bot 的实时运行日志：

```
开机 → tty1 自动登录(root)
     → .profile 检测到 tty1
     → 启动 fbterm（中文渲染 + 文泉驿字体 20pt）
     → 自动附着到 tmux hydroai 会话
     → 显示 HydroAI 界面 + 实时日志
```

### 屏幕操作

| 操作 | 按键/命令 |
|---|---|
| 退出 tmux（回 shell） | `Ctrl+B` 松手再按 `D` |
| 回去看日志 | 输入 `tmux attach` |
| SSH 远程看日志 | `tmux attach -t hydroai` |

### 字体大小调整

```bash
sed -i 's/font-size=20/font-size=XX/' /root/.fbtermrc
systemctl restart getty@tty1
```

---

## 🔧 常用维护命令

```bash
# SSH 连接
ssh root@192.168.0.108

# 查看 Bot 实时日志
journalctl -u hydroai -f

# 重启 Bot
systemctl restart hydroai

# 查看 tmux 中的运行输出
tmux attach -t hydroai

# 编辑配置文件
nano /opt/HydroAI/settings.json

# 更新代码（从 GitHub）
cd /opt/HydroAI && git pull
systemctl restart hydroai
```

---

## 📁 项目结构说明

| 文件 | 功能 |
|---|---|
| `main.py` | 入口，初始化日志 + Web 面板 + Bot 主循环 |
| `config.py` | 配置管理，读写 `settings.json` |
| `bot.py` | 机器人主逻辑：轮询消息 → 解析命令 → AI 回复 → 发送 |
| `command_parser.py` | 自然语言命令解析，支持几十种表达方式 |
| `ai_client.py` | DeepSeek API 客户端，流式生成回复 |
| `oj_client.py` | OJ 站内信 API 封装 |
| `web_tools.py` | 工具函数（时间查询等） |
| `console_ui.py` | 控制台输出统一管理 |
| `web_server.py` | Web 管理面板（零依赖，纯 `http.server`） |
