from __future__ import annotations

from firefly.orm import DatabaseConfig
from firefly.redis import RedisConfig

from data import DatabaseSettings, RedisSettings, build_async_database_url, redis_url


def test_database_url_uses_async_driver() -> None:
    settings = DatabaseSettings(database="demo", username="demo", password="secret")

    assert build_async_database_url(settings) == "mysql+asyncmy://demo:secret@127.0.0.1:3306/demo?charset=utf8mb4"
    assert isinstance(settings.to_firefly(), DatabaseConfig)


def test_redis_settings_defaults() -> None:
    settings = RedisSettings()

    assert settings.host == "127.0.0.1"
    assert settings.port == 6379
    assert settings.decode_responses is True
    assert isinstance(settings.to_firefly(), RedisConfig)
    assert redis_url(settings) == "redis://127.0.0.1:6379/0"
