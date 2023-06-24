"""
bilibili_api.utils.AsyncEvent

发布-订阅模式异步事件类支持。
"""

from typing import Coroutine, Callable
import asyncio


class AsyncEvent:
    """
    发布-订阅模式异步事件类支持。

    特殊事件：__ALL__ 所有事件均触发
    """

    def __init__(self):
        self.__handlers = {}
        self.__ignore_events = []

    def add_event_listener(self, name: str, handler: Coroutine) -> None:
        """
        注册事件监听器。

        Args:
            name (str):            事件名。
            handler (Coroutine):   回调异步函数。
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

        def decorator(func: Coroutine):
            self.add_event_listener(event_name, func)
            return func

        return decorator

    def remove_all_event_listener(self) -> None:
        """
        移除所有事件监听函数
        """
        self.__handlers = {}

    def remove_event_listener(self, name: str, handler: Coroutine) -> bool:
        """
        移除事件监听函数。

        Args:
            name (str):            事件名。
            handler (Coroutine):   要移除的函数。

        Returns:
            bool, 是否移除成功。
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

    def dispatch(self, name: str, *args, **kwargs) -> None:
        """
        异步发布事件。

        Args:
            name (str):       事件名。
            *args, **kwargs:  要传递给函数的参数。
        """
        if len(args) == 0 and len(kwargs.keys()) == 0:
            args = [{}]
        if name.upper() in self.__ignore_events:
            return

        name = name.upper()
        if name in self.__handlers:
            for coroutine in self.__handlers[name]:
                asyncio.create_task(coroutine(*args, **kwargs))

        if name != "__ALL__":
            kwargs.update({"name": name, "data": args})
            self.dispatch("__ALL__", kwargs)
