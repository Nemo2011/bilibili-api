"""
bilibili_api.utils.sync

同步执行异步函数
"""

import asyncio
from asyncio.futures import Future as AsyncioFuture
from collections.abc import Coroutine
from concurrent.futures import Future as ConcurrentFuture
from concurrent.futures import ThreadPoolExecutor
from typing import Any, TypeVar

T = TypeVar("T")


def __ensure_event_loop() -> asyncio.AbstractEventLoop:
    try:
        asyncio.get_event_loop()
    except Exception:
        asyncio.set_event_loop(asyncio.new_event_loop())
    return asyncio.get_event_loop()


def sync(
    coroutine: Coroutine[Any, Any, T] | AsyncioFuture | ConcurrentFuture,
) -> T:
    """
    同步执行异步函数，使用可参考 [同步执行异步代码](https://nemo2011.github.io/bilibili-api/#/sync-executor)

    Args:
        obj (Coroutine | Future): 异步函数

    Returns:
        Any: 该异步函数的返回值
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return __ensure_event_loop().run_until_complete(coroutine)
    else:
        with ThreadPoolExecutor() as executor:
            return executor.submit(
                lambda x: __ensure_event_loop().run_until_complete(x), coroutine
            ).result()
