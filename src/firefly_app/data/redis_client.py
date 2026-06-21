"""Redis 配置骨架。"""

from __future__ import annotations

from pydantic import BaseModel, Field


class RedisSettings(BaseModel):
    """Redis 连接配置。"""

    host: str = "127.0.0.1"
    port: int = Field(default=6379, gt=0, le=65535)
    database: int = Field(default=0, ge=0)
    username: str = ""
    password: str = ""
    decode_responses: bool = True
