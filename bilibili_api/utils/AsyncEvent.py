"""
bilibili_api.utils.AsyncEvent

发布-订阅模式异步事件类支持。
"""

import asyncio
from collections.abc import Callable, Coroutine

tasks = set()


class AsyncEvent:
    """
    发布-订阅模式异步事件类支持。

    特殊事件：\\_\\_ALL\\_\\_ 所有事件均触发；\\_\\_TASK_EXCEPTION\\_\\_ 当订阅任务执行过程中抛出异常时发布的事件，不包含在 \\_\\_ALL\\_\\_ 中，订阅此事件的处理函数不再进行异常处理。
    """

    def __init__(self):
        """ """
        # don't remove this empty docstring
        self.__handlers = {}
        self.__ignore_events = []

    def add_event_listener(self, name: str, handler: Callable | Coroutine) -> None:
        """
        注册事件监听器。

        Args:
            name (str): 事件名。
            handler (Callable | Coroutine): 回调函数。
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

        Returns:
            Callable: 传入函数的参数字典
        """

        def decorator(func: Callable | Coroutine):
            self.add_event_listener(event_name, func)
            return func

        return decorator

    def remove_all_event_listener(self) -> None:
        """
        移除所有事件监听函数
        """
        self.__handlers = {}

    def remove_event_listener(self, name: str, handler: Callable | Coroutine) -> bool:
        """
        移除事件监听函数。

        Args:
            name (str): 事件名。
            handler (Callable | Coroutine): 要移除的函数。

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
        asyncio.Task 完成后的回调函数

        如果任务抛出异常，分发特殊异常事件，避免 `Task exception was never retrieved`
        """
        tasks.discard(task)

        if task.cancelled():
            return

        event_name = getattr(task, "event_name", None)

        try:
            e = task.exception()
        except Exception:
            return

        if e is None:
            return

        if event_name != "__TASK_EXCEPTION__":
            self.dispatch("__TASK_EXCEPTION__", e)
        else:
            raise e

    def dispatch(self, name: str, *args, **kwargs) -> None:
        """
        异步发布事件。

        Args:
            name (str): 事件名。
            args (Any): 要传递给函数的参数。 *args 传递。
            kwargs (Any): 要传递给函数的参数。 **kwargs 传递。
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
                    setattr(task, "event_name", name)
                    task.add_done_callback(self.__on_task_done)
                    tasks.add(task)

        if name != "__ALL__" and name != "__TASK_EXCEPTION__":
            kwargs.update({"name": name, "data": args})
            self.dispatch("__ALL__", kwargs)
