# 示例：获取搜索结果

``` python
from bilibili_api import search, sync

print(sync(search.search("奥利给")))
```

# 示例：获取搜索结果（仅用户）

``` python
from bilibili_api import search, sync

print(sync(
    search.search_by_type("bishi", search.SearchObjectType.USER)
))
```
