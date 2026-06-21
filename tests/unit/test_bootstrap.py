from __future__ import annotations

from pathlib import Path

from firefly.consul import ConsulConfig
from firefly.micro.telemetry import TelemetryConfig

from firefly_app.app.bootstrap import load_bootstrap_config, load_consul_config


def test_load_bootstrap_config() -> None:
    config = load_bootstrap_config(Path("conf/bootstrap.json"))

    assert config.app.id == "demo-app"
    assert config.service.name == "firefly-python-demo"
    assert config.telemetry.to_firefly().resource()["service.name"] == "firefly-python-demo"
    assert isinstance(config.telemetry.to_firefly(), TelemetryConfig)


def test_load_consul_config() -> None:
    config = load_consul_config(Path("conf/consul.json"))

    assert config.base_url == "http://127.0.0.1:8500"
    assert isinstance(config.to_firefly(), ConsulConfig)
