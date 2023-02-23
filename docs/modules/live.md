# Module live.py

```python
from bilibili_api import live
```

直播相关。

## class ScreenResolution

**Extends:** enum.Enum

直播源清晰度。

+ FOUR_K        : 4K。
+ ORIGINAL      : 原画。
+ BLU_RAY_DOLBY : 蓝光（杜比）。
+ BLU_RAY       : 蓝光。
+ ULTRA_HD      : 超清。
+ HD            : 高清。
+ FLUENCY       : 流畅。

---

## class LiveProtocol

**Extends:** enum.Enum

直播源流协议。

+ FLV
+ HLS
+ DEFAULT

---

## class LiveFormat

**Extends:** enum.Enum

直播源容器格式。

+ FLV
+ TS
+ FMP4
+ DEFAULT

---

## class LiveCodec

**Extends:** enum.Enum

直播源视频编码

+ AVC
+ HEVC
+ DEFAULT

---

## class LiveRoom

直播类，获取各种直播间的操作均在里边。

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| room_display_id | int | 房间展示 ID |

### Functions

#### def \_\_init\_\_()

| name            | type                 | description                   |
| --------------- | -------------------- | ----------------------------- |
| room_display_id | int                  | 房间展示 ID（即 URL 中的 ID） |
| credential      | Credential \| None, optional | 凭据. Defaults to None.       |

#### async def start()

| name | type | description |
| - | - | - |
| area_id | int | 直播分区id（子分区id）。可使用 live_area 模块查询。 |

开始直播

**Returns:** dict: 调用 API 返回的结果

#### async def stop()

停止直播

**Returns:** dict: 调用 API 返回的结果

#### async def get_room_play_info()

获取房间信息（真实房间号，直播状态，封禁情况等）

**Returns:** dict: 调用 API 返回的结果

#### async def get_room_id()

获取真实房号

**Returns:** 真实房号

#### async def get_ruid()

获取真实房间 id

**Returns:** 真实房间 id

#### async def get_chat_conf()

获取聊天弹幕服务器配置信息(websocket)

**Returns:** dict: 调用 API 返回的结果

#### async def get_room_info()

获取直播间信息（标题，简介，直播状态，直播开始时间，分区信息等）

**Returns:** dict: 调用 API 返回的结果

#### async def get_fan_model()

| name      | type          | description         |
|-----------|---------------|---------------------|
| roomId    | int, optional | 指定房间，查询是否拥有此房间的粉丝牌  |
| target_id | int \| None, optional | 指定返回一个主播的粉丝牌，留空就不返回 |
| page_num  | int \| None, optional | 页码. Defaults to 1   |

获取自己的粉丝勋章信息

如果带有房间号就返回是否具有的判断 has_medal

如果带有主播 id ，就返回主播的粉丝牌，没有就返回 null

**Returns:** dict: 调用 API 返回的结果

#### async def get_user_info_in_room()

获取自己在直播间的信息（粉丝勋章等级，直播用户等级等）

**Returns:** dict: 调用 API 返回的结果

#### async def get_dahanghai()

| name | type          | description         |
| ---- | ------------- | ------------------- |
| page | int, optional | 页码. Defaults to 1 |

获取大航海列表

**Returns:** dict: 调用 API 返回的结果

#### async def get_seven_rank()

获取七日榜

**Returns:** dict: 调用 API 返回的结果

#### async def get_fans_medal_rank()

获取粉丝勋章排行

**Returns:** dict: 调用 API 返回的结果

#### async def get_black_list()

获取房间黑名单

**Returns:** dict: 调用 API 返回的结果

#### async def get_room_play_url()

| name              | type                       | description                                   |
| ----------------- | -------------------------- | --------------------------------------------- |
| screen_resolution | ScreenResolution, optional | 清晰度. Defaults to ScreenResolution.ORIGINAL |

获取房间直播流列表

**Returns:** dict: 调用 API 返回的结果

#### async def get_room_play_info_v2()

