# DocAgent 使用指南

## 简介

DocAgent 是一个智能文档生成助手，可以自动分析代码文件、网页或文档内容，生成专业的技术文档。

**支持的输入：**
- 代码文件：`.py`, `.js`, `.java`, `.go`, `.ts`, `.cpp`, `.c`, `.rb`, `.php`
- 文档文件：`.md`, `.txt`, `.pdf`
- 网页 URL

**支持的输出：**
- API 文档
- README 文档
- 用户手册

---

## 本地运行

### 1. 安装依赖

```bash
cd d:\code\DocAgent\docagent
pip install -r requirements.txt
```

### 2. 配置 API Key

确保 `.env` 文件存在，内容如下：
```
OPENAI_API_KEY=你的API-Key
FLASK_ENV=development
PORT=5000
```

### 3. 启动服务

```bash
python app.py
```

### 4. 访问

打开浏览器访问：**http://localhost:5000**

---

## 使用方法

### 方式一：上传文件

1. 进入网页后，默认是「上传文件」标签
2. 点击「选择文件」按钮，选择一个代码文件或文档
3. 选择输出格式（Markdown 或 PDF）
4. 点击「生成文档」按钮
5. 等待生成完成，查看预览结果

### 方式二：输入 URL

1. 点击「输入URL」标签
2. 在文本框中输入网页地址（如 https://example.com）
3. 选择输出格式（Markdown 或 PDF）
4. 点击「生成文档」按钮
5. 等待生成完成，查看预览结果

---

## 示例测试

### 测试 1：Python 代码生成 API 文档

1. 创建一个测试文件 `test.py`：
```python
def hello():
    """打招呼函数"""
    print("Hello, World!")

def add(a, b):
    """加法函数"""
    return a + b
```

2. 上传 `test.py`，输出格式选择「Markdown」
3. 查看生成的 API 文档

### 测试 2：从 URL 生成文档

1. 切换到「输入URL」标签
2. 输入任意网页 URL
3. 点击「生成文档」
4. 查看生成的用户手册

---

## 故障排除

### 问题：提示 "OPENAI_API_KEY environment variable is required"

**解决方法：** 确保 `.env` 文件存在且包含正确的 API Key

### 问题：网络请求超时

**解决方法：** 检查网络连接，或者 API Key 是否有效

### 问题：生成的文档是乱码

**解决方法：** 确保输入文件是 UTF-8 编码

---

## 项目结构

```
docagent/
├── app.py              # Flask 主应用
├── agent/              # LangGraph Agent
│   ├── graph.py        # 工作流定义
│   ├── nodes.py        # 节点（路由、生成）
│   ├── prompts.py      # Prompt 模板
│   └── state.py        # 状态定义
├── extractors/         # 内容提取器
│   ├── file_extractor.py   # 文件提取
│   └── web_extractor.py    # URL 提取
├── exporters/          # 文档导出器
│   ├── markdown_exporter.py
│   └── pdf_exporter.py
├── templates/
│   └── index.html      # 前端页面
├── tests/              # 测试
└── requirements.txt    # 依赖
```

---

## 部署到 Railway

1. 在 GitHub 创建仓库并推送代码
2. 登录 https://railway.app
3. 创建新项目，选择「Deploy from GitHub」
4. 选择你的仓库
5. 在环境变量中添加 `OPENAI_API_KEY`
6. 等待部署完成，获取访问 URL

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | HTML + CSS + JS |
| 后端 | Python Flask |
| Agent | LangGraph |
| LLM | MiniMax-M2.7 |
| 部署 | Railway |
