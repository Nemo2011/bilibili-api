# 同步执行异步代码

考虑到有部分开发者有需要写同步代码的需求，亦或是简单的逻辑不想用异步，这里提供了一个很方便的异步转同步代码，使用方法如下：

```python
from bilibili_api import sync, video

v = video.Video('BV1GK4y1V7HP')

print(sync(v.get_info()))

print(sync(v.get_download_url(0)))
```

使用 `sync()` 来包装异步代码，按照上述代码格式写即可实现同步运行。

原理其实也很简单，`sync()` 代码如下：

```python
from typing import Coroutine
import asyncio
import nest_asyncio
from .. import settings


def __ensure_event_loop():
    try:
        asyncio.get_event_loop()

    except:
        asyncio.set_event_loop(asyncio.new_event_loop())


def sync(coroutine: Coroutine):
    """
    同步执行异步函数，使用可参考 [同步执行异步代码](https://nemo2011.github.io/bilibili-api/#/sync-executor)

    Args:
        coroutine (Coroutine): 异步函数

    Returns:
        该异步函数的返回值
    """
    if settings.nest_asyncio == True:
        nest_asyncio.apply()
    __ensure_event_loop()
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine)

```