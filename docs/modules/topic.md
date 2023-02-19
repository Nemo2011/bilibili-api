# Module topic.md

``` python
from bilibili_api import topic
```

## class TopicCardsSortBy

**Extends:** enum.Enum

话题下内容排序方式。

+ NEW: 最新
+ HOT: 最热
+ RECOMMEND: 推荐

## async def get_hot_topics()

| name | type | description |
| - | - | - |
| numbers | int | 话题数量. Defaults to 33. |

获取动态页的火热话题

**Returns:** dict: 调用 API 返回的结果

## async def search_topic()

| name | type | description |
| - | - | - |
| keyword | str | 关键词 |
| pn | int | 页数. Defaults to 1. |
| ps | int | 数据数量. Defaults to 10. |

搜索话题

从动态页发布动态处的话题搜索框搜索话题

**Returns:** dict: 调用 API 返回的结果

---

## class Topic

### Attributes

| name | type | description |
| - | - | - |
| credential | Credential \| None | 凭据类 |

### Methods

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| topic_id | int | 话题 id |
| credential | Credential | 凭据类 |

#### def get_topic_id()

获取话题 id

**Returns:** int: 话题 id

#### async def get_info()

获取话题简介

**Returns:** dict: 调用 API 返回的结果

#### async def get_raw_cards()

| name | type | description |
| - | - | - |
| ps | int | 数据数量. Defaults to 100. |
| offset | int | 偏移量. 生成格式为 f'{页码}_{页码*数据量]}' 如'2_40'. Defaults to None |
| sort_by | TopicCardsSortBy | 排序方式. Defaults to TopicCardsSortBy.HOT. |

获取话题下的原始内容

未登录无法使用热门排序字段即 TopicCardsSortBy.RECOMMEND

**Returns:** dict: 调用 API 返回的结果

#### async def get_cards()

| name | type | description |
| - | - | - |
| ps | int | 数据数量. Defaults to 100. |
| offset | int | 偏移量. 生成格式为 f'{页码}_{页码*数据量]}' 如'2_40'. Defaults to None |
| sort_by | TopicCardsSortBy | 排序方式. Defaults to TopicCardsSortBy.HOT. |

获取话题下的内容

自动处理并转换成动态类

未登录无法使用热门排序字段即 TopicCardsSortBy.RECOMMEND

**Returns:** list: 内容列表

#### async def like()

| name | type | description |
| ---- | ---- | ----------- |
| status | bool | 状态. Defaults to True. |

设置点赞话题

**Returns:** dict: 调用 API 返回的结果

#### async def set_favorite()

| name | type | description |
| ---- | ---- | ----------- |
| status | bool | 状态. Defaults to True. |

设置收藏话题

**Returns:** dict: 调用 API 返回的结果
