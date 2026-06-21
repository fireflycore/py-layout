# py-layout

`py-layout` 是 Firefly Python 业务服务模板和集成样板。

当前状态是 MVP 骨架：用于验证 `firefly.micro`、`firefly.consul`、FastAPI、`grpc.aio`、SQLAlchemy、Redis、structlog 和 OTel 的标准装配口径。

```bash
uv sync
uv run pytest
```

本地开发期通过 `tool.uv.sources` 使用相邻的 `../py-micro` 和 `../py-consul`。真实业务服务或发布校验应改用 PyPI 上的 `firefly-micro` / `firefly-consul`。