| name          | type                       | description                                    |
|---------------|----------------------------|------------------------------------------------|
| live_protocol | LiveProtocol, optional     | 直播源流协议. Defaults to LiveProtocol.DEFAULT.      |
| live_format   | LiveFormat, optional       | 直播源容器格式. Defaults to LiveFormat.DEFAULT.       |
| live_codec    | LiveCodec, optional        | 直播源视频编码. Defaults to LiveCodec.DEFAULT.        |
| live_qn       | ScreenResolution, optional | 直播源清晰度. Defaults to ScreenResolution.ORIGINAL. |

获取房间信息及可用清晰度列表

**Returns:** dict: 调用 API 返回的结果

#### async def get_general_info()

| name   | type          | description              |
| ------ | ------------- | ------------------------ |
| act_id | int, optional | 未知. Defaults to 100061 |

获取自己在该房间的大航海信息, 比如是否开通, 等级等

**Returns:** dict: 调用 API 返回的结果

#### async def get_gift_common()

获取当前直播间内的普通礼物列表，此 API 只返回 `gift_id`，不包含礼物 `price` 参数

**Returns:** dict: 调用 API 返回的结果

#### async def get_gift_special()

| name   | type | description                           |
| ------ | ---- | ------------------------------------- |
| tab_id | int  | 礼物类型. 2：特权礼物， 3：定制礼物 |

获取当前直播间内的特殊礼物列表

**Returns:** dict: 调用 API 返回的结果

#### async def ban_user()

| name | type | description |
| ---- | ---- | ----------- |
| uid  | int  | 用户 UID    |

封禁用户

**Returns:** dict: 调用 API 返回的结果

#### async def unban_user()

| name     | type | description                               |
| -------- | ---- | ----------------------------------------- |
| block_id | int  | 封禁事件 ID，使用 `get_black_list()` 获取 |

解封用户

**Returns:** API 调用返回结果

#### async def receive_reward()

| name         | type | description             |
| ------------ | ---- | ----------------------- |
| receive_type | int  | 领取类型. Defaults to 2 |

领取自己在直播间内所有可领取的航海日志奖励

**Returns:** dict: 调用 API 返回的结果

#### async def sign_up_dahanghai()

| name    | type          | description               |
| ------- | ------------- | ------------------------- |
| task_id | int, optional | 任务 ID. Defaults to 1447 |

航海日志每日签到

**Returns:** dict: 调用 API 返回的结果

#### async def send_danmaku()

| name    | type    | description |
| ------- | ------- | ----------- |
| danmaku | Danmaku | 弹幕类      |

直播间发送弹幕

**Returns:** dict: 调用 API 返回的结果

#### asyc def send_gift_from_bag()

| name          | type          | description             |
| ------------- | ------------- | ----------------------- |
| uid           | int           | 赠送用户的 UID          |
| bag_id        | int           | 礼物背包 ID             |
| gift_id       | int           | 礼物 ID                 |
| gift_num      | int           | 赠送礼物数量            |
| storm_beat_id | int, optional | 未知. Defaults to 0     |
| price         | int, optional | 礼物单价. Defaults to 0 |

直播间赠送背包中的礼物

**Returns:** dict: 调用 API 返回的结果

#### asyc def send_gift_gold()

| name          | type          | description         |
| ------------- | ------------- | ------------------- |
| uid           | int           | 赠送用户的 UID      |
| gift_id       | int           | 礼物 ID             |
| gift_num      | int           | 赠送礼物数量        |
| price         | int           | 礼物单价            |
| storm_beat_id | int, optional | 未知. Defaults to 0 |

在直播间赠送金瓜子礼物，礼物id可通过 `get_gift_commom` 或 `get_gift_special` 或 `get_gift_config` 获取.

**Returns:** dict: 调用 API 返回的结果

#### asyc def send_gift_silver()

| name          | type          | description         |
| ------------- | ------------- | ------------------- |
| uid           | int           | 赠送用户的 UID      |
| gift_id       | int           | 礼物 ID             |
| gift_num      | int           | 赠送礼物数量        |
| price         | int           | 礼物单价            |
| storm_beat_id | int, optional | 未知. Defaults to 0 |

在直播间赠送银瓜子礼物，辣条的 `gift_id` 为 `1`

**Returns:** API 调用返回结果

