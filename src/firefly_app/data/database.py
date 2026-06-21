"""SQLAlchemy 数据库配置骨架。"""

from __future__ import annotations

from pydantic import BaseModel, Field


class DatabaseSettings(BaseModel):
    """关系数据库配置。"""

    driver: str = "mysql+asyncmy"
    host: str = "127.0.0.1"
    port: int = Field(default=3306, gt=0, le=65535)
    database: str
    username: str
    password: str = ""
    echo: bool = False


def build_async_database_url(settings: DatabaseSettings) -> str:
    """构造 SQLAlchemy async database URL。"""

    # URL 只在连接工厂内部使用，日志中不得输出包含 password 的完整字符串。
    auth = settings.username if not settings.password else f"{settings.username}:{settings.password}"
    return f"{settings.driver}://{auth}@{settings.host}:{settings.port}/{settings.database}"
