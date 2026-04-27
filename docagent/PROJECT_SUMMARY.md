# DocAgent 项目总结

## 项目概述

**项目名称：** DocAgent - 智能文档生成助手

**目的：** 技术文档工程师求职作品集，展示 AI Agent 开发能力

**核心功能：** 用户上传文件（代码/文档）或输入网页 URL，Agent 自动分析内容并生成结构化文档（API 文档、README、用户手册等）

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | HTML + CSS + JS（纯原生，无框架） |
| 后端 | Python Flask |
| Agent | LangGraph |
| LLM | MiniMax-M2.7（Anthropic 兼容 API） |
| PDF 生成 | fpdf2 |
| 部署 | Railway |

---

## 项目结构

```
docagent/
├── app.py                    # Flask 主应用，API 路由
├── config.py                 # 配置（从 .env 读取）
├── agent/
│   ├── graph.py             # LangGraph 工作流定义
│   ├── nodes.py             # 节点（route_node, generate_node）
│   ├── prompts.py           # Prompt 模板
│   └── state.py             # AgentState TypedDict
├── extractors/
│   ├── file_extractor.py    # 本地文件提取
│   └── web_extractor.py     # 网页 URL 提取
├── exporters/
│   ├── markdown_exporter.py # Markdown 导出
│   └── pdf_exporter.py      # PDF 导出（中文回退到 ASCII）
├── templates/
│   └── index.html           # 前端页面
├── tests/                   # 测试文件
├── .env                     # 环境变量（含 API Key）
├── requirements.txt         # 依赖
└── Procfile                 # Railway 启动命令
```

---

## 关键配置

**API 配置（.env）：**
```
OPENAI_API_KEY=sk-cp-xxx  # MiniMax API Key
FLASK_ENV=development
PORT=5000
```

**MiniMax API：**
- Base URL: `https://api.minimaxi.com/anthropic`
- Model: `MiniMax-M2.7`

---

## 已完成功能

1. **文件上传** - 支持 .py, .js, .java, .go, .ts, .cpp, .c, .rb, .php, .md, .txt, .pdf
2. **URL 解析** - 输入网页 URL，提取内容
3. **智能路由** - Agent 自动判断内容类型（code/markdown/pdf/web/text）
4. **文档生成** - 根据类型生成 API 文档、README 或用户手册
5. **格式导出** - 支持 Markdown 和 PDF 两种输出格式
6. **Web 界面** - 支持文件上传和 URL 输入两种方式

---

## 运行方式

```bash
cd d:\code\DocAgent\docagent
python app.py
# 访问 http://localhost:5000
```

---

## 测试文件

- `tests/fixtures/sample_code.py` - Python 测试代码
- `tests/fixtures/sample_readme.md` - Markdown 测试文档

---

## 已知问题/待改进

1. **PDF 中文支持** - fpdf2 不支持中文，导出时中文会回退到 ASCII 显示
2. **ThinkingBlock** - MiniMax-M2.7 返回 ThinkingBlock 而非 TextBlock，代码已做兼容处理
3. **Windows 文件锁定** - 临时文件删除有重试机制

---

## GitHub

仓库：https://github.com/hualI66/docagent

---

## 近期修改记录

- 使用原生 `anthropic` 库替代 `langchain_anthropic`
- MiniMax URL: `https://api.minimaxi.com/anthropic`（注意是 minimaxi 不是 minimax）
- 处理 ThinkingBlock，从 thinking 内容中提取答案
- PDF 导出添加了异常处理回退
