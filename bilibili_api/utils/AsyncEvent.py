"""
bilibili_api.utils.AsyncEvent

发布-订阅模式异步事件类支持。
"""

import asyncio
import logging
from typing import Callable, Coroutine, Union


class AsyncEvent:
    """
    发布-订阅模式异步事件类支持。

    特殊事件：__ALL__ 所有事件均触发
    """

    def __init__(self):
        self.__handlers = {}
        self.__ignore_events = []
        self.__tasks = set()

    def add_event_listener(self, name: str, handler: Union[Callable, Coroutine]) -> None:
        """
        注册事件监听器。

        Args:
            name    (str)              :            事件名。
            handler (Union[Callable, Coroutine]):   回调函数。
        """
        name = name.upper()
        if name not in self.__handlers:
            self.__handlers[name] = []
        self.__handlers[name].append(handler)

    def on(self, event_name: str) -> Callable:
        """
        装饰器注册事件监听器。

        Args:
            event_name (str): 事件名。
        """

        def decorator(func: Union[Callable, Coroutine]):
            self.add_event_listener(event_name, func)
            return func

        return decorator

    def remove_all_event_listener(self) -> None:
        """
        移除所有事件监听函数
        """
        self.__handlers = {}

    def remove_event_listener(self, name: str, handler: Union[Callable, Coroutine]) -> bool:
        """
        移除事件监听函数。

        Args:
            name                  (str):            事件名。
            handler (Union[Callable, Coroutine]):   要移除的函数。

        Returns:
            bool: 是否移除成功。
        """
        name = name.upper()
        if name in self.__handlers:
            if handler in self.__handlers[name]:
                self.__handlers[name].remove(handler)
                return True
        return False

    def ignore_event(self, name: str) -> None:
        """
        忽略指定事件

        Args:
            name (str): 事件名。
        """
        name = name.upper()
        self.__ignore_events.append(name)

    def remove_ignore_events(self) -> None:
        """
        移除所有忽略事件
        """
        self.__ignore_events = []

    def __on_task_done(self, task: asyncio.Task) -> None:
        """
        asyncio.Task完成后的回调函数
        1、立刻从self.__tasks中移除任务
        2、如果任务抛出异常，装模做样处理下异常，避免Task exception was never retrieved
        """
        self.__tasks.discard(task)

        if task.cancelled(): return

        logger: logging.Logger | None = getattr(self, "logger", None)

        try:
            e = task.exception()
            if e and logger:
                logger.error(f"dispatched task raised an exception: {e}")
        except Exception:
            pass

    def dispatch(self, name: str, *args, **kwargs) -> None:
        """
        异步发布事件。

        Args:
            name (str):       事件名。
            *args, **kwargs (Any):  要传递给函数的参数。
        """
        if len(args) == 0 and len(kwargs.keys()) == 0:
            args = [{}]
        if name.upper() in self.__ignore_events:
            return

        name = name.upper()
        if name in self.__handlers:
            for callableorcoroutine in self.__handlers[name]:
                obj = callableorcoroutine(*args, **kwargs)
                if isinstance(obj, Coroutine):
                    task = asyncio.create_task(obj)
                    task.add_done_callback(self.__on_task_done)
                    self.__tasks.add(task) # 保持对task的引用状态

        if name != "__ALL__":
            kwargs.update({"name": name, "data": args})
            self.dispatch("__ALL__", kwargs)
