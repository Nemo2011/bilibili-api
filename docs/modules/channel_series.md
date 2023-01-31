# Module channel_series.py

``` python
from bilibili_api import channel_series
```

用户的合集与列表相关

## async def create_channel_series()

| name | type | description |
| - | - | - |
| name | str | 列表名称 |
| aids | List[int] | 要加入列表的视频的 aid 列表 |
| keywords | List[str] | 列表的关键词 |
| description | str | 列表的描述 |
| credential | Credential \| None | 凭据类 |

新建一个视频列表 (旧版合集)

**Returns:** dict: 调用 API 返回的结果

---

## async def del_channel_series()

| name | type | description |
| - | - | - |
| series_id | int | 旧版合集 id |
| credential | Credential | 凭据类 |

删除视频列表(旧版合集)

**Returns:** dict: 调用 API 返回的结果

---

## async def add_aids_to_series()

| name | type | description |
| - | - | - |
| series_id | int | 旧版合集 id |
| aids | List[int] | 视频 aid 列表 |
| credential | Credential | 凭据类 |

添加视频至视频列表(旧版合集)

**Returns:** dict: 调用 API 返回的结果

---

## async def del_aids_from_series()

| name | type | description |
| - | - | - |
| series_id | int | 旧版合集 id |
| aids | List[int] | 视频 aid 列表 |
| credential | Credential | 凭据类 |

从视频列表(旧版合集)删除视频

**Returns:** dict: 调用 API 返回的结果

---

## class ChannelSeries

合集与列表类

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| uid | int | 用户 uid |
| type_ | ChannelSeriesType | 合集与列表的类型，分旧版和新版 |
| id_ | int | season_id 或 series_id |
| credential | Credential \| None | 凭据类 |

#### def get_meta()

获取元数据

**Returns:** 调用接口返回的内容。

#### async def get_videos()

获取合集视频

**Returns:** 调用接口返回的内容。

---

## async def set_follow_channel_season()

设置是否订阅合集(新版)

| name | type | description |
| ---- | ---- | ----------- |
| season_id | int | 合集 id  |
| status | bool | 是否订阅状态. Defaults to True. |

**Returns:** dict: 调用 API 返回的结果
