# 配置

```python
from bilibili_api import settings
```

## 代理

```python
settings.proxy = "" # 此处填写你的代理地址
```

## nest_asyncio

10.0.1 版本已经引入 nest_asyncio 以解决 asyncio 不支持事件嵌套。但是可能会造成一些后果。目前还没出现问题，官方也没有公布。<br>
如果想要禁用此功能，可以这么设置：

``` python
from bilibili_api import settings
settings.nest_asyncio = False
```

> 注意: 番剧示例中的第二个需要设置 nest_asyncio
