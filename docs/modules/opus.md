# Module opus.py


bilibili_api.opus

图文相关


``` python
from bilibili_api import opus
```

- [class Opus()](#class-Opus)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def add\_coins()](#async-def-add\_coins)
  - [async def get\_images()](#async-def-get\_images)
  - [async def get\_images\_raw\_info()](#async-def-get\_images\_raw\_info)
  - [async def get\_info()](#async-def-get\_info)
  - [def get\_opus\_id()](#def-get\_opus\_id)
  - [async def get\_reaction()](#async-def-get\_reaction)
  - [async def get\_rid()](#async-def-get\_rid)
  - [async def is\_article()](#async-def-is\_article)
  - [async def markdown()](#async-def-markdown)
  - [async def set\_favorite()](#async-def-set\_favorite)
  - [async def set\_like()](#async-def-set\_like)
  - [async def turn\_to\_article()](#async-def-turn\_to\_article)
  - [def turn\_to\_dynamic()](#def-turn\_to\_dynamic)

---

## class Opus()

图文类。


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()





### async def add_coins()

给专栏投币，目前只能投一个



**Returns:** `dict`:  调用 API 返回的结果




### async def get_images()

获取图文所有图片并转为 Picture 类



**Returns:** `list`:  图片信息




### async def get_images_raw_info()

获取图文所有图片原始信息



**Returns:** `list`:  图片信息




### async def get_info()

获取图文基本信息



**Returns:** `dict`:  调用 API 返回的结果




### def get_opus_id()

获取图文 id



**Returns:** `int`:  图文 idd




### async def get_reaction()

获取点赞、转发


| name | type | description |
| - | - | - |
| `offset` | `str, optional` | 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to "" |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_rid()

获取 rid，以传入 `comment.get_comments_lazy` 等函数 oid 参数对评论区进行操作



**Returns:** `int`:  rid




### async def is_article()

获取图文是否同时为专栏

如果是，则专栏/图文/动态数据共享，可以投币



**Returns:** `bool`:  是否同时为专栏




### async def markdown()

将图文转为 markdown



**Returns:** `str`:  markdown 内容




### async def set_favorite()

设置图文收藏状态


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 收藏状态. Defaults to True |

**Returns:** `dict`:  调用 API 返回的结果




### async def set_like()

设置图文点赞状态


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 点赞状态. Defaults to True. |

**Returns:** `dict`:  调用 API 返回的结果




### async def turn_to_article()

对专栏图文，转换为专栏（评论、点赞等数据专栏/动态/图文共享）

如图文无对应专栏将报错。



**Returns:** `article.Article`:  专栏类




### def turn_to_dynamic()

转为动态

图文完全包含于动态，且图文与专栏 id 数值上一致，因此此函数绝对成功。



**Returns:** `dynamic.Dynamic`:  对应的动态类




