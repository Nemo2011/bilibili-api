# Module session.py

```python
from bilibili_api import session
```

消息相关。

#### async def fetch_session_msgs()

| name         | type          | description                      |
| ------------ | ------------- | -------------------------------- |
| talker_id    | int           | 用户 UID                         |
| credential   | Credential    | 凭证                             |
| session_type | int, optional | 会话类型 1 私聊 2 应援团          |
| begin_seqno  | int, optional | 起始 Seqno，每条信息有自己的Seqno |

获取指定用户的近三十条消息

**Returns:** dict: 调用 API 返回结果

#### async def new_sessions()

| name       | type          | description |
| ---------- | ------------- | ----------- |
| credential | Credential    | 凭证        |
| begin_ts   | int, optional | 起始时间戳  |

获取新消息

**Returns:** dict: 调用 API 返回结果

#### async def get_sessions()

| name         | type          | description                                 |
| ------------ | ------------- | ------------------------------------------- |
| credential   | Credential    | 凭证                                        |
| session_type | int, optional | 会话类型 1: 私聊, 2: 通知, 3: 应援团, 4: 全部 |

获取已有消息

**Returns:** dict: 调用 API 返回结果

#### async def get_session_detail()

| name         | type          | description                                 |
| ------------ | ------------- | ------------------------------------------- |
| credential   | Credential    | 凭证                                        |
| session_type | int, optional | 会话类型                                     |
| talker_id    | int           | 对话人 UID                                   |

获取指定会话的详细信息

**Returns:** dict: 调用 API 返回结果

#### async def send_msg()

| name        | type          | description |
| ----------- | ------------- | ----------- |
| credential  | Credential    | 凭证        |
| receiver_id | int           | 接收者 UID  |
| msg_type    | EventType     | 信息类型    |
| content     | str 或 Picture | 信息内容。  |

给用户发送私聊信息。目前支持纯文本、图片、撤回。

**Returns:** dict: 调用 API 返回结果

---

#### async def get_likes()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类 |

获取收到的点赞。

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_unread_messages()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类 |

获取未读的信息

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_replies()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类 |

获取收到的回复

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_system_messages()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类 |

获取系统信息

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_at()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类 |
| last_id | int, optional | 最后一个 ID |
| at_time | int, optional | 最后一个点赞发送时间 |

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_session_settings()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类 |

获取消息设置

**Returns:** dict: 调用 API 返回的结果

---

## class Event

消息类，定义有各种消息类型，并可将 json 传换成字符串

**消息参数:**

+ receiver_id:   收信人 UID
+ receiver_type: 收信人类型，1: 私聊, 2: 应援团通知, 3: 应援团
+ sender_uid:    发送人 UID
+ talker_id:     对话人 UID
+ msg_seqno:     事件 Seqno
+ msg_type:      事件类型
+ msg_key:       事件唯一编号
+ timestamp:     事件时间戳
+ content:       事件内容


## class EventType

**Extends:** enum.Enum

消息类型

+ TEXT:           纯文字消息
+ PICTURE:        图片消息
+ WITHDRAW:       撤回消息
+ GROUPS_PICTURE: 应援团图片
+ SHARE_VIDEO:    分享视频
+ NOTICE:         系统通知
+ PUSHED_VIDEO:   UP主推送的视频
+ WELCOME:        新成员加入应援团欢迎

### Functions

#### def \_\_init\_\_()

| name     | type | description         |
| -------- | ---- | ------------------- |
| data     | dict | 接收到的事件详细信息 |
| self_uid | int  | 用户自身 UID        |

#### def \_\_str\_\_()

信息概述

**Returns:** 信息的字符串形式

#### def \_\_content()

格式化信息，将信息内容转换为数字、文本、Video对象或Picture对象。

---

## class Session

**Extends:** bilibili_api.utils.AsyncEvent.AsyncEvent

会话类，用来开启消息监听。

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

### Functions

#### def \_\_init\_\_()

| name       | type           | description |
| ---------- | -------------- | ----------- |
| credential | Credential     | 凭证        |
| debug      | bool, optional | 日志等级    |

#### def get_status()

获取连接状态

**Returns:** int: 0 初始化，1 已连接，2 断开连接中，3 已断开，4 错误

#### async def run()

| name        | type           | description                  |
| ----------- | -------------- | ---------------------------- |
| except_self | bool, optional | 是否排除自己发出的消息，默认是 |

不阻塞开始轮询

#### async def start()

| name        | type           | description                  |
| ----------- | -------------- | ---------------------------- |
| except_self | bool, optional | 是否排除自己发出的消息，默认是 |

阻塞开始轮询

#### async def reply()

| name    | type  | description |
| ------- | ----- | ----------- |
| event   | Event | 要回复的消息 |
| content | str 或 Picture | 回复文字或图片 |

快速回复

**Returns:** dict: 调用接口返回的内容。

#### def close()

结束轮询
