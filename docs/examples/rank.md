# 示例：获取热门内的综合热门

``` python
from bilibili_api import rank, sync

print(sync(rank.get_hot_videos()))
```

# 示例：获取全站排行榜

``` python
from bilibili_api import rank, sync

print(sync(rank.get_rank()))
```
