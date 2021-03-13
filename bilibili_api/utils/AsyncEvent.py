"""
bilibili_api.utils.AsyncEvent

发布-订阅模式异步事件类支持。
"""

from typing import Coroutine
import asyncio


class AsyncEvent:
    """
    发布-订阅模式异步事件类支持。
    """
    def __init__(self):
        self.__handlers = {}
        
    def add_event_listener(self, name: str, handler: Coroutine):
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
    
    def remove_event_listener(self, name: str, handler: Coroutine):
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

    def dispatch(self, name: str, *args, **kwargs):
        """
        异步发布事件。

        Args:
            name (str):       事件名。
            *args, **kwargs:  要传递给函数的参数。
        """
        name = name.upper()
        if name in self.__handlers:
            for coroutine in self.__handlers[name]:
                asyncio.create_task(coroutine(*args, **kwargs))
