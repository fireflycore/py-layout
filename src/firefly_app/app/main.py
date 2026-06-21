"""py-layout 本地启动入口。"""

from __future__ import annotations

import asyncio

from .bootstrap import load_bootstrap_config, load_consul_config
from .lifecycle import create_runtime_resources


async def main() -> None:
    """加载配置并创建运行期资源。"""

    bootstrap = load_bootstrap_config()
    consul = load_consul_config()
    resources = await create_runtime_resources(bootstrap, consul)
    await resources.close()


if __name__ == "__main__":
    asyncio.run(main())
