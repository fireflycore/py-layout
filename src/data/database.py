"""数据库配置适配层。"""

from __future__ import annotations

from firefly.orm import DatabaseConfig, DatabaseType, PoolConfig, build_async_database_url as _build_async_database_url
from pydantic import BaseModel, Field


class DatabaseSettings(BaseModel):
    """py-layout 配置文件中的关系数据库配置。"""

    type: str = "mysql"
    address: str = "127.0.0.1:3306"
    database: str
    username: str
    password: str = ""
    driver: str = ""
    max_open_connects: int = Field(default=100, ge=0)
    max_idle_connects: int = Field(default=10, ge=0)
    conn_max_life_time: int = Field(default=600, ge=0)

    def to_firefly(self) -> DatabaseConfig:
        """转换为 firefly.orm 的公共数据库配置。"""

        # py-layout 只负责配置文件形态，连接 URL 与 pool 语义交给 firefly.orm。
        return DatabaseConfig(
            type=_database_type(self.type),
            address=self.address,
            database=self.database,
            username=self.username,
            password=self.password,
            driver=self.driver,
            pool=PoolConfig(
                max_open_connects=self.max_open_connects,
                max_idle_connects=self.max_idle_connects,
                conn_max_life_time=self.conn_max_life_time,
            ),
        )


def build_async_database_url(settings: DatabaseSettings) -> str:
    """构造 SQLAlchemy async database URL。"""

    # URL 拼装统一走 firefly.orm，避免模板层和公共包规则漂移。
    return _build_async_database_url(settings.to_firefly())


def _database_type(value: str) -> DatabaseType:
    # 配置文件允许写 mysql/postgres/postgresql，转换为 firefly.orm 的枚举。
    normalized = value.strip().lower()
    if normalized == "mysql":
        return DatabaseType.MYSQL
    if normalized in {"postgres", "postgresql"}:
        return DatabaseType.POSTGRES
    raise ValueError(f"unsupported database type: {value}")
