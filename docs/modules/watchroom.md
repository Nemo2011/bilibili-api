# Module `watchroom.py`

``` python
from bilibili_api import watchroom
```

---

## class SeasonType

**Extends: enum.Enum**

季度类型

+ ANIME: 番剧
+ MOVIE: 电影
+ DOCUMENTARY: 纪录片
+ GUOCHUANG: 国创
+ TV: 电视剧
+ VARIETY: 综艺

---

## class MessageType

**Extends: enum.Enum**

消息类型

+ PLAIN: 纯文本
+ EMOJI: 表情

---

## class MessageSegment

消息片段

### Attributes

| name | type | description |
| msg | str | 信息 |
| msg_type | MessageType | 信息类型 |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| msg | str | 信息 |
| is_emoji | bool | 是否为表情包 |

---

## class Message

消息集合

Ex: 

``` python
msg = Message("114514", MessageSegment("doge", True))
```

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| msg_list | List[MessageSegment \| str] | 消息列表 |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| *messages | MessageSegment \| str | 信息 |

---

## class WatchRoom

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类, defaults to Credential() |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| room_id | int | 放映室 id |
| credential | Credential | 凭据类, defaults to None. |

#### def get_room_id()

获取放映室 id

**Returns:** int: 放映室 id

#### def get_season_id()

获取番剧季节 id

**Returns:** int: 番剧季节 id

#### def get_episode_id()

获取番剧剧集 id

**Returns:** int: 番剧剧集 id

#### async def get_info()

获取放映室信息

**Returns:** dict: 调用 API 返回的结果

#### async def open()

开放放映室

**Returns:** None

#### async def close()

关闭放映室

**Returns:** None

#### async def progress()

| name | type | description |
| ---- | ---- | ----------- |
| progress | int, optional | 进度，单位为秒 |
| status | bool, optional | 播放状态 1 播放中 0 暂停中 2 已结束 |

设置播放状态，包括暂停与进度条

**Returns:** None

#### async def join()

| name | type | description |
| ---- | ---- | ----------- |
| token | str | 邀请 token |

加入放映室

**Returns:** dict: 调用 API 返回的结果

#### async def send()

| name | type | description |
| ---- | ---- | ----------- |
| msg | Message | 消息 |

发送消息

**Returns:** dict: 调用 API 返回的结果

#### async def kickout()

| name | type | description |
| ---- | ---- | ----------- |
| uid | int | 用户 uid |

踢出放映室

**Returns:** dict: 调用 API 返回的结果

#### async def share()

获取邀请 token

**Returns:** str: 邀请 token

---

## async def create()

| name | type | description |
| ---- | ---- | ----------- |
| season_id | int | 番剧季节 id |
| episode_id | int | 番剧剧集 id |
| is_open | bool | 是否公开 |
| credential | Credential | 凭据类 |

创建放映室

**Returns:** WatchRoom: 放映室

---

## async def match()

| name | type | description |
| ---- | ---- | ----------- |
| season_id | int | 番剧季节 id |
| episode_id | int | 番剧剧集 id |
| credential | Credential | 凭据类 |

匹配放映室

**Returns:** WatchRoom: 放映室
