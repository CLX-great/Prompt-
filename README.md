# 智能流量套餐推荐系统（basic）

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
## 升级➡️对话记忆（Memory）功能（withMemoryTest）

为了提升系统的智能化程度，本项目引入了基于 **LangChain + SQLite** 的对话记忆机制，使模型能够结合历史对话进行更准确的回答。

### 功能特点

- 支持多轮对话上下文记忆
- 根据 `userId` 和 `conversationId` 区分不同用户会话
- 自动存储并读取历史聊天记录
- 限制历史长度（默认保留最近 10 条）以提高效率
- 让模型具备“上下文理解能力”

---

### 工作流程

```text
用户请求
   ↓
FastAPI 接口接收请求
   ↓
根据 userId + conversationId 获取历史记录（SQLite）
   ↓
拼接 Prompt（System + History + 当前问题）
   ↓
调用 LLM（Qwen 等）
   ↓
返回结果并更新历史记录
```

### 事例效果
<img width="2636" height="1320" alt="image" src="https://github.com/user-attachments/assets/812cc176-187f-4407-892e-eb67c14b25f2" />

```text
根据图片可以看出，支持多轮对话上下文记忆。并且对于与流量套餐无关的内容，客服没有胡乱回答，而是进行了提醒。
```

---

## 升级➡️质量检查测试（cot）

本项目调用的是大语言模型接口，因此模型的回答并不是完全固定的规则判断结果。即使输入内容相同，模型在多次运行时也可能返回不同结果。
### 事例效果
<img width="1564" height="1448" alt="image" src="https://github.com/user-attachments/assets/ffa88db7-4d8a-4492-a41b-502e6cbde626" />

```text
这个问题正确输出应该是N，根据图片可以看到它有时候输出N，有时候输出Y。不过后面输出N更多一些。
```

---

## 升级➡️质量检查测试2(selfConsistency)

本项目调用的是大语言模型接口，因此模型的回答并不是完全固定的规则判断结果。即使输入内容相同，模型在多次运行时也可能返回不同结果。

为提高判断结果的稳定性，本项目进行了以下优化：

### 1. Prompt 优化

在 `prompt_template_system.txt` 中新增了以下要求：

```text
请一步一步分析后再作出回答
```

该设置用于引导模型在给出最终判断前先进行逐步推理，从而减少直接给出错误结论的情况。

### 2. 多次调用与投票机制

在代码层面，系统会对同一输入连续调用模型 5 次，并统计每次输出中的 Y 和 N 数量。

最终系统会根据多数投票结果返回判断：

- 如果 Y 的数量更多，则输出 Y
- 如果 N 的数量更多，则输出 N
- 如果两者数量相同，则默认输出 Y

这种方式可以降低单次模型输出不稳定带来的影响，提高整体判断结果的可靠性。

相关核心逻辑位于 main.py 中的 /v1/chat/completions 接口部分，代码会循环调用模型 5 次，并分别统计 Y 和 N 的出现次数。

### 事例效果

<img width="2094" height="454" alt="image" src="https://github.com/user-attachments/assets/faf8452c-c0d9-4977-9f3b-5a90095decde" />

```text
结果与预期完全一致
因此，系统通过多次调用与多数投票机制，最终可以得到更稳定、更接近正确结果的判断。
```

## 升级➡️扩展了思维链NEW（sportservice）

本项目实现了一个基于 LangChain 的多阶段推理系统（Multi-Chain Pipeline）。

### 推理流程

```text
输入：用户能力描述
        ↓
Chain1：能力分析（结构化输出）
        ↓
Chain2：候选生成（可能运动项目）
        ↓
Chain3：能力匹配评估（约束过滤）
        ↓
Chain4：报告生成（自然语言输出）
```

### 核心特点

- 使用多个 Prompt 分阶段推理
- 每个 Chain 只负责单一任务（职责清晰）
- 引入剪枝（Pruning）优化推理效率
- 避免无效结果生成

### 示例输出
<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/65a7216b-c594-41ae-8b58-1ee466630ec8" />
<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/9411c620-a043-4948-8f01-48d98116567e" />
<img width="1000" height="406" alt="image" src="https://github.com/user-attachments/assets/824c89b0-8aa0-4db8-b691-84f0a74b7fc5" />

## 最终升级➡️加UI界面（basicWebUI）

### 示例输出

<img width="2606" height="1384" alt="image" src="https://github.com/user-attachments/assets/9304c199-ab69-49e4-a550-fc21e94d2c79" />


## 作者

Linxing Cui  
The University of Sydney
