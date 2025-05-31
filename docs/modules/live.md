# Module live.py


bilibili_api.live

直播相关


``` python
from bilibili_api import live
```

- [class LiveCodec()](#class-LiveCodec)
- [class LiveDanmaku()](#class-LiveDanmaku)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def connect()](#async-def-connect)
  - [async def disconnect()](#async-def-disconnect)
  - [def get\_live\_room()](#def-get\_live\_room)
  - [def get\_status()](#def-get\_status)
- [class LiveFormat()](#class-LiveFormat)
- [class LiveProtocol()](#class-LiveProtocol)
- [class LiveRoom()](#class-LiveRoom)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def ban\_user()](#async-def-ban\_user)
  - [async def get\_black\_list()](#async-def-get\_black\_list)
  - [async def get\_dahanghai()](#async-def-get\_dahanghai)
  - [async def get\_danmu\_info()](#async-def-get\_danmu\_info)
  - [async def get\_emoticons()](#async-def-get\_emoticons)
  - [async def get\_fan\_model()](#async-def-get\_fan\_model)
  - [async def get\_fans\_medal\_rank()](#async-def-get\_fans\_medal\_rank)
  - [async def get\_gaonengbang()](#async-def-get\_gaonengbang)
  - [async def get\_general\_info()](#async-def-get\_general\_info)
  - [async def get\_gift\_common()](#async-def-get\_gift\_common)
  - [async def get\_gift\_special()](#async-def-get\_gift\_special)
  - [async def get\_popular\_ticket\_num()](#async-def-get\_popular\_ticket\_num)
  - [async def get\_room\_id()](#async-def-get\_room\_id)
  - [async def get\_room\_info()](#async-def-get\_room\_info)
  - [async def get\_room\_play\_info()](#async-def-get\_room\_play\_info)
  - [async def get\_room\_play\_info\_v2()](#async-def-get\_room\_play\_info\_v2)
  - [async def get\_room\_play\_url()](#async-def-get\_room\_play\_url)
  - [async def get\_ruid()](#async-def-get\_ruid)
  - [async def get\_seven\_rank()](#async-def-get\_seven\_rank)
  - [async def get\_user\_info\_in\_room()](#async-def-get\_user\_info\_in\_room)
  - [async def receive\_reward()](#async-def-receive\_reward)
  - [async def send\_danmaku()](#async-def-send\_danmaku)
  - [async def send\_emoticon()](#async-def-send\_emoticon)
  - [async def send\_gift\_from\_bag()](#async-def-send\_gift\_from\_bag)
  - [async def send\_gift\_gold()](#async-def-send\_gift\_gold)
  - [async def send\_gift\_silver()](#async-def-send\_gift\_silver)
  - [async def send\_popular\_ticket()](#async-def-send\_popular\_ticket)
  - [async def sign\_up\_dahanghai()](#async-def-sign\_up\_dahanghai)
  - [async def start()](#async-def-start)
  - [async def stop()](#async-def-stop)
  - [async def unban\_user()](#async-def-unban\_user)
  - [async def update\_news()](#async-def-update\_news)
- [class ScreenResolution()](#class-ScreenResolution)
- [async def create\_live\_reserve()](#async-def-create\_live\_reserve)
- [async def get\_area\_info()](#async-def-get\_area\_info)
- [async def get\_gift\_config()](#async-def-get\_gift\_config)
- [async def get\_live\_followers\_info()](#async-def-get\_live\_followers\_info)
- [async def get\_self\_bag()](#async-def-get\_self\_bag)
- [async def get\_self\_dahanghai\_info()](#async-def-get\_self\_dahanghai\_info)
- [async def get\_self\_info()](#async-def-get\_self\_info)
- [async def get\_self\_live\_info()](#async-def-get\_self\_live\_info)
- [async def get\_unlive\_followers\_info()](#async-def-get\_unlive\_followers\_info)

---

## class LiveCodec()

**Extend: enum.Enum**

直播源视频编码

视频编码，0 为 avc 编码，1 为 hevc 编码。默认：0,1
+ AVC   : 0。
+ HEVC  : 1。
+ DEFAULT   : 0,1。




---

## class LiveDanmaku()

**Extend: bilibili_api.utils.AsyncEvent.AsyncEvent**

Websocket 实时获取直播弹幕

Extends: AsyncEvent

Logger: LiveDanmaku().logger

Events：
+ DANMU_MSG: 用户发送弹幕
+ SEND_GIFT: 礼物
+ COMBO_SEND：礼物连击
+ GUARD_BUY：续费大航海
+ SUPER_CHAT_MESSAGE：醒目留言（SC）
+ SUPER_CHAT_MESSAGE_JPN：醒目留言（带日语翻译？）
+ WELCOME: 老爷进入房间
+ WELCOME_GUARD: 房管进入房间
+ NOTICE_MSG: 系统通知（全频道广播之类的）
+ PREPARING: 直播准备中
+ LIVE: 直播开始
+ ROOM_REAL_TIME_MESSAGE_UPDATE: 粉丝数等更新
+ ENTRY_EFFECT: 进场特效
+ ROOM_RANK: 房间排名更新
+ INTERACT_WORD: 用户进入直播间
+ ACTIVITY_BANNER_UPDATE_V2: 好像是房间名旁边那个 xx 小时榜
+ ===========================
+ 本模块自定义事件：
+ ==========================
+ VIEW: 直播间人气更新
+ ALL: 所有事件
+ DISCONNECT: 断开连接（传入连接状态码参数）
+ TIMEOUT: 心跳响应超时
+ VERIFICATION_SUCCESSFUL: 认证成功




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `room_display_id` | `int` | 房间展示 ID |
| `debug` | `bool, optional` | 调试模式，将输出更多信息。. Defaults to False. |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |
| `max_retry` | `int, optional` | 连接出错后最大重试次数. Defaults to 5 |
| `retry_after` | `int, optional` | 连接出错后重试间隔时间（秒）. Defaults to 1 |


### async def connect()

连接直播间






### async def disconnect()

断开连接






### def get_live_room()

获取对应直播间对象



**Returns:** `LiveRoom`:  直播间对象




### def get_status()

获取连接状态



**Returns:** `int`:  0 初始化，1 连接建立中，2 已连接，3 断开连接中，4 已断开，5 错误




---

## class LiveFormat()

**Extend: enum.Enum**

直播源容器格式

容器格式，0 为 flv 格式；1 为 ts 格式（仅限 hls 流）；2 为 fmp4 格式（仅限 hls 流）。默认：0,2
+ FLV   : 0。
+ TS: 1。
+ FMP4  : 2。
+ DEFAULT   : 2。




---

## class LiveProtocol()

**Extend: enum.Enum**

直播源流协议。

流协议，0 为 FLV 流，1 为 HLS 流。默认：0,1
+ FLV : 0。
+ HLS : 1。
+ DEFAULT : 0,1




---

## class LiveRoom()

直播类，获取各种直播间的操作均在里边。


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |
| `room_display_id` | `int` | 房间展示 id |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `room_display_id` | `int` | 房间展示 ID（即 URL 中的 ID） |
| `credential` | `Credential, optional` | 凭据. Defaults to None. |


### async def ban_user()

封禁用户


| name | type | description |
| - | - | - |
| `uid` | `int` | 用户 UID |
| `hour` | `int` | 禁言时长，-1为永久，0为直到本场结束 |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_black_list()

获取黑名单列表



**Returns:** `dict`:  调用 API 返回的结果




### async def get_dahanghai()

获取大航海列表


| name | type | description |
| - | - | - |
| `page` | `int, optional` | 页码. Defaults to 1. |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_danmu_info()

获取聊天弹幕服务器配置信息(websocket)



**Returns:** `dict`:  调用 API 返回的结果




### async def get_emoticons()

获取本房间可用表情包



**Returns:** `dict`:  调用 API 返回的结果




### async def get_fan_model()

获取自己的粉丝勋章信息

如果带有房间号就返回是否具有的判断 has_medal

如果带有主播 id ，就返回主播的粉丝牌，没有就返回 null


| name | type | description |
| - | - | - |
| `roomId` | `int, optional` | 指定房间，查询是否拥有此房间的粉丝牌 |
| `target_id` | `int \| None, optional` | 指定返回一个主播的粉丝牌，留空就不返回 |
| `page_num` | `int \| None, optional` | 粉丝牌列表，默认 1 |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_fans_medal_rank()

获取粉丝勋章排行



**Returns:** `dict`:  调用 API 返回的结果




### async def get_gaonengbang()

获取高能榜列表


| name | type | description |
| - | - | - |
| `page` | `int, optional` | 页码. Defaults to 1 |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_general_info()

获取自己在该房间的大航海信息, 比如是否开通, 等级等


| name | type | description |
| - | - | - |
| `act_id` | `int, optional` | 未知，Defaults to 100061 |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_gift_common()

获取当前直播间内的普通礼物列表



**Returns:** `dict`:  调用 API 返回的结果




### async def get_gift_special()

注：此 API 已失效，请使用 live.get_gift_config

获取当前直播间内的特殊礼物列表


| name | type | description |
| - | - | - |
| `tab_id` | `int` | 2：特权礼物，3：定制礼物 |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_popular_ticket_num()

获取自己在直播间的人气票数量（付费人气票已赠送的量，免费人气票的持有量）



**Returns:** `dict`:  调用 API 返回的结果




### async def get_room_id()

获取直播间真实 id



**Returns:** `int`:  直播间 id




### async def get_room_info()

获取直播间信息（标题，简介等）



**Returns:** `dict`:  调用 API 返回的结果




### async def get_room_play_info()

获取房间信息（真实房间号，封禁情况等）



**Returns:** `dict`:  调用 API 返回的结果




### async def get_room_play_info_v2()

获取房间信息及可用清晰度列表


| name | type | description |
| - | - | - |
| `live_protocol` | `LiveProtocol, optional` | 直播源流协议. Defaults to LiveProtocol.DEFAULT. |
| `live_format` | `LiveFormat, optional` | 直播源容器格式. Defaults to LiveFormat.DEFAULT. |
| `live_codec` | `LiveCodec, optional` | 直播源视频编码. Defaults to LiveCodec.DEFAULT. |
| `live_qn` | `ScreenResolution, optional` | 直播源清晰度. Defaults to ScreenResolution.ORIGINAL. |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_room_play_url()

获取房间直播流列表


| name | type | description |
| - | - | - |
| `screen_resolution` | `ScreenResolution, optional` | 清晰度. Defaults to ScreenResolution.ORIGINAL |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_ruid()

获取直播的 up 的 uid (ruid)



**Returns:** `int`:  ruid




### async def get_seven_rank()

获取七日榜



**Returns:** `dict`:  调用 API 返回的结果




### async def get_user_info_in_room()

获取自己在直播间的信息（粉丝勋章等级，直播用户等级等）



**Returns:** `dict`:  调用 API 返回的结果




### async def receive_reward()

领取自己在某个直播间的航海日志奖励


| name | type | description |
| - | - | - |
| `receive_type` | `int` | 领取类型，Defaults to 2. |

**Returns:** `dict`:  调用 API 返回的结果




### async def send_danmaku()

直播间发送弹幕


| name | type | description |
| - | - | - |
| `danmaku` | `Danmaku` | 弹幕类 |
| `reply_mid` | `int, optional` | @的 UID. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




### async def send_emoticon()

直播间发送表情包


| name | type | description |
| - | - | - |
| `emoticon` | `Danmaku` | text为表情包代号 |

**Returns:** `dict`:  调用 API 返回的结果




### async def send_gift_from_bag()

赠送包裹中的礼物，获取包裹信息可以使用 get_self_bag 方法


| name | type | description |
| - | - | - |
| `uid` | `int` | 赠送用户的 UID |
| `bag_id` | `int` | 礼物背包 ID |
| `gift_id` | `int` | 礼物 ID |
| `gift_num` | `int` | 礼物数量 |
| `storm_beat_id` | `int, optional` | 未知， Defaults to 0 |
| `price` | `int, optional` | 礼物单价，Defaults to 0 |

**Returns:** `dict`:  调用 API 返回的结果




### async def send_gift_gold()

赠送金瓜子礼物


| name | type | description |
| - | - | - |
| `uid` | `int` | 赠送用户的 UID |
| `gift_id` | `int` | 礼物 ID (可以通过 get_gift_common 或 get_gift_special 或 get_gift_config 获取) |
| `gift_num` | `int` | 赠送礼物数量 |
| `price` | `int` | 礼物单价 |
| `storm_beat_id` | `int, Optional` | 未知，Defaults to 0 |

**Returns:** `dict`:  调用 API 返回的结果




### async def send_gift_silver()

赠送银瓜子礼物


| name | type | description |
| - | - | - |
| `uid` | `int` | 赠送用户的 UID |
| `gift_id` | `int` | 礼物 ID (可以通过 get_gift_common 或 get_gift_special 或 get_gift_config 获取) |
| `gift_num` | `int` | 赠送礼物数量 |
| `price` | `int` | 礼物单价 |
| `storm_beat_id` | `int, Optional` | 未知, Defaults to 0 |

**Returns:** `dict`:  调用 API 返回的结果




### async def send_popular_ticket()

赠送自己在直播间的所有免费人气票



**Returns:** `dict`:  调用 API 返回的结果




### async def sign_up_dahanghai()

大航海签到


| name | type | description |
| - | - | - |
| `task_id` | `int, optional` | 签到任务 ID. Defaults to 1447 |

**Returns:** `dict`:  调用 API 返回的结果




### async def start()

开始直播


| name | type | description |
| - | - | - |
| `area_id` | `int` | 直播分区id（子分区id）。可使用 live_area 模块查询。 |

**Returns:** `dict`:  调用 API 返回的结果




### async def stop()

关闭直播



**Returns:** `dict`:  调用 API 返回的结果




### async def unban_user()

解封用户


| name | type | description |
| - | - | - |
| `uid` | `int` | 用户 UID |

**Returns:** `dict`:  调用 API 返回的结果




### async def update_news()

更新公告


| name | type | description |
| - | - | - |
| `content` | `str` | 最多 60 字符 |

**Returns:** `dict`:  调用 API 返回的结果




---

## class ScreenResolution()

**Extend: enum.Enum**

直播源清晰度。

清晰度编号，4K 20000，原画 10000，蓝光（杜比）401，蓝光 400，超清 250，高清 150，流畅 80
+ FOUR_K: 4K。
+ ORIGINAL  : 原画。
+ BLU_RAY_DOLBY : 蓝光（杜比）。
+ BLU_RAY   : 蓝光。
+ ULTRA_HD  : 超清。
+ HD: 高清。
+ FLUENCY   : 流畅。




---

## async def create_live_reserve()

创建直播预约


| name | type | description |
| - | - | - |
| `title` | `str` | 直播间标题 |
| `start_time` | `int` | 开播时间戳 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_area_info()

获取所有分区信息



**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_gift_config()

获取所有礼物的信息，包括礼物 id、名称、价格、等级等。

同时填了 room_id、area_id、area_parent_id，则返回一个较小的 json，只包含该房间、该子区域、父区域的礼物。

但即使限定了三个条件，仍然会返回约 1.5w 行的 json。不加限定则是 2.8w 行。


| name | type | description |
| - | - | - |
| `room_id` | `int, optional` | 房间显示 ID. Defaults to None. |
| `area_id` | `int, optional` | 子分区 ID. Defaults to None. |
| `area_parent_id` | `int, optional` | 父分区 ID. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_live_followers_info()

获取关注列表中正在直播的直播间信息，包括房间直播热度，房间名称及标题，清晰度，是否官方认证等信息。


| name | type | description |
| - | - | - |
| `need_recommend` | `bool, optional` | 是否接受推荐直播间，Defaults to True |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_self_bag()

获取自己的直播礼物包裹信息



**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_self_dahanghai_info()

获取自己开通的大航海信息


| name | type | description |
| - | - | - |
| `page` | `int, optional` | 页数. Defaults to 1. |
| `page_size` | `int, optional` | 每页数量. Defaults to 10. |

**Returns:** `dict`:  调用 API 返回的结果


总页数取得方法:

```python
import math

info = live.get_self_live_info(credential)
pages = math.ceil(info['data']['guards'] / 10)
```



---

## async def get_self_info()

获取自己直播等级、排行等信息



**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_self_live_info()

获取自己的粉丝牌、大航海等信息



**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_unlive_followers_info()

获取关注列表中未在直播的直播间信息，包括上次开播时间，上次开播的类别，直播间公告，是否有录播等。


| name | type | description |
| - | - | - |
| `page` | `int, optional` | 页码, Defaults to 1. |
| `page_size` | `int, optional` | 每页数量 Defaults to 30. |

**Returns:** `dict`:  调用 API 返回的结果




