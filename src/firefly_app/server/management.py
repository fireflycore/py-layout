"""management FastAPI app。"""

from __future__ import annotations

from fastapi import FastAPI
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from ..app.settings import BootstrapConfig


def create_management_app(config: BootstrapConfig) -> FastAPI:
    """创建 management 端口应用。"""

    app = FastAPI(title=f"{config.service.name} management")

    @app.get("/health")
    async def health() -> dict[str, str]:
        # health 只表达进程可响应，不要求 sidecar 或 service token 已就绪。
        return {"status": "ok"}

    @app.get("/ready")
    async def ready() -> dict[str, str]:
        # MVP 阶段 readiness 与 health 保持一致，后续会纳入 DB/Redis/sidecar 状态。
        return {"status": "ready"}

    @app.get("/info")
    async def info() -> dict[str, object]:
        # info 暴露低敏服务元信息，避免泄露 app secret、token 或 authority。
        return {
            "app": {
                "id": config.app.id,
                "instance_id": config.app.instance_id,
                "name": config.app.name,
                "env": config.app.env,
                "version": config.app.version,
            },
            "service": {
                "name": config.service.name,
                "namespace": config.service.namespace,
            },
            "telemetry": {
                "service_name": config.telemetry.service_name,
                "service_version": config.telemetry.service_version,
                "environment": config.telemetry.environment,
                "traces": config.telemetry.traces,
                "metrics": config.telemetry.metrics,
                "logs": config.telemetry.logs,
            },
        }

    @app.get("/metrics")
    async def metrics() -> Response:
        # Prometheus client 直接生成 scrape payload，后续会挂接 OTel / Prometheus provider。
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return app
