"""py-layout 运行时生命周期骨架。"""

from __future__ import annotations

from dataclasses import dataclass

import structlog

from app.settings import BootstrapConfig, ConsulSettings
from runtime.logging import configure_logging


@dataclass(slots=True)
class RuntimeResources:
    """应用运行期资源句柄。"""

    bootstrap: BootstrapConfig
    consul: ConsulSettings
    logger: structlog.stdlib.BoundLogger

    async def close(self) -> None:
        """关闭运行期资源。"""

        # MVP 阶段还没有打开真实 DB/Redis/sidecar 连接，这里先保留统一关闭入口。
        self.logger.info("runtime_resources_closed")


async def create_runtime_resources(bootstrap: BootstrapConfig, consul: ConsulSettings) -> RuntimeResources:
    """创建 py-layout 运行期资源。"""

    configure_logging(bootstrap.logger.level)
    logger = structlog.get_logger("py_layout").bind(
        service_name=bootstrap.service.name,
        service_instance_id=bootstrap.app.instance_id,
    )
    logger.info("runtime_resources_created", consul_base_url=consul.base_url)
    return RuntimeResources(bootstrap=bootstrap, consul=consul, logger=logger)
