# Module bilibili_api

```python
import bilibili_api
```

根模块

## const dict HEADERS

访问 bilibili 视频下载链接等内部网址用的 HEADERS

## def set_session()

| name    | type                  | description                |
| ------- | --------------------- | -------------------------- |
| session | httpx.AsyncSession | httpx.AsyncSession 实例 |

用户手动设置 Session

**Returns:** None

---

## def get_session()

获取当前模块的 httpx.AsyncSession 对象，用于自定义请求

**Returns:** httpx.AsyncSession

---

## class Credential

凭据类，用于各种请求操作的验证。

### Functions

#### def \_\_init\_\_()

| name     | type          | description                         |
| -------- | ------------- | ----------------------------------- |
| sessdata | str, optional | 浏览器 Cookies 中的 SESSDATA 字段值 |
| bili_jct | str, optional | 浏览器 Cookies 中的 bili_jct 字段值 |
| buvid3   | str, optional | 浏览器 Cookies 中的 BUVID3 字段值   |
| dedeuserid | str, optional | 浏览器 Cookies 中的 DedeUserID 字段值 |

各字段获取方式查看：https://nemo2011.github.io/bilibili-api/#/get-credential.md

#### def get_cookies()

获取请求 Cookies 字典

**Returns:** dict: 请求 Cookies 字典

#### def has_sessdata()

是否提供 sessdata。

**Returns:** bool

#### def has_bili_jct()

是否提供 bili_jct。

**Returns:** bool

#### def has_buvid3()

是否提供 buvid3。

**Returns:** bool

#### def has_dedeuserid()

是否提供 dedeuserid。

**Returns:** bool

#### def raise_for_no_sessdata()

没有提供 sessdata 则抛出异常。

**Returns:** None

#### def raise_for_no_bili_jct()

没有提供 bili_jct 则抛出异常。

**Returns:** None

#### def raise_for_no_buvid3()

没有提供 buvid3 则抛出异常。

**Returns:** None

#### def raise_for_no_dedeuserid()

没有提供 dedeuserid 则抛出异常。

**Returns:** None

#### async def check_valid()

检查 cookies 是否有效

**Returns:** bool: cookies 是否有效

---

## def sync()

| name      | type      | description |
| --------- | --------- | ----------- |
| coroutine | Coroutine | 异步函数    |

