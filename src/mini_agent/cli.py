"""REPL 入口。uv run mini-agent 启动。

骨架已提供主循环框架；TODO 按 P1→P4 顺序逐步解锁。
"""

import json
import sys

from .chat import ChatSession
from .client import chat_completion
from .config import load_config
from .tools import TOOLS_SCHEMA, execute_tool

HELP = """命令:
  /help       显示本帮助
  /reset      清空对话历史（保留 system prompt）
  /raw        下一条消息的响应打印原始 JSON（P1 调试用）
  /tokens     显示累计 token 用量（P5）
  /quit       退出"""


def main() -> None:
    # Windows 控制台中文/UTF-8 兼容
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

    try:
        config = load_config()
    except NotImplementedError:
        print("P0 未完成: 请先实现 config.load_config()")
        return
    except Exception as e:  # noqa: BLE001
        print(f"配置加载失败: {e}")
        return

    session = ChatSession()
    print(f"mini-agent 已启动 (model={config.model})。输入 /help 查看命令。\n")

    while True:
        try:
            user_input = input("你> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见!")
            break

        if not user_input:
            continue
        if user_input == "/quit":
            print("再见!")
            break
        if user_input == "/help":
            print(HELP)
            continue
        if user_input == "/reset":
            session.reset()
            print("已清空对话历史。\n")
            continue
        if user_input == "/tokens":
            print(f"累计 tokens: {session.total_tokens_used()}\n")
            continue

        session.add_user(user_input)

        # ----- P1: 第一次真实调用 -----
        # TODO(P1): 调 chat_completion(config, session.messages)，打印响应 JSON 里的
        #           choices[0].message.content，并把 usage 记到 session（P5 再做）。
        # TODO(P4): 外面再套一层 while True 工具循环:
        #   response = chat_completion(config, session.messages, tools=TOOLS_SCHEMA)
        #   msg = response["choices"][0]["message"]
        #   session.add_assistant(msg)
        #   if msg.get("tool_calls"):
        #       for tc in msg["tool_calls"]:
        #           result = execute_tool(tc["function"]["name"], tc["function"]["arguments"])
        #           session.add_tool_result(tc["id"], result)
        #       continue  # 带着工具结果再次调用模型
        #   print(msg["content"])
        #   break
        print("(P1 未完成: 在 cli.py 中实现调用逻辑)")
        print()


if __name__ == "__main__":
    main()
