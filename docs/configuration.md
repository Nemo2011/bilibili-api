# 配置

```python
from bilibili_api import settings
```

## 代理

```python
settings.proxy = "" # 此处填写你的代理地址
```

## nest_asyncio

10.0.1 版本已经引入 nest_asyncio 以解决 asyncio 不支持事件嵌套（放在 sync 函数，因为 sync 函数和其他的函数共用的事件循环。）这样子能在 sync 运行 async 函数时调用 sync。总之就是修复了一个写的时候出现的 bug<br>
如果想要禁用此功能，可以这么设置：

``` python
from bilibili_api import settings
settings.nest_asyncio = False
```

> 注意: 番剧示例中的第二个需要设置 nest_asyncio
