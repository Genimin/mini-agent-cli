# mini-agent-cli

从零构建的带工具调用能力的 CLI 聊天机器人。**学习项目**：不使用任何框架/SDK，只用 `httpx` + 标准库，目的是看清 LLM agent 的协议本质。

## 你将亲手实现的

```
用户输入 ──► messages 数组 ──► POST /v1/chat/completions
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │ 响应里有没有 tool_calls？      │
                     └───────┬───────────────┬───────┘
                          没有│            有│
                             ▼               ▼
                    打印助手回复      本地执行工具函数
                             │       （计算器/天气查询）
                             │               │
                             │               ▼
                             │      结果以 role=tool 回填 messages
                             │               │
                             └───────► 再次调用模型（循环）
```

这个循环就是所有 agent（Codex / Claude Code / Hermes）的原子操作。

## 项目结构

```
mini-agent-cli/
├── pyproject.toml          # uv 管理的项目配置
├── .env.example            # 配置模板（复制为 .env 并填入 key）
├── README.md
├── src/
│   └── mini_agent/
│       ├── __init__.py
│       ├── config.py       # P0: 配置读取（base_url / api_key / model）
│       ├── client.py       # P1-P3: 裸 HTTP 客户端（非流式/流式）
│       ├── chat.py         # P2: 多轮对话状态（messages 数组管理）
│       ├── tools.py        # P4: 工具定义 + 本地执行（计算器/天气）
│       └── cli.py          # 入口 REPL
└── tests/
    └── test_tools.py       # P5: 工具层单元测试
```

## 阶段验收清单（对照填空）

### P0 骨架 ✅（已完成）
- [x] `uv sync` 依赖安装成功
- [x] `uv run mini-agent` 进入 REPL，能输入能退出

### P1 单轮调用
- [ ] 完成 `client.py::chat_completion()`：裸 POST，返回完整 JSON dict
- [ ] 在 REPL 打印一次完整的原始响应 JSON（用 `json.dumps(..., indent=2, ensure_ascii=False)`）
- [ ] **能回答**：响应里 `usage` 有哪些字段？各自什么含义？

### P2 多轮对话
- [ ] 完成 `chat.py`：维护 messages 数组，每轮把新消息 append 进去
- [ ] 连续问两遍「我叫什么」验证有记忆
- [ ] **能回答**：为什么每轮都要全量重发所有历史消息？（提示：无状态服务 + KV cache）

### P3 流式
- [ ] 完成 `client.py::chat_completion_stream()`：`stream=true`，逐行解析 SSE
- [ ] 处理 `data: {...}` 行与 `data: [DONE]` 终止标记
- [ ] 从 `stream_options: {"include_usage": true}` 的最后一个 chunk 统计 token
- [ ] 打字机效果正常显示中文（注意 UTF-8）

### P4 工具调用 ⭐ 灵魂阶段
- [ ] 完成 `tools.py`：两个工具的 schema 定义 + 执行分发
  - `calculator`：安全的表达式求值（只用 `ast` 模块，**禁止** `eval` 明文字符串）
  - `get_weather`：调 `wttr.in`（`curl wttr.in/Zhengzhou?format=j1` 的 Python 版）
- [ ] 处理响应中的 `tool_calls` 字段：解析 `function.name` / `function.arguments`
- [ ] 工具结果以 `{"role": "tool", "tool_call_id": ..., "content": ...}` 回填
- [ ] 端到端测试：问「郑州今天多少度？」→ 模型自主决定调工具 → 自然语言回答
- [ ] **能回答**：模型说想调两次工具时，messages 里应该是什么结构？

### P5 工程化
- [ ] 超时 + 重试（只重试「可重试错误」：网络错误/429/5xx；不重试 400/401）
- [ ] 错误分类打印：连接失败 / 认证失败 / 余额不足 / 上下文超长，各有明确报错
- [ ] 每轮对话结束打印 token 用量累计
- [ ] 故障注入自测：断网、错误 key、超短超时——三种故障都优雅处理
- [ ] 完成 `tests/test_tools.py`：calculator 的正常/异常/注入用例

## 运行

```bash
uv sync
cp .env.example .env    # 编辑填入你的 key
uv run mini-agent
```

## 红线 ⚠️

1. 全程只用 `httpx` + 标准库（pydantic 只用于 config 解析可以）
2. 不要看 openai SDK 的源码来「抄」——先自己实现，P4 完成后再对照
3. `.env` 别提交到 git（`.gitignore` 已配好）
