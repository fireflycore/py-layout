"""Redis 配置适配层。"""

from __future__ import annotations

from firefly.redis import PoolConfig, RedisConfig, build_connection_kwargs, build_redis_url
from pydantic import BaseModel, Field


class RedisSettings(BaseModel):
    """py-layout 配置文件中的 Redis 连接配置。"""

    address: str = "127.0.0.1:6379"
    database: str | int = "0"
    username: str = ""
    password: str = ""
    decode_responses: bool = True
    max_open_connects: int = Field(default=100, ge=0)
    max_idle_connects: int = Field(default=10, ge=0)
    conn_max_life_time: int = Field(default=600, ge=0)

    def to_firefly(self) -> RedisConfig:
        """转换为 firefly.redis 的公共 Redis 配置。"""

        # py-layout 不再自己拼 redis 参数，只负责把配置文件字段转给公共包。
        return RedisConfig(
            address=self.address,
            database=self.database,
            username=self.username,
            password=self.password,
            decode_responses=self.decode_responses,
            pool=PoolConfig(
                max_open_connects=self.max_open_connects,
                max_idle_connects=self.max_idle_connects,
                conn_max_life_time=self.conn_max_life_time,
            ),
        )

    @property
    def host(self) -> str:
        """兼容旧测试读取 host，真实连接使用 address。"""

        # 只用于模板层展示和测试，连接参数以 firefly.redis 为准。
        return str(build_connection_kwargs(self.to_firefly())["host"])

    @property
    def port(self) -> int:
        """兼容旧测试读取 port，真实连接使用 address。"""

        # 只用于模板层展示和测试，连接参数以 firefly.redis 为准。
        return int(build_connection_kwargs(self.to_firefly())["port"])


def redis_url(settings: RedisSettings) -> str:
    """构造 Redis URL。"""

    # URL 拼装统一走 firefly.redis，模板层不维护第二套规则。
    return build_redis_url(settings.to_firefly())
