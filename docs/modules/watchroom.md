# Module watchroom.py


bilibili_api.watchroom

放映室相关 API

注意，此类操作务必传入 `Credential` 并且要求传入 `buvid3` 否则可能无法鉴权


``` python
from bilibili_api import watchroom
```

- [class Message()](#class-Message)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
- [class MessageSegment()](#class-MessageSegment)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
- [class MessageType()](#class-MessageType)
- [class SeasonType()](#class-SeasonType)
- [class WatchRoom()](#class-WatchRoom)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def close()](#async-def-close)
  - [async def get\_episode\_id()](#async-def-get\_episode\_id)
  - [async def get\_info()](#async-def-get\_info)
  - [def get\_room\_id()](#def-get\_room\_id)
  - [async def get\_season\_id()](#async-def-get\_season\_id)
  - [async def join()](#async-def-join)
  - [async def kickout()](#async-def-kickout)
  - [async def open()](#async-def-open)
  - [async def progress()](#async-def-progress)
  - [async def send()](#async-def-send)
  - [def set\_episode\_id()](#def-set\_episode\_id)
  - [def set\_season\_id()](#def-set\_season\_id)
  - [async def share()](#async-def-share)
- [async def create()](#async-def-create)
- [async def match()](#async-def-match)

---

## class Message()

消息集合




### def \_\_init\_\_()





---

## class MessageSegment()

消息片段


| name | type | description |
| - | - | - |
| `msg` | `str` | 信息 |
| `is_emoji` | `bool` | 是否为表情包 |


### def \_\_init\_\_()





---

## class MessageType()

**Extend: enum.Enum**

消息类型

+ PLAIN: 纯文本
+ EMOJI: 表情




---

## class SeasonType()

**Extend: enum.Enum**

季度类型

+ ANIME: 番剧
+ MOVIE: 电影
+ DOCUMENTARY: 纪录片
+ GUOCHUANG: 国创
+ TV: 电视剧
+ VARIETY: 综艺




---

## class WatchRoom()

放映室类




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 (大部分用户操作都需要与之匹配的 buvid3 值，务必在 credential 传入) |
| `room_id` | `int` | 放映室 id |


### async def close()

关闭放映室






### async def get_episode_id()

获取番剧剧集 id



**Returns:** `int`:  番剧剧集 id




### async def get_info()

获取放映室信息，播放进度等



**Returns:** `dict`:  调用 API 返回的结果




### def get_room_id()

获取放映室 id



**Returns:** `int`:  放映室 id




### async def get_season_id()

获取番剧季度 id



**Returns:** `int`:  番剧季度 id




### async def join()

加入放映室


| name | type | description |
| - | - | - |
| `token` | `str, Optional` | 邀请 Token |

**Returns:** `dict`:  调用 API 返回的结果




### async def kickout()

踢出放映室


| name | type | description |
| - | - | - |
| `uid` | `int` | 用户 uid |

**Returns:** `dict`:  调用 API 返回的结果




### async def open()

开放放映室






### async def progress()

设置播放状态，包括暂停与进度条


| name | type | description |
| - | - | - |
| `progress` | `int, None` | 进度，单位为秒 |
| `status` | `bool, None` | 播放状态 1 播放中 0 暂停中 2 已结束 |




### async def send()

发送消息


| name | type | description |
| - | - | - |
| `msg` | `Message` | 消息 |

**Returns:** `dict`:  调用 API 返回的结果




### def set_episode_id()

设置番剧剧集 id


| name | type | description |
| - | - | - |
| `episode_id` | `int` | 番剧剧集 id |




### def set_season_id()

设置番剧季度 id


| name | type | description |
| - | - | - |
| `season_id` | `int` | 季度 id |




### async def share()

获取邀请 Token



**Returns:** `str`:  邀请 Token




---

## async def create()

创建放映室


| name | type | description |
| - | - | - |
| `season_id` | `int` | 每季度的 ID |
| `ep_id` | `int` | 剧集 ID |
| `is_open` | `bool` | 是否公开 |
| `credential` | `Credential` | 凭据 |

**Returns:** `Watchroom`:  放映室




---

## async def match()

匹配放映室


| name | type | description |
| - | - | - |
| `season_id` | `int` | 季度 ID |
| `season_type` | `str` | 季度类型 |

**Returns:** `Watchroom`:  放映室




