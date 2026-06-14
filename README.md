# 🦕 HydroAI

Hydro OJ 站内消息 AI 自动回复机器人 + Web 管理面板

---

## ✨ 功能

- 🤖 **AI 自动回复** — 监听 OJ 站内消息，调用 DeepSeek API 流式生成回复
- 🧠 **思考过程实时显示** — AI 推理过程实时显示在 Web 面板
- 👥 **白名单管理** — 添加/删除白名单用户，支持备注
- 🚫 **屏蔽词系统** — 自定义屏蔽词，AI 输出自动打码
- 🛠️ **全功能 Web 面板** — 控制台日志实时显示、启停控制、配置修改
- 🗣️ **自然语言管理** — 直接用中文管理白名单、屏蔽词等，无需记命令

---

## 🚀 快速开始

### 1. 安装

```bash
pip install requests pyinstaller
```

### 2. 配置

编辑 `settings.json`，填入 OJ 账号和 AI API Key（首次运行自动生成模板）：

```json
{
    "oj": {
        "username": "your_oj_username",
        "password": "your_oj_password",
        "base_url": "https://hydro.ac"
    },
    "ai": {
        "api_key": "sk-your-deepseek-api-key",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-v4-flash"
    }
}
```

### 3. 运行

```bash
python main.py
```

浏览器访问 **http://localhost:8080** 进入管理面板。

### 打包 exe

```bash
pip install pyinstaller
pyinstaller --onefile --name "HydroAI" main.py
```

---

## 📖 使用教程

### 启动与停止

**服务方式（推荐，开机自启）：**

```bash
systemctl status hydroai     # 查看状态
systemctl restart hydroai    # 重启
systemctl stop hydroai       # 停止
journalctl -u hydroai -f     # 查看实时日志
```

**前台方式（调试用）：**

```bash
cd /opt/HydroAI && source venv/bin/activate
python main.py
```

### Web 管理面板

浏览器打开 `http://<设备IP>:8080` 即可使用：

- 查看机器人运行状态（启动/停止）
- 管理白名单（添加/删除/备注）
- 管理屏蔽词
- 修改 AI 配置（API Key、模型、提示词、参数）
- 修改 OJ 配置（账号、密码、轮询间隔）
- 实时运行日志

### 站内消息管理（管理员）

所有管理操作支持自然语言，在 OJ 站内信直接对 Bot 说：

**白名单管理：**

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

**屏蔽词管理：**

| 你说 | 效果 |
|---|---|
| `添加屏蔽词广告` | 添加屏蔽词「广告」 |
| `屏蔽一下推广` | 同上（简短形式） |
| `删除屏蔽词广告` | 删除屏蔽词 |
| `查看屏蔽词` | 查看所有屏蔽词 |

**状态查询：**

| 你说 | 效果 |
|---|---|
| `#状态` / `#status` | 查看完整运行状态 |
| `运行了多久` | 查看运行时长 |
| `处理了多少消息` | 查看已处理消息数 |
| `余额还剩多少` | 查询 DeepSeek 余额 |

**# 快捷命令：**

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

### 用户权限

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

### 配置文件 (`settings.json`)

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
        "admin_id": 0,
        "allowed_user_ids": [],
        "poll_interval_seconds": 3,
        "blocked_words": []
    }
}
```

首次运行自动生成默认配置，填写后重启服务即可。

---

## 📁 项目结构

```
HydroAI/
├── main.py              入口文件
├── bot.py               机器人主逻辑（消息轮询、AI 回复）
├── config.py            配置管理（settings.json 读写）
├── ai_client.py         AI API 客户端（DeepSeek 流式回复）
├── oj_client.py         OJ 站内信 API 封装（登录、收发消息）
├── command_parser.py    自然语言命令解析（50+ 表达方式）
├── console_ui.py        控制台 UI 统一管理
├── web_tools.py         工具函数（时间查询）
├── web_server.py        Web 管理面板后端
├── index.html           Web 管理面板前端（单独文件）
├── settings.json        配置文件（用户填写，不入库）
└── bot.log              运行日志
```

---

## 🖥️ 设备屏幕显示（NanoPC / 树莓派等）

屏幕（tty1）会自动显示 Bot 的实时运行日志：

```
开机 → tty1 自动登录(root)
     → .profile 检测到 tty1
     → 启动 fbterm（中文渲染）
     → 自动附着到 tmux hydroai 会话
     → 显示 HydroAI 界面 + 实时日志
```

### 屏幕操作

| 操作 | 按键/命令 |
|---|---|
| 退出 tmux（回到 shell） | `Ctrl+B` 松手再按 `D` |
| 回去看日志 | `tmux attach` |
| SSH 远程查看日志 | `tmux attach -t hydroai` |

### 字体大小调整

```bash
sed -i 's/font-size=20/font-size=XX/' /root/.fbtermrc
systemctl restart getty@tty1
```

---

## 🔧 常用维护命令

```bash
# SSH 连接设备
ssh root@<设备IP>

# 查看 Bot 实时日志
journalctl -u hydroai -f

# 重启 Bot
systemctl restart hydroai

# 查看 tmux 中的运行输出
tmux attach -t hydroai

# 编辑配置文件
nano /opt/HydroAI/settings.json

# 更新代码
cd /opt/HydroAI && git pull
systemctl restart hydroai
```

---

## 🔧 技术栈

- Python 3.12
- DeepSeek API（流式）
- Python 标准库 `http.server`（零依赖 Web 面板）
- PyInstaller（打包 exe）

---

## 📋 更新日志

### v1.3.0 fix (2026-06-14)

- 🧩 **HTML 页面分离** — 将内嵌在 `web_server.py` 中的 150+ 行 HTML/CSS/JS 提取到独立 `index.html` 文件
- 🧹 修改样式或前端逻辑不再需要动 Python 代码，前后端完全分离

### v1.3.0 (2026-06-14)

- 🎨 **全新控制台 UI** — 统一 Console 类管理输出，信息更清晰、格式更一致
- 🗣️ **自然语言管理大升级** — 支持 50+ 种自然表达，怎么问都能识别
- 🧹 **移除记忆功能** — 每次对话独立，AI 不再受历史干扰
- ⏰ **时间感知** — 管理员可使用 `#状态` 查看运行时长，系统提示注入当前时间
- 📋 **内置完整使用教程** — 命令速查、配置说明、维护指南全覆盖

### v1.2.1 (2026-06-14)

- 🐛 修复 token 消耗信息进入对话记忆，避免 AI 模仿此格式
- ✨ 新增状态查询功能，管理员可通过 `#状态` 或自然语言查询
- 🌐 DeepSeek 余额实时查询

### v1.2.0 (2026-06-13)

- 🐛 修复首次运行崩溃（`_comment` 字段导致 `dict()` 构造失败）
- ⚡ 改用 `copy.deepcopy` 安全创建默认配置
- 🚀 打包为单 exe 文件，首次启动自动生成 `settings.json`

### v1.1.2

- 自动创建默认配置，移除仓库中的 settings.json

### v1.1.1

- 彩虹色 ASCII 艺术字，HydroAI 品牌重命名，自动识别管理员
