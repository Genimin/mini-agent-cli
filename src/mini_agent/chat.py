"""P2: 多轮对话状态管理。

核心认知：API 是无状态的。所谓「记忆」，就是每轮把整个 messages 数组全量重发。
"""

# 建议的系统提示词，可自行调整
SYSTEM_PROMPT = "你是一个乐于助人的中文助手。你可以使用提供的工具来回答问题。"


class ChatSession:
    """管理 messages 数组的多轮会话。

    内部结构示例（P4 之后）：
        [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "郑州今天多少度？"},
            {"role": "assistant", "content": "", "tool_calls": [
                {"id": "call_xxx", "type": "function",
                 "function": {"name": "get_weather", "arguments": "{\\"city\\": \\"郑州\\"}"}}
            ]},
            {"role": "tool", "tool_call_id": "call_xxx", "content": "{...天气数据...}"},
            {"role": "assistant", "content": "郑州今天 25 度，晴。"},
        ]
    """

    def __init__(self, system_prompt: str = SYSTEM_PROMPT) -> None:
        self.messages: list[dict] = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def add_user(self, content: str) -> None:
        """TODO(P2): append 用户消息。"""

    def add_assistant(self, message: dict) -> None:
        """TODO(P2/P4): append 完整的助手消息 dict。

        注意：P4 工具调用时，这里存的是含 tool_calls 字段的完整 dict，
        而不是只存 content——回填工具结果时 API 要求 assistant 消息原样在场。
        """

    def add_tool_result(self, tool_call_id: str, content: str) -> None:
        """TODO(P4): append 工具结果消息。"""

    def total_tokens_used(self) -> int:
        """TODO(P5): 累计所有轮次的 usage。

        提示：在 cli.py 里每次调用后把 usage 存到 session 上，这里只做求和。
        """

    def reset(self) -> None:
        """清空到初始状态（保留 system prompt）。"""
        self.messages = [m for m in self.messages if m["role"] == "system"]
