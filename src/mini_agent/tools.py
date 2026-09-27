"""P4: 工具定义 + 本地执行。⭐ 整个项目的灵魂模块。

两个工具：
  1. calculator  —— 安全表达式求值（ast 实现，禁止 eval）
  2. get_weather —— 查询 wttr.in 天气

你要实现三件事：
  A. TOOLS_SCHEMA: 给模型看的 JSON Schema 声明（「schema 即提示」）
  B. execute_tool(): 本地执行分发器
  C. 工具执行错误时，返回能帮模型自我纠正的错误描述（错误信息是写给模型看的！）
"""

import ast
import json
import operator
from collections.abc import Callable

# ---------------------------------------------------------------- A. Schema

TOOLS_SCHEMA: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "计算一个数学表达式并返回结果。"
                "支持加減乘除、乘方(**)、括号、取余(%)。"
                "例如: (1 + 2) * 3"
            ),
            # TODO(P4): 补全 parameters 字段
            # {"type": "object", "properties": {"expression": {"type": "string", ...}}, "required": [...]}
        },
    }
    # TODO(P4): 追加 get_weather 的 schema（参数: city, string）
]

# ---------------------------------------------------------------- B. 执行器

_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    # TODO(P4): 需要的话补充 FloorDiv / USub（负号）等
}


def calculator(expression: str) -> str:
    """安全求值：只允许数字和 _SAFE_OPS 里的运算符。

    TODO(P4):
      1. ast.parse(expression, mode="eval") 得到语法树
      2. 递归求值：ast.BinOp → _eval(left) op _eval(right)；
         ast.UnaryOp(USub) → 取负；ast.Constant(number) → 直接返回
      3. 遇到任何其他节点类型（函数调用、变量名……）抛 ValueError
      4. 返回 str(result)，异常不用在这里捕获——交给 execute_tool 统一处理

    禁止使用 eval() / exec()。这是练习安全设计，真实 agent 的 shell 工具同理。
    """
    raise NotImplementedError("P4: 请实现 calculator()")


def get_weather(city: str) -> str:
    """查询 wttr.in。返回 json 字符串（截取关键字段更好）。

    TODO(P4):
      1. httpx.get(f"https://wttr.in/{city}", params={"format": "j1", "lang": "zh"}, timeout=15)
      2. 从 current_condition[0] 提取: temp_C, weatherDesc, humidity, windspeedKmph
      3. 返回紧凑的 json.dumps({...}, ensure_ascii=False)
      4. 网络失败时抛异常即可，execute_tool 会包装成模型可读的错误
    """
    raise NotImplementedError("P4: 请实现 get_weather()")


_TOOL_FUNCS: dict[str, Callable[..., str]] = {
    "calculator": calculator,
    "get_weather": get_weather,
}


def execute_tool(name: str, arguments_json: str) -> str:
    """执行分发器。永远返回 str（成功结果或错误描述），**不抛异常**。

    TODO(P4):
      1. name 不在 _TOOL_FUNCS → 返回 f"错误: 未知工具 {name}，可用工具: ..."
      2. json.loads(arguments_json) 失败 → 返回 "错误: 参数不是合法 JSON: ..."
      3. 用 **kwargs 调用函数；TypeError(参数不匹配) → 返回该工具的 schema 描述帮模型纠错
      4. 其他异常 → 返回 f"错误: 工具执行失败: {e}"

    设计要点：错误信息是写给模型看的。返回「参数不匹配，expression 应为字符串」
    模型下一轮就能自我纠正；返回「内部错误」它就只能瞎猜。
    """
    raise NotImplementedError("P4: 请实现 execute_tool()")
