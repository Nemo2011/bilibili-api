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

搜索关键词为`小马宝莉`的`30-60分钟`之间`视频`，指定为 `MMD`分区，`第二页`

```python
async def test_f_search_by_order():
    return await search.search_by_type("小马宝莉", search_type=search.SearchObjectType.VIDEO,
                                       order_type=search.OrderVideo.SCORES, time_range=50,
                                       topic_type=search.TopicType.AnimeMMD, page=2)

```