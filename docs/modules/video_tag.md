# Module video_tag.py


bilibili_api.video_tag

视频标签相关，部分的标签的 id 与同名的频道的 id 一模一样。


``` python
from bilibili_api import video_tag
```

- [class Tag()](#class-Tag)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_similar\_tags()](#async-def-get\_similar\_tags)
  - [async def get\_tag\_id()](#async-def-get\_tag\_id)
  - [async def get\_tag\_info()](#async-def-get\_tag\_info)
  - [async def get\_tag\_name()](#async-def-get\_tag\_name)
  - [async def subscribe\_tag()](#async-def-subscribe\_tag)
  - [async def unsubscribe\_tag()](#async-def-unsubscribe\_tag)

---

## class Tag()

标签类




### def \_\_init\_\_()

注意：tag_name 和 tag_id 任选一个传入即可。tag_id 优先。


| name | type | description |
| - | - | - |
| `tag_name` | `str \| None` | 标签名. Defaults to None. |
| `tag_id` | `int \| None` | 标签 id. Defaults to None. |
| `credential` | `Credential` | 凭据类. Defaults to None. |


### async def get_similar_tags()

获取相关的标签



**Returns:** `dict`:  调用 API 返回的结果




### async def get_tag_id()

获取标签 id



**Returns:** `int`:  标签 id




### async def get_tag_info()

获取标签信息。



**Returns:** `dict`:  调用 API 返回的结果




### async def get_tag_name()

获取标签名



**Returns:** `str`:  标签名




### async def subscribe_tag()

关注标签。



**Returns:** `dict`:  调用 API 返回的结果。




### async def unsubscribe_tag()

取关标签。



**Returns:** `dict`:  调用 API 返回的结果。




