# Module topic.py


bilibili_api.topic

话题相关


``` python
from bilibili_api import topic
```

- [class Topic()](#class-Topic)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_cards()](#async-def-get\_cards)
  - [async def get\_info()](#async-def-get\_info)
  - [def get\_topic\_id()](#def-get\_topic\_id)
  - [async def like()](#async-def-like)
  - [async def set\_favorite()](#async-def-set\_favorite)
- [class TopicCardsSortBy()](#class-TopicCardsSortBy)
- [async def get\_hot\_topics()](#async-def-get\_hot\_topics)
- [async def search\_topic()](#async-def-search\_topic)

---

## class Topic()

话题类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `topic_id` | `int` | 话题 id |
| `credential` | `Credential` | 凭据类 |


### async def get_cards()

获取话题下的内容

未登录无法使用热门排序字段即 TopicCardsSortBy.RECOMMEND


| name | type | description |
| - | - | - |
| `ps` | `int` | 数据数量. Defaults to 100. |
| `offset` | `Optional, str` | 偏移量. 生成格式为 f'{页码}_{页码*数据量]}' 如'2_40' Defaults to None. |
| `sort_by` | `TopicCardsSortBy` | 排序方式. Defaults to TopicCardsSortBy.HOT. |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_info()

获取话题简介



**Returns:** `dict`:  调用 API 返回的结果




### def get_topic_id()

获取话题 id



**Returns:** `int`:  话题 id




### async def like()

设置点赞话题


| name | type | description |
| - | - | - |
| `status` | `bool` | 是否设置点赞. Defaults to True. |

**Returns:** `dict`:  调用 API 返回的结果




### async def set_favorite()

设置收藏话题


| name | type | description |
| - | - | - |
| `status` | `bool` | 是否设置收藏. Defaults to True. |

**Returns:** `dict`:  调用 API 返回的结果




---

## class TopicCardsSortBy()

**Extend: enum.Enum**

话题下内容排序方式

+ NEW: 最新
+ HOT: 最热
+ RECOMMEND: 推荐




---

## async def get_hot_topics()

获取动态页的火热话题


| name | type | description |
| - | - | - |
| `numbers` | `int` | 话题数量. Defaults to 33. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def search_topic()

搜索话题

从动态页发布动态处的话题搜索框搜索话题


| name | type | description |
| - | - | - |
| `keyword` | `str` | 搜索关键词 |
| `ps` | `int` | 每页数量. Defaults to 20. |
| `pn` | `int` | 页数. Defaults to 1. |

**Returns:** `dict`:  调用 API 返回的结果




