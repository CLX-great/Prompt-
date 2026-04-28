# 智能流量套餐推荐系统

基于 FastAPI + LangChain + One API 构建的模拟通信运营商客服智能问答系统，用于根据用户需求推荐合适的手机流量套餐。

## 项目简介

本项目模拟一个运营商客服系统，通过调用大语言模型（LLM），结合提示词工程（Prompt Engineering），实现对用户流量套餐需求的智能推荐。

系统能够：

- 接收用户问题，例如“有没有土豪套餐”
- 根据预设套餐信息进行推理
- 返回自然语言形式的推荐结果
- 支持流式与非流式输出

---

## 系统架构

```text
客户端（apiTest.py）
        ↓
FastAPI 后端服务（main.py，端口 8000）
        ↓
One API 中转服务（localhost:3000）
        ↓
大语言模型（Qwen 等）
```

---

## 项目结构

```text
basic/
├── main.py                      # FastAPI 后端服务
├── apiTest.py                   # 客户端测试脚本
├── prompt_template_system.txt   # 系统提示词模板
├── prompt_template_user.txt     # 用户提示词模板
├── requirements.txt             # 项目依赖文件
├── README.md                    # 项目说明文档
└── .gitignore                   # Git 忽略文件配置
```

---

## 环境配置

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/你的仓库.git
cd basic
```

### 2. 创建并激活虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 One API

请先确保本地 One API 服务已经启动，并且地址为：

```text
http://localhost:3000
```

同时需要在 One API 后台完成：

- 添加模型渠道
- 配置可用模型
- 创建可用 Token
- 确认 Token 具有对应模型权限

### 5. 配置模型信息

在 `main.py` 中确认以下配置：

```python
ONEAPI_API_BASE = "http://localhost:3000/v1"
ONEAPI_CHAT_MODEL = "qwen-turbo"
```

注意：请不要将真实 API Key 上传到 GitHub。建议使用环境变量保存密钥。

---

## 启动项目

### 1. 启动后端服务

```bash
python main.py
```

成功启动后，服务会运行在：

```text
http://localhost:8000
```

### 2. 运行测试脚本

打开新的终端窗口，运行：

```bash
python apiTest.py
```

---

## 示例输入与输出

### 输入

```text
有没有土豪套餐
```

### 输出示例

```text
有的，可以考虑无限套餐，每月 300 元，包含 1000G 流量，适合流量需求特别大的用户。
```

---

## 功能说明

- 基于 Prompt 的流量套餐推荐
- 使用 FastAPI 构建本地 API 服务
- 使用 LangChain 管理 Prompt 与模型调用
- 通过 One API 接入大语言模型
- 支持普通非流式输出
- 支持 Streaming 流式输出
- 返回格式兼容 OpenAI API 的 `choices` 结构

---

## 常见问题

### 1. 端口被占用怎么办？

如果 `8000` 端口被占用，可以使用：

```bash
lsof -i :8000
kill -9 PID
```

或直接一行：

```bash
lsof -ti :8000 | xargs kill -9
```

### 2. 出现 401 错误怎么办？

通常表示没有正确提供 Token，需要检查请求头或 One API 配置。

### 3. 出现 403 错误怎么办？

通常表示 Token 没有权限调用当前模型，需要在 One API 后台检查模型权限。

### 4. 出现 `KeyError: choices` 怎么办？

说明接口返回的是错误信息，而不是正常模型结果。应先打印：

```python
print(response.status_code)
print(response.text)
```

再根据错误信息排查。

---

## 后续优化方向

- 增加前端页面
- 增加数据库保存用户历史对话
- 支持更多套餐规则
- 接入更多模型，例如 DeepSeek、GPT、Qwen Plus
- 部署到云服务器

---

## 作者

Linxing Cui  
The University of Sydney
