"""py-layout 本地引导配置模型。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from firefly.consul import (
    AppConfig,
    ConsulConfig,
    KernelConfig,
    ServiceConfig,
    SidecarAgentConfig,
)
from firefly.micro.telemetry import TelemetryConfig
from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    """业务应用身份配置。"""

    id: str
    instance_id: str
    name: str
    env: str
    version: str
    secret: str = ""

    def to_firefly(self) -> AppConfig:
        # sidecar 注册 payload 使用 firefly.consul 的模型，避免 py-layout 自行维护两套契约。
        return AppConfig(
            id=self.id,
            instance_id=self.instance_id,
            name=self.name,
            env=self.env,
            version=self.version,
            secret=self.secret,
        )


class KernelSettings(BaseModel):
    """运行内核配置。"""

    language: str = "python"
    version: str = ""

    def to_firefly(self) -> KernelConfig:
        # KernelConfig 会进入 sidecar 注册 payload，字段名必须与 firefly.consul 对齐。
        return KernelConfig(language=self.language, version=self.version)


class ServiceSettings(BaseModel):
    """服务发现与注册配置。"""

    name: str
    namespace: str = "default"
    type: str = "svc"
    cluster_domain: str = "cluster.local"
    weight: int = 100

    def to_firefly(self) -> ServiceConfig:
        # ServiceConfig 只表达注册所需的服务发现事实，不携带运行端口。
        return ServiceConfig(
            name=self.name,
            namespace=self.namespace,
            type=self.type,
            cluster_domain=self.cluster_domain,
            weight=self.weight,
        )


class ServerSettings(BaseModel):
    """业务、HTTP 和 management 端口配置。"""

    host: str = "0.0.0.0"
    grpc_port: int = Field(default=50051, gt=0, le=65535)
    http_port: int = Field(default=8080, gt=0, le=65535)
    management_port: int = Field(default=15020, gt=0, le=65535)


class LoggerSettings(BaseModel):
    """结构化日志配置。"""

    level: str = "INFO"
    console: bool = True


class TelemetrySettings(BaseModel):
    """OTel resource 与开关配置。"""

    service_name: str
    service_version: str = ""
    environment: str = ""
    otlp_endpoint: str = ""
    traces: bool = True
    metrics: bool = True
    logs: bool = True
    resource_attributes: dict[str, str] = Field(default_factory=dict)

    def to_firefly(self) -> TelemetryConfig:
        # firefly.micro 当前只承接稳定 resource 字段，具体 provider 由 py-layout 装配。
        return TelemetryConfig(
            service_name=self.service_name,
            service_version=self.service_version,
            environment=self.environment,
            otlp_endpoint=self.otlp_endpoint,
            resource_attributes=dict(self.resource_attributes),
        )


class SidecarSettings(BaseModel):
    """本机 sidecar-agent 接入配置。"""

    base_url: str = "http://127.0.0.1:15010"
    watch_url: str = ""
    grace_period: str = ""
    request_timeout: float = 3.0
    reconnect_interval: float = 1.0
    gateway_manifest_path: str = "dep/protobuf/gen/gateway.manifest.json"

    def to_firefly(self) -> SidecarAgentConfig:
        # 先转成 firefly.consul 配置，再调用 normalized 统一默认值。
        return SidecarAgentConfig(
            base_url=self.base_url,
            watch_url=self.watch_url,
            grace_period=self.grace_period,
            request_timeout=self.request_timeout,
            reconnect_interval=self.reconnect_interval,
            gateway_manifest_path=self.gateway_manifest_path,
        ).normalized()


class BootstrapConfig(BaseModel):
    """py-layout 本地 bootstrap.json 完整模型。"""

    app: AppSettings
    service: ServiceSettings
    kernel: KernelSettings = Field(default_factory=KernelSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    logger: LoggerSettings = Field(default_factory=LoggerSettings)
    telemetry: TelemetrySettings
    sidecar: SidecarSettings = Field(default_factory=SidecarSettings)


class ConsulSettings(BaseModel):
    """conf/consul.json 配置模型。"""

    base_url: str = "http://127.0.0.1:8500"
    namespace: str = "config-center"
    timeout: float = 3.0
    watch_buffer: int = 8
    watch_wait_seconds: int = 60

    def to_firefly(self) -> ConsulConfig:
        # firefly.consul 使用 timedelta 表达 watch wait time，配置文件中保留易读秒数。
        return ConsulConfig(
            base_url=self.base_url,
            namespace=self.namespace,
            timeout=self.timeout,
            watch_buffer=self.watch_buffer,
            watch_wait_time=timedelta(seconds=self.watch_wait_seconds),
        )


@dataclass(slots=True)
class RuntimeIdentity:
    """组合 sidecar 注册所需的身份模型。"""

    app: AppConfig
    kernel: KernelConfig
    service: ServiceConfig
