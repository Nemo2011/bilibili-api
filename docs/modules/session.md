# Module session.py


bilibili_api.session

消息相关


``` python
from bilibili_api import session
```

- [class Event()](#class-Event)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
- [class EventType()](#class-EventType)
- [class Session()](#class-Session)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def close()](#def-close)
  - [def get\_status()](#def-get\_status)
  - [def on()](#def-on)
  - [async def reply()](#async-def-reply)
  - [async def run()](#async-def-run)
  - [async def start()](#async-def-start)
- [async def fetch\_session\_msgs()](#async-def-fetch\_session\_msgs)
- [async def get\_at()](#async-def-get\_at)
- [async def get\_likes()](#async-def-get\_likes)
- [async def get\_replies()](#async-def-get\_replies)
- [async def get\_session\_detail()](#async-def-get\_session\_detail)
- [async def get\_session\_settings()](#async-def-get\_session\_settings)
- [async def get\_sessions()](#async-def-get\_sessions)
- [async def get\_system\_messages()](#async-def-get\_system\_messages)
- [async def get\_unread\_messages()](#async-def-get\_unread\_messages)
- [async def new\_sessions()](#async-def-new\_sessions)
- [async def send\_msg()](#async-def-send\_msg)

---

## class Event()

事件参数:
+ receiver_id:   收信人 UID
+ receiver_type: 收信人类型，1: 私聊, 2: 应援团通知, 3: 应援团
+ sender_uid:发送人 UID
+ talker_id: 对话人 UID
+ msg_seqno: 事件 Seqno
+ msg_type:  事件类型
+ msg_key:   事件唯一编号
+ timestamp: 事件时间戳
+ content:   事件内容




### def \_\_init\_\_()

信息事件类型


| name | type | description |
| - | - | - |
| `data` | `Dict` | 接收到的事件详细信息 |
| `self_uid` | `int` | 用户自身 UID |


---

## class EventType()

**Extend: enum.Enum**

事件类型

- TEXT:   纯文字消息
- PICTURE:图片消息
- WITHDRAW:   撤回消息
- GROUPS_PICTURE: 应援团图片，但似乎不常触发，一般使用 PICTURE 即可
- SHARE_VIDEO:分享视频
- NOTICE: 系统通知
- PUSHED_VIDEO:   UP主推送的视频
- WELCOME:新成员加入应援团欢迎




---

## class Session()

**Extend: bilibili_api.utils.AsyncEvent.AsyncEvent**

会话类，用来开启消息监听。




### def \_\_init\_\_()





### def close()

结束轮询





### def get_status()

获取连接状态



**Returns:** `int`:  0 初始化，1 已连接，2 断开连接中，3 已断开，4 错误




### def on()

重载装饰器注册事件监听器


| name | type | description |
| - | - | - |
| `event_type` | `EventType` | 事件类型 |




### async def reply()

快速回复消息


| name | type | description |
| - | - | - |
| `event` | `Event` | 要回复的消息 |
| `content` | `str \| Picture` | 要回复的文字内容 |

**Returns:** `dict`:  调用接口返回的内容。




### async def run()

非阻塞异步爬虫 定时发送请求获取消息


| name | type | description |
| - | - | - |
| `exclude_self` | `bool` | 是否排除自己发出的消息，默认排除 |




### async def start()

阻塞异步启动 通过调用 self.close() 后可断开连接


| name | type | description |
| - | - | - |
| `exclude_self` | `bool` | 是否排除自己发出的消息，默认排除 |




---

## async def fetch_session_msgs()

获取指定用户的近三十条消息


| name | type | description |
| - | - | - |
| `talker_id` | `int` | 用户 UID |
| `credential` | `Credential` | Credential |
| `session_type` | `int` | 会话类型 1 私聊 2 应援团 |
| `begin_seqno` | `int` | 起始 Seqno |

**Returns:** `dict`:  调用 API 返回结果




---

## async def get_at()

获取收到的 AT


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类. |
| `last_id` | `Optional, int` | 最后一个 ID |
| `at_time` | `Optional, int` | 最后一个点赞发送时间 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_likes()

获取收到的赞


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类. |
| `last_id` | `Optional, int` | 最后一个 ID |
| `like_time` | `Optional, int` | 最后一个点赞发送时间 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_replies()

获取收到的回复


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类. |
| `last_reply_id` | `Optional, int` | 最后一个评论的 ID |
| `reply_time` | `Optional, int` | 最后一个评论发送时间 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_session_detail()

获取会话详情


| name | type | description |
| - | - | - |
| `credential` | `Credential` | Credential |
| `session_type` | `int` | 会话类型 |
| `talker_id` | `int` | 会话对象的UID |

**Returns:** `dict`:  调用 API 返回结果




---

## async def get_session_settings()

获取消息设置


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_sessions()

获取已有消息


| name | type | description |
| - | - | - |
| `credential` | `Credential` | Credential |
| `session_type` | `int` | 会话类型 1 |

**Returns:** `dict`:  调用 API 返回结果




---

## async def get_system_messages()

获取系统信息


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_unread_messages()

获取未读的信息


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def new_sessions()

获取新消息


| name | type | description |
| - | - | - |
| `credential` | `Credential` | Credential |
| `begin_ts` | `int` | 起始时间戳 |

**Returns:** `dict`:  调用 API 返回结果




---

## async def send_msg()

给用户发送私聊信息。目前仅支持纯文本。

调用 API 需要发送者用户的 UID，可将此携带在凭据类的 DedeUserID 字段，不携带模块将自动获取对应 UID。


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭证 |
| `receiver_id` | `int` | 接收者 UID |
| `msg_type` | `EventType` | 信息类型，参考 Event 类的事件类型。 |
| `content` | `str \| Picture` | 信息内容。支持文字和图片。 |

**Returns:** `dict`:  调用 API 返回结果




