# Agent 工程师学习规划 · 个人执行版

> 面向：有编程基础的成熟 Java 后端工程师
> 总周期：约 2~2.5 个月（业余时间）
> 最后更新：2026-09-23

---

## 一、路线图总览

| 阶段 | 时长 | 内容 | 状态 |
|---|---|---|---|
| **P0 语言切换** | 1 周 | Python 3.11 + asyncio + httpx + pydantic；适应生态（uv / 类型系统 / async 习惯） | 🟡 进行中 |
| **P1 模型行为** | 3~5 天（可与 P0 并行） | token 与上下文窗口、采样与非确定性、费用结构、KV cache、prompt vs RAG vs 微调边界 | ⬜ 未开始 |
| **P2 实战一** | 1~2 周 | 从零写带工具调用的 CLI agent（即本项目） | 🟡 已开工 |
| **P3 实战二** | 2~3 周 | 沙箱 agent：文件读写 + shell 执行 + 上下文管理 + 多轮状态 | ⬜ 未开始 |
| **P4 可靠性工程** | 2 周 | evals 设计、轨迹观测、成本核算、提示注入防御 | ⬜ 未开始 |
| **P5 编排** | 按需 | 多 agent、MCP、LangGraph —— 用到再学 | ⬜ 已降级为可选 |

### 两条关键判断

1. **最大优势在 P4**：微服务熔断/降级/幂等的工程经验可直接迁移到 agent 可靠性工程。多数转型者死在这一层，对你是降维打击。
2. **最大的坑在 P0→P2 的跳跃**：不是难度问题，是「感觉太简单而不动手」。LLM 的坑（工具调用回填、流式解析、上下文膨胀）只有亲手写才踩得到。

---

## 二、知识架构分层（L0~L5）

```
L0 软件工程底座 ── 不可跳过，agent 工程的失败 80% 死在这
L1 模型行为学 ── 把 LLM 当黑盒，但吃透它的 I/O 特性
L2 API 裸调用 ── 动手起点，禁用框架
L3 Agent 核心循环 ── 本体，"agent"一词 90% 指这个
L4 可靠性工程 ── evals + 观测 + 安全，真正的分水岭
L5 编排 ── 可选，按需再学
```

**L0 · 软件底座**：Python 或 TS、异步编程、REST/streaming API、git、调试能力。
判断标准：能独立写完一个带重试和错误处理的 API 客户端。

**L1 · 模型行为学**：token 与上下文窗口、非确定性（temperature/采样）、KV cache 与费用结构、微调 vs 提示 vs RAG 的边界。
判断标准：能预测「为什么这个 prompt 会失败」。

**L2 · API 裸调用**：chat completions、**tool/function calling**、JSON 结构化输出、流式、embeddings。
实践：不碰任何框架，从零写一个能调工具的 CLI 聊天机器人，~300 行。

**L3 · 核心循环**（本体）：`模型 → 工具调用 → 结果回填 → 循环`，加上：上下文工程（system prompt、压缩、记忆）、**工具设计**（schema 即提示、错误信息要写给模型看）、多轮状态管理。
实践：写一个能在沙箱里读写文件、跑 shell 命令的 agent —— 做到这个，你就理解了 Codex / Claude Code 的骨架。

**L4 · 可靠性工程**（分水岭）：**evals（怎么证明你的改动变好了，而不是感觉变好了）**、轨迹观测与成本核算、重试/超时/降级、沙箱与提示注入防御、人在环路的审批设计。
自学者和工程师的分界线就在这层。

**L5 · 编排（可选）**：多智能体协作（诚实说：被高估）、MCP 等工具协议、LangGraph 类框架 —— **先裸写再学框架**。

---

## 三、当前进度定位

```
P2 实战项目「mini-agent-cli」
├── P0 项目骨架        ✅ 已完成（uv sync 通过，可启动）
├── 阶段1 单轮调用      🟡 ← 卡在这里（待完成: config.py 的 load_config()）
├── 阶段2 多轮对话      ⬜
├── 阶段3 流式          ⬜
├── 阶段4 工具调用 ⭐    ⬜
└── 阶段5 工程化        ⬜
```

### 已就绪的环境

| 项 | 值 |
|---|---|
| 项目位置 | `D:\codexFiles\mini-agent-cli\` |
| Python | 3.11（uv 管理） |
| uv | 0.12.12 |
| API 端点 | `https://ai.hixx.cc:9898/v1`（OpenAI 兼容） |
| 模型 | `hixx-txt`（中转别名，后端动态路由 GLM / DeepSeek） |
| context_length | 131072（已在 config.yaml 显式配置，保守值） |

---

## 四、眼下的具体目标

**目标：让 REPL 跑起来，并看清一次 API 响应的原始结构。**

```bash
cd /d/codexFiles/mini-agent-cli
cp .env.example .env          # ① 填入你的真实 key
# ② 实现 src/mini_agent/config.py 的 load_config()
uv run mini-agent             # ③ 应该能进 REPL 不再报「P0 未完成」
```

`load_config()` 就三件事：
1. `Path(__file__).parents[2]` 定位项目根 → `load_dotenv(root/".env")`
2. 用 `_env()` 读三个环境变量填进 `Config`
3. 缺配置时抛中文报错（提示用户先 `cp .env.example .env`）

**验收标准**：`uv run mini-agent` 进入 REPL 并打印 `mini-agent 已启动 (model=hixx-txt)`。

---

## 五、项目阶段验收清单（详见项目内 README.md）

| 阶段 | 核心任务 | 你能回答的问题 |
|---|---|---|
| P0 骨架 | ✅ 已完成 | — |
| P1 单轮调用 | 裸 POST，打印完整响应 JSON | `usage` 有哪些字段？各什么含义？ |
| P2 多轮对话 | 维护 messages 数组 | 为什么每轮要全量重发历史？（无状态服务 + KV cache） |
| P3 流式 | SSE 逐行解析 | 如何从最后一个 chunk 统计 token？ |
| P4 工具调用 ⭐ | schema + tool_calls 回填循环 | 模型要调两次工具时，messages 是什么结构？ |
| P5 工程化 | 超时/重试/错误分类/测试 | 哪些错误该重试，哪些不该？ |

### 红线 ⚠️
1. 全程只用 `httpx` + 标准库（pydantic 仅用于 config 解析）
2. 不要看 openai SDK 源码来「抄」—— 先自己实现，P4 完成后再对照
3. `.env` 别提交到 git

---

## 六、信息源（全部免费、非卖课）

- **官方文档**：Anthropic《Building effective agents》、OpenAI function calling 指南
- **真实源码**（最好的教材）：Codex CLI（Rust）、Hermes Agent（Nous Research）、OpenHands、SWE-agent
- **Karpathy 免费视频**：从零构建 GPT（唯一值得看的入门系）
- **hamelhusain 的 evals 系列**：L4 层最好的免费材料
- **论文只需三篇内**：ReAct、SWE-bench、Toolformer（按需）

---

## 七、注意（学习用途）

使用第三方中转站时记住：
- 所有请求内容（含代码）明文经过中转服务器，**不要发送敏感数据**
- 上游模型可能随时变更（`hixx-txt` 实测后端在 GLM 和 DeepSeek 之间切换）
- 计费按 token，注意余额
