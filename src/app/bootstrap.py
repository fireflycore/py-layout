"""本地 bootstrap / consul 配置加载。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from .settings import BootstrapConfig, ConsulSettings

T = TypeVar("T", bound=BaseModel)


def load_bootstrap_config(path: str | Path = "conf/bootstrap.json") -> BootstrapConfig:
    """加载本地 bootstrap.json。"""

    return _load_json_model(Path(path), BootstrapConfig)


def load_consul_config(path: str | Path = "conf/consul.json") -> ConsulSettings:
    """加载本地 consul.json。"""

    return _load_json_model(Path(path), ConsulSettings)


def _load_json_model(path: Path, model: type[T]) -> T:
    # 配置文件固定按 UTF-8 JSON 读取，避免系统默认编码影响部署行为。
    raw = json.loads(path.read_text(encoding="utf-8"))
    # Pydantic 在边界处完成字段校验，后续装配层只处理强类型配置。
    return model.model_validate(raw)
