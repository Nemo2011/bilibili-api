# Module search.py

```python
from bilibili_api import search
```

各种杂类操作（主页搜索 API）

## class SearchObjectType

**Extends:** enum.Enum

搜索对象。

+ VIDEO : 视频
+ BANGUMI : 番剧
+ FT : 影视
+ LIVE : 直播
+ ARTICLE : 专栏
+ TOPIC : 话题
+ USER : 用户

## _async_ def web_search()

只指定关键字在 web 进行搜索，返回未经处理的字典

| name | type | description |
| ---- | ---- | ----------- |
| keyword | string | 搜索关键词 |
| page | int | 页数，defaults to 1 |

**Returns:** 调用 API 返回的结果

## _async_ def web_search_by_type()

指定关键字和类型进行搜索，返回未经处理的字典

| name | type | description |
| ---- | ---- | ----------- |
| keyword | string | 搜索关键词 |
| search_type | SearchObjectType | 搜索类别 |
| page | int | 页数，defaults to 1 |

**Returns:** 调用 API 返回的结果