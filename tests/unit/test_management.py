from __future__ import annotations

from fastapi.testclient import TestClient

from firefly_app.app.bootstrap import load_bootstrap_config
from firefly_app.server.management import create_management_app


def test_management_app_exposes_health_ready_info_and_metrics() -> None:
    config = load_bootstrap_config("conf/bootstrap.json")
    client = TestClient(create_management_app(config))

    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/ready").json() == {"status": "ready"}
    assert client.get("/info").json()["service"]["name"] == "firefly-python-demo"
    assert client.get("/metrics").status_code == 200