---

## class LiveDanmaku

**Extends:** bilibili_api.utils.asyncEvent.AsyncEvent

Websocket 实时获取直播弹幕

**Events：**

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
+ ACTIVITY_BANNER_UPDATE_V2: 好像是房间名旁边那个xx小时榜
+ 本模块自定义事件：
+ VIEW: 直播间人气更新
+ ALL: 所有事件
+ DISCONNECT: 断开连接（传入连接状态码参数）
+ TIMEOUT: 心跳响应超时
+ VERIFICATION_SUCCESSFUL: 认证成功

### Functions

#### def \_\_init\_\_()

| name            | type                 | description                                    |
| --------------- | -------------------- | ---------------------------------------------- |
| room_display_id | int                  | 房间展示 ID                                    |
| debug           | bool, optional       | 调试模式，将输出更多信息。. Defaults to False. |
| credential      | Credential \| None, optional | 凭据. Defaults to None.                        |
| max_retry       | int, optional        | 连接出错后最大重试次数. Defaults to 5          |
| retry_after     | int, optional        | 连接出错后重试间隔时间（秒）. Defaults to 1    |

#### def get_status()

获取连接状态

**Returns:** int: 0 初始化，1 连接建立中，2 已连接，3 断开连接中，4 已断开，5 错误

#### async def connect()

连接直播间

**Returns:** None

#### async def disconnect()

断开连接

**Returns:** None

---

## async def get_self_info()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| credential | Credential | 凭据        |

获取自己直播等级、排行、硬币数、金银瓜子数等信息

**Returns:** dict: 调用 API 返回的结果

## async def get_self_live_info()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| credential | Credential | 凭据        |

获取自己直播间的等级、粉丝牌、自己开通的大航海数量等信息

**Returns:** dict: 调用 API 返回的结果

## async def get_self_bag()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| credential | Credential | 凭据        |

获取自己的直播礼物包裹信息

**Returns:** dict: 调用 API 返回的结果

## async def get_area_info()

获取所有分区信息

**Returns:** dict: 调用 API 返回的结果

## async def get_gift_config()

| name           | type          | description                  |
| -------------- | ------------- | ---------------------------- |
| room_id        | int \| None, optional | 房间显示 ID. Defaults to None |
| area_id        | int \| None, optional | 子分区 ID. Defaults to None   |
| area_parent_id | int \| None, optional | 父分区 ID. Defaults to None   |

获取所有礼物的信息，包括礼物 ID、名称、价格、等级等。

同时填了 `room_id`、`area_id`、`area_parent_id`，则返回一个较小的 json，只包含该房间、该子区域、父区域的礼物。

但即使限定了三个条件，仍然会返回约 1.5w 行的 json。不加限定则是 2.8w 行。

**Returns:** dict: 调用 API 返回的结果

## async def get_self_dahanghai_info()

| name       | type          | description              |
| ---------- | ------------- | ------------------------ |
| page       | int, optional | 页数. Defaults to 1      |
| page_size  | int, optional | 每页数量. Defaults to 10 |
| credential | Credential    | 凭据.  |

获取自己开通的大航海列表

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_live_followers_info()

| name           | type           | description                          |
| -------------- | -------------- | ------------------------------------ |
| need_recommend | bool, optional | 是否接受推荐直播间. Defaults to True |

获取关注列表中正在直播的直播间信息，包括房间直播热度，房间名称及标题，清晰度，是否官方认证等信息。

**Returns:** dict: 调用 API 返回的结果

#### async def get_unlive_followers_info()

| name      | type          | description              |
| --------- | ------------- | ------------------------ |
| page      | int, optional | 页码. Defaults to 1      |
| page_size | int, optional | 每页数量. Defaults to 30 |

获取关注列表中未在直播的直播间信息，包括上次开播时间，上次开播的类别，直播间公告，是否有录播等。


**Returns:** dict: 调用 API 返回的结果

---

## async def create_live_reserve()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| credential | Credential | 凭据        |
| title      | str        | 直播标题    |
| start_time | int        | 开播时间    |

创建直播预约

**Returns:** dict: 调用 API 返回的结果