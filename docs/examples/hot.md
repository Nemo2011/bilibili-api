# 示例：获取热门内的综合热门

``` python
from bilibili_api import hot, sync

print(sync(hot.get_hot_videos()))
```

# 示例：获取热词图鉴

``` python
from bilibili_api import hot, sync

print(sync(hot.get_hot_buzzwords()))
```
