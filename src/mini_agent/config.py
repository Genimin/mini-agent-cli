"""P0: 配置读取。

从环境变量 / .env 文件加载配置。
pydantic 只在这里使用（配置解析），其余模块保持纯标准库风格。
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Config(BaseModel):
    base_url: str = Field(description="OpenAI 兼容 API 的 base url，如 https://ai.hixx.cc:9898/v1")
    api_key: str = Field(description="API 密钥，sk- 开头")
    model: str = Field(default="hixx-txt", description="模型名")

    @property
    def chat_url(self) -> str:
        """完整 chat completions 端点。P1 会用到。"""
        return f"{self.base_url.rstrip('/')}/chat/completions"


def load_config() -> Config:
    """加载配置：先找项目根目录的 .env，再退回环境变量。

    TODO(P0): 实现加载逻辑
      1. Path(__file__).parents[2] 定位项目根目录
      2. load_dotenv(root / ".env")
      3. 从 os.environ 读取 MINI_AGENT_BASE_URL / MINI_AGENT_API_KEY / MINI_AGENT_MODEL
      4. 缺关键配置时抛出明确的中文报错（告诉用户先 cp .env.example .env）
    """
    raise NotImplementedError("P0: 请实现 load_config()")


def _env(name: str) -> str | None:
    """读环境变量的薄封装，方便测试时 monkeypatch。"""
    return os.environ.get(name)
