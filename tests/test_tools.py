"""P5: 工具层单元测试。uv run pytest 运行（需先 uv add --dev pytest）。"""

import pytest

from mini_agent.tools import calculator, execute_tool


class TestCalculator:
    """正常用例"""

    def test_basic_ops(self):
        assert calculator("1 + 2") == "3"
        assert calculator("(1 + 2) * 3") == "9"
        assert calculator("2 ** 10") == "1024"
        assert calculator("10 % 3") == "1"

    def test_float(self):
        assert calculator("1 / 3") == "0.3333333333333333"

    def test_negative(self):
        assert calculator("-5 + 3") == "-2"


class TestCalculatorSafety:
    """安全用例：恶意输入必须被拒绝（抛异常），不许碰 eval"""

    def test_reject_function_call(self):
        with pytest.raises(ValueError):
            calculator("__import__('os').system('dir')")

    def test_reject_variable(self):
        with pytest.raises(ValueError):
            calculator("os.getcwd()")

    def test_reject_name(self):
        with pytest.raises(ValueError):
            calculator("x + 1")

    def test_reject_empty(self):
        with pytest.raises(Exception):
            calculator("")


class TestExecuteTool:
    """错误信息要写给模型看：可读、可纠错"""

    def test_unknown_tool(self):
        result = execute_tool("no_such_tool", "{}")
        assert result.startswith("错误")
        assert "calculator" in result  # 应列出可用工具

    def test_bad_json(self):
        result = execute_tool("calculator", "not-json{{")
        assert "JSON" in result

    def test_bad_args(self):
        result = execute_tool("calculator", '{"expression": 123}')
        assert "错误" in result

    def test_success_path(self):
        assert execute_tool("calculator", '{"expression": "1+1"}') == "2"