同步执行异步函数，使用可参考 [同步执行异步代码](https://nemo2011.github.io/bilibili-api/#/sync-executor)

**Returns:** 该异步函数的返回值

---

## def aid2bvid()

| name | type | description |
| ---- | ---- | ----------- |
| aid  | int  | AV 号       |

AV 号转 BV 号。

**Returns:** str: BV 号。

---

## def bvid2aid()

| name | type | description |
| ---- | ---- | ----------- |
| bvid | str  | BV 号。     |

BV 号转 AV 号。

**Returns:** int: AV 号。

---

## async def get_real_url()

| name | type | description |
| - | - | - |
| short_url | str | 短链接 |

获取短链接对应的真实链接。

**注意：** 这个函数可以用于获取一个跳转`url`的目标。

**Returns:** 目标链接（如果不是有效的链接会报错）

---

## class ResourceType()

### Extends: enum.Enum

链接类型类。

+ VIDEO: 视频
+ BANGUMI: 番剧
+ EPISODE: 番剧剧集
+ FAVORITE_LIST: 视频收藏夹
+ CHEESE: 课程
+ CHEESE_VIDEO: 课程视频
+ AUDIO: 音频
+ AUDIO_LIST: 歌单
+ ARTICLE: 专栏
+ USER: 用户
+ LIVE: 直播间
+ CHANNEL_SERIES: 合集与列表

## <span id="parse">async def parse_link()</span>

| name | type | description |
| - | - | - |
| url | str | 链接 |
| credential | Credential | 凭据类 |

获取链接对应的对象。举个例子：如果有一个视频链接，想要获取对应的 `Video` 类需要读取 `bvid` 或 `aid`，然后初始化 `Video` 类。
但是 `parse_link` 可以自动读取 `bvid` 或 `aid` 并生成对应的对象。

**注意：** `parse_link` 会读取可跳转链接的目标链接！

目前 `parse_link` 函数支持解析：

- 视频
- 番剧
- 番剧剧集
- 收藏夹
- 课程视频
- 音频
- 歌单
- 专栏
- 用户
- 直播间
- 合集与列表
- 游戏
- 话题

[查看示例](https://nemo2011.github.io/bilibili-api/#/parse_link)

**Returns:** `tuple[obj, ResourceType]`: 第一项为返回对象，第二项为对象类型。

**元组第一项是资源对象，第二项是资源类型**

---

## class DmMode

弹幕模式

+ FLY: 飞行弹幕
+ TOP: 顶部弹幕
+ BOTTOM: 底部弹幕
+ REVERSE: 反向弹幕

---

## class DmFontSize

弹幕字体大小

+ EXTREME_SMALL: 最小
+ SUPER_SMALL: 非常小
+ SMALL: 小
+ NORMAL: 中等
+ BIG: 大
+ SUPER_BIG: 非常大
+ EXTREME_BIG: 最大

---

## class Danmaku

弹幕类

### Attributes

| name      | type               | description                                                 |
| --------- | ------------------ | ----------------------------------------------------------- |
| text      | str                  | 弹幕文本。                                                  |
| dm_time   | float, optional      | 弹幕在视频中的位置，单位为秒。Defaults to 0.0.              |
| send_time | float, optional      | 弹幕发送的时间。Defaults to time.time().                    |
| crc32_id  | str, optional        | 弹幕发送者 UID 经 CRC32 算法取摘要后的值。Defaults to None. |
| color     | str, optional        | 弹幕十六进制颜色。Defaults to "ffffff".                     |
| weight    | int, optional        | 弹幕在弹幕列表显示的权重。Defaults to -1.                   |
| id_       | int, optional        | 弹幕 ID。Defaults to -1.                                    |
| id_str    | str, optional        | 弹幕字符串 ID。Defaults to "".                              |
| action    | str, optional        | 暂不清楚。Defaults to "".                                   |
| mode      | DmMode, optional     | 弹幕模式。Defaults to DmMode.FLY.                             |
| font_size | DmFontSize, optional | 弹幕字体大小。Defaults to DmFontSize.NORMAL.                  |
| is_sub    | bool, optional       | 是否为字幕弹幕。Defaults to False.                          |
| pool      | int, optional        | 暂不清楚。Defaults to -1.                                   |
| attr      | int, optional        | 暂不清楚。 Defaults to -1.                                  |

### Functions

#### def \_\_init\_\_()

| name      | type               | description                                                 |
| --------- | ------------------ | ----------------------------------------------------------- |
| text      | str                  | 弹幕文本。                                                  |
| dm_time   | float, optional      | 弹幕在视频中的位置，单位为秒。Defaults to 0.0.              |
| send_time | float, optional      | 弹幕发送的时间。Defaults to time.time().                    |
| crc32_id  | str, optional        | 弹幕发送者 UID 经 CRC32 算法取摘要后的值。Defaults to "". |
| color     | str, optional        | 弹幕十六进制颜色。Defaults to "ffffff".                     |
| weight    | int, optional        | 弹幕在弹幕列表显示的权重。Defaults to -1.                   |
| id_       | int, optional        | 弹幕 ID。Defaults to -1.                                    |
| id_str    | str, optional        | 弹幕字符串 ID。Defaults to "".                              |
| action    | str, optional        | 暂不清楚。Defaults to "".                                   |
| mode      | DmMode, optional     | 弹幕模式。Defaults to DmMode.FLY.                             |
| font_size | DmFontSize, optional | 弹幕字体大小。Defaults to DmFontSize.NORMAL.                  |
| is_sub    | bool, optional       | 是否为字幕弹幕。Defaults to False.                          |
| pool      | int, optional        | 暂不清楚。Defaults to -1.                                   |
| attr      | int, optional        | 暂不清楚。 Defaults to -1.                                  |

#### def set_crc32_id()

| name      | type               | description                                                 |
| - | - | - |
| crc32_id | str | crc32_id |

设置 crc32_id 同时破解 uid

#### def to_xml()

将弹幕转换为 xml 格式弹幕

**Returns:** str: xml 格式弹幕

---

## class SpecialDanmaku

### Attributes

| name | type | description |
| - | - | - |
| content | str | 弹幕内容 |
| id_ | int | 弹幕 ID |
| id_str | str | 弹幕字符串 ID |
| mode | DmMode | int | 弹幕模式 |
| pool | int | 池 |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| content | str | 弹幕内容 |
| id_ | int | 弹幕 ID |
| id_str | str | 弹幕字符串 ID |
| mode | DmMode \| int | 弹幕模式 |
| pool | int | 池 |

---

## class GetItemObjectType

**Extends: enum.Enum**

资源类型。(仅供 get_item 使用)
+ VIDEO : 视频
+ BANGUMI : 番剧
+ FT : 影视
+ LIVE : 直播
+ ARTICLE : 专栏
+ USER : 用户
+ LIVEUSER : 直播间用户
+ GAME: 游戏

## async def get_item()

通过名称及类型获取对应资源。

支持：视频，番剧，影视，直播间，专栏，用户，直播用户，游戏

如：名称是"碧诗", 类型是用户, 就能得到 User(uid = 2)

| name | type | description |
| - | - | - |
| name | str |             名称 |
| obj_type | GetItemObjectType | 资源类型 |
| credential | Credential     | 凭据 |

**Returns:** 对应资源或 -1 (无匹配资源)

---

## class AsyncEvent

发布-订阅模式异步事件类支持。

特殊事件：\_\_ALL\_\_ 所有事件均触发

### Functions

#### def add_eevent_listener()

| name | type | description |
| - | - | - |
| name | str |           事件名。 |
| handler | Coroutine |   回调异步函数。 |

注册事件监听器。

#### def on()

装饰器注册事件监听器。

| name | type | description |
| - | - | - |
| event_name | str | 事件名。 |

#### def remove_all_event_listener()

移除所有事件监听函数

#### def remove_event_listener()

移除事件监听函数。

| name | type | description |
| - | - | - |
| name | str |            事件名 |
| handler | Coroutine |   要移除的函数 |

**Returns:** bool, 是否移除成功。

#### def ignore_event()

忽略指定事件

| name | type | description |
| - | - | - |
| name | str | 事件名 |

#### def remove_ignore_events()

移除所有忽略事件
