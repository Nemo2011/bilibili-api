from typing import Coroutine
import asyncio


def sync(coroutine: Coroutine):
    """
    同步执行异步函数，使用可参考 [同步执行异步代码](https://www.passkou.com/bilibili-api/#/sync-executor)

    Args:
        coroutine (Coroutine): 异步函数

    Returns:
        该异步函数的返回值
    """
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine)

