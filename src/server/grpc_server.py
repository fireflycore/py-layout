"""grpc.aio server 骨架。"""

from __future__ import annotations

import grpc


def create_grpc_server() -> grpc.aio.Server:
    """创建 grpc.aio Server。"""

    # 真实服务会在这里注册由 Buf 生成的 servicer；MVP 先保留可测试 server 工厂。
    return grpc.aio.server()
