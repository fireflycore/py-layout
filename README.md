# py-layout

`py-layout` 是 Firefly Python 业务服务模板和集成样板。

当前状态是 MVP 骨架：用于验证 `firefly.micro`、`firefly.consul`、FastAPI、`grpc.aio`、SQLAlchemy、Redis、structlog 和 OTel 的标准装配口径。

它不是公共运行时包，`src/` 直接承载应用私有源码，语义上对应 `go-layout/internal/`。因此源码目录不再包一层 `firefly_app`。

```bash
uv sync
uv run pytest
PYTHONPATH=src uv run python -m app.main
```

本地开发期通过 `tool.uv.sources` 使用相邻的 `../py-micro` 和 `../py-consul`。真实业务服务或发布校验应改用 PyPI 上的 `firefly-micro` / `firefly-consul`。
