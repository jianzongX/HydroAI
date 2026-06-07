# 🦕 HydroAI

Hydro OJ 站内消息 AI 自动回复机器人 + Web 管理面板

## ✨ 功能

- 🤖 **AI 自动回复** — 监听 OJ 站内消息，调用 DeepSeek API 流式生成回复
- 🧠 **思考过程实时显示** — AI 推理过程实时显示在 Web 面板
- 💬 **对话上下文** — 记忆最近 6 轮对话，AI 能理解上下文
- 🔐 **管理密码保护** — 仪表盘顶部密码锁，保护敏感操作
- 👥 **白名单管理** — 添加/删除白名单用户，支持备注
- 🚫 **屏蔽词系统** — 自定义屏蔽词，AI 输出自动打码
- 📋 **日志查看** — 实时日志显示
- 🛠️ **全功能 Web 面板** — 状态监控、启停控制、配置修改

## 🚀 快速开始

### 1. 安装

```bash
pip install requests pyinstaller
```

### 2. 配置

复制 `settings.example.json` 为 `settings.json`，填入你的配置：

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

打开浏览器访问 **http://localhost:8080** 进入管理面板。

首次使用输入任意账号密码，自动保存为管理员凭证。

### 打包 exe

```bash
pip install pyinstaller
pyinstaller --onefile --name "HydroAI" main.py
```

## 📁 项目结构

```
HydroAI/
├── main.py             入口（集成 Web 管理面板）
├── web_server.py       Web 管理面板模块
├── bot.py              机器人主逻辑
├── config.py           配置管理
├── oj_client.py        OJ API 封装
├── ai_client.py        AI 客户端（流式回复）
├── command_parser.py   命令解析
├── settings.json       配置文件（本地，不入库）
├── settings.example.json  配置模板
└── requirements.txt    依赖清单
```

## 🔧 技术栈

- Python 3.12
- DeepSeek API（流式）
- Python 标准库 `http.server`（零依赖 Web 面板）
- PyInstaller（打包 exe）
