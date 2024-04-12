"""
bilibili_api.utils.sync

同步执行异步函数
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Coroutine

def sync(coroutine: Coroutine) -> Any:
    """
    同步执行异步函数，使用可参考 [同步执行异步代码](https://nemo2011.github.io/bilibili-api/#/sync-executor)

    Args:
        coroutine (Coroutine): 执行协程函数所创建的协程对象

    Returns:
        该协程对象的返回值
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coroutine)
    else:
        with ThreadPoolExecutor() as executor:
            return executor.submit(asyncio.run, coroutine).result()
