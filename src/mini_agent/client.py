"""P1-P3: 裸 HTTP 客户端。

红线：这里只能用 httpx + 标准库。
你会亲手处理：非流式调用(P1) → 流式 SSE 解析(P3) → 重试/超时(P5)。
"""

import json
from collections.abc import Iterator

import httpx

from .config import Config


def chat_completion(config: Config, messages: list[dict], tools: list[dict] | None = None) -> dict:
    """P1: 非流式调用。POST {base_url}/chat/completions，返回完整响应 dict。

    TODO(P1):
      1. 组装请求体: {"model": ..., "messages": ..., 可选 "tools": ...}
      2. headers 带 Authorization: Bearer <key>
      3. httpx.post(...)，设置合理 timeout（建议 120s，推理模型可能很慢）
      4. resp.raise_for_status() 或手动检查状态码
      5. 返回 resp.json()

    P5 进阶：把这里的错误处理升级为「可重试/不可重试」分类。
    """
    raise NotImplementedError("P1: 请实现 chat_completion()")


def chat_completion_stream(
    config: Config, messages: list[dict], tools: list[dict] | None = None
) -> Iterator[dict]:
    """P3: 流式调用。yield 每个 SSE 事件解析后的 dict。

    TODO(P3):
      1. 请求体加 "stream": true 和 "stream_options": {"include_usage": true}
      2. 用 httpx.stream(...) 逐行迭代
      3. 只处理 "data: " 开头的行；"data: [DONE]" 时终止
      4. 每行剥掉 "data: " 前缀后 json.loads，yield 出去
      5. 注意 UTF-8 解码（Windows 控制台记得 PYTHONIOENCODING=utf-8 或 sys.stdout.reconfigure）

    迭代器消费方（cli.py）负责拼 delta 和统计 usage。
    """
    raise NotImplementedError("P3: 请实现 chat_completion_stream()")
