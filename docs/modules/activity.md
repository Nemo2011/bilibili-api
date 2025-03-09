# Module activity.py


bilibili_api.activity

活动相关


``` python
from bilibili_api import activity
```

- [async def get\_activity\_aid()](#async-def-get\_activity\_aid)
- [async def get\_activity\_info()](#async-def-get\_activity\_info)
- [async def get\_activity\_list()](#async-def-get\_activity\_list)

---

## async def get_activity_aid()

获取部分活动存在的 aid，可用于获取评论


| name | type | description |
| - | - | - |
| `url` | `str` | 活动链接 |

**Returns:** `int`:  活动 aid，若活动无 aid 返回 -1




---

## async def get_activity_info()

获取活动详情


| name | type | description |
| - | - | - |
| `url` | `str` | 活动链接 |

**Returns:** `dict`:  活动详情




---

## async def get_activity_list()

获取活动列表


| name | type | description |
| - | - | - |
| `pn` | `int, optional` | 页数. Defaults to 1. |
| `ps` | `int, optional` | 每页数量. Defaults to 15. |

**Returns:** `dict`:  调用 API 返回的结果




