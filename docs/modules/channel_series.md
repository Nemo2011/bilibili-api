# Module channel_series.py


bilibili_api.channel_series

用户合集与列表相关


``` python
from bilibili_api import channel_series
```

- [class ChannelOrder()](#class-ChannelOrder)
- [class ChannelSeries()](#class-ChannelSeries)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_meta()](#async-def-get\_meta)
  - [async def get\_videos()](#async-def-get\_videos)
- [class ChannelSeriesType()](#class-ChannelSeriesType)
- [async def add\_aids\_to\_series()](#async-def-add\_aids\_to\_series)
- [async def create\_channel\_series()](#async-def-create\_channel\_series)
- [async def del\_aids\_from\_series()](#async-def-del\_aids\_from\_series)
- [async def del\_channel\_series()](#async-def-del\_channel\_series)
- [async def set\_follow\_channel\_season()](#async-def-set\_follow\_channel\_season)

---

## class ChannelOrder()

**Extend: enum.Enum**

合集视频排序顺序。
+ DEFAULT: 默认排序
+ CHANGE : 升序排序




---

## class ChannelSeries()

合集与列表类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类. Defaults to None. |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `uid` | `int` | 用户 uid. Defaults to -1. |
| `type_` | `ChannelSeriesType` | 合集与列表类型. Defaults to ChannelSeriesType.SERIES. |
| `id_` | `int` | season_id 或 series_id. Defaults to -1. |
| `credential` | `Credential` | 凭证. Defaults to None. |


### async def get_meta()

获取元数据



**Returns:** `dict`:  调用 API 返回的结果




### async def get_videos()

获取合集视频

| name | type | description |
| - | - | - |
| `sort` | `ChannelOrder` | 排序方式 |
| `pn` | `int` | 页数，默认为 1 |
| `ps` | `int` | 每一页显示的视频数量 |

**Returns:** `dict`:  调用 API 返回的结果




---

## class ChannelSeriesType()

**Extend: enum.Enum**

合集与列表类型

+ SERIES: 相同视频分类
+ SEASON: 新概念多 P

**SEASON 类合集与列表名字为`合集·XXX`，请注意区别**




---

## async def add_aids_to_series()

添加视频至视频列表(旧版合集)


| name | type | description |
| - | - | - |
| `series_id` | `int` | 旧版合集 id。 |
| `aids` | `List[int]` | 视频 aid 列表。 |
| `credential` | `Credential` | 凭据类。 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def create_channel_series()

新建一个视频列表 (旧版合集)


| name | type | description |
| - | - | - |
| `name` | `str` | 列表名称。 |
| `aids` | `List[int]` | 要加入列表的视频的 aid 列表。 |
| `keywords` | `List[str]` | 列表的关键词。 |
| `description` | `str` | 列表的描述。 |
| `credential` | `Credential \| None` | 凭据类。 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def del_aids_from_series()

从视频列表(旧版合集)删除视频


| name | type | description |
| - | - | - |
| `series_id` | `int` | 旧版合集 id。 |
| `aids` | `List[int]` | 视频 aid 列表。 |
| `credential` | `Credential` | 凭据类。 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def del_channel_series()

删除视频列表(旧版合集)


| name | type | description |
| - | - | - |
| `series_id` | `int` | 旧版合集 id。 |
| `credential` | `Credential` | 凭据类。 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def set_follow_channel_season()

设置是否订阅合集(新版)


| name | type | description |
| - | - | - |
| `season_id` | `int` | 合集 id |
| `status` | `bool` | 是否订阅状态. Defaults to True. |




