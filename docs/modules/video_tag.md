# Module video_tag.py

``` python
from bilibili_api import video_tag
```

视频标签相关，部分的标签的 id 与同名的频道的 id 一模一样。

## class Tag

标签类

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| tag_name | str \| None | 标签名. Defaults to None. |
| tag_id | int \| None | 标签 id. Defaults to None. |

**注意：tag_name 和 tag_id 任选一个传入即可。tag_id 优先使用。**

#### def get_tag_id()

获取标签 id

**Returns:** int: 标签 id

#### async def get_tag_info()

获取标签信息

**Returns:** dict: 调用 API 返回的结果

#### async def get_simulir_tags()

获取相关的标签

**Returns:** dict: 调用 API 返回的结果

#### async def get_cards()

获取标签下的视频/动态

**Returns:** dict: 调用 API 返回的结果
