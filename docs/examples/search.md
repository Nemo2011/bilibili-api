# 示例：获取搜索结果

```python
from bilibili_api import search, sync

print(sync(search.search("奥利给")))
```

# 示例：获取搜索结果（仅用户），`order_sort`指定0为从高到低，`order_type` 指定根据粉丝数目搜索

```python
from bilibili_api import search, sync

print(sync(
    search.search_by_type("音乐", search_type=search.SearchObjectType.USER, order_type=search.OrderUser.FANS,
                          order_sort=0)
))
```

# 示例：多条件搜索

搜索关键词为`小马宝莉`的`10-30分钟`之间`视频`，指定为 `MMD`分区，`第一页`,且使用一个`回调`来打印具体参数

> 分钟指定自动转换到指定区间，只在视频类型下生效 有四种：10分钟以下，10-30分钟，30-60分钟，60分钟以上

```python
from bilibili_api import search, sync, video_zone


async def test_f_search_by_order():
    return await search.search_by_type("小马宝莉", search_type=search.SearchObjectType.VIDEO,
                                       order_type=search.OrderVideo.SCORES, time_range=10,
                                       zone_type=video_zone.VideoZoneTypes.DOUGA_MMD, page=1, debug_param_func=print)


res = sync(test_f_search_by_order())
print(res)

```