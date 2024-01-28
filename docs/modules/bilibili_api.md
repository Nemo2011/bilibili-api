# Module bilibili_api

```python
import bilibili_api
```

根模块 (默认已导入所有子模块，例如 `bilibili_api.video`, `bilibili_api.user`)

---

## const dict HEADERS

访问 bilibili 视频下载链接等内部网址用的 HEADERS

---

## def set_session()

| name    | type                  | description                |
| ------- | --------------------- | -------------------------- |
| session | httpx.AsyncClient | httpx.AsyncClient 实例 |

用户手动设置 Session

**Returns:** None

---

## def get_session()

获取当前模块的 httpx.AsyncClient 对象，用于自定义请求

**Returns:** httpx.AsyncClient

---

## def set_aiohttp_session()

| name    | type                  | description                |
| ------- | --------------------- | -------------------------- |
| session | aiohttp.ClientSession | aiohttp.ClientSession 实例 |

用户手动设置 Session

**Returns:** None

---

## def get_aiohttp_session()

获取当前模块的 aiohttp.ClientSession 对象，用于自定义请求

**Returns:** aiohttp.ClientSession

---

## def set_httpx_sync_session()

| name    | type                  | description                |
| ------- | --------------------- | -------------------------- |
| session | httpx.Client | httpx.Client 实例 |

用户手动设置 Session

**Returns:** None

---

## def get_httpx_sync_session()

获取当前模块的 httpx.Client 对象，用于自定义请求

**Returns:** httpx.Client

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
| ac_time_value | str | 浏览器 Cookies 中的 ac_time 字段值 |

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

#### def has_ac_time_value()

是否提供 ac_time_value。

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

#### def raise_for_no_ac_time_value()

没有提供 ac_time_value 则抛出异常。

**Returns:** None

#### async def check_valid()

检查 cookies 是否有效

**Returns:** bool: cookies 是否有效

#### async def refresh()

刷新 cookies

**Returns:** None

#### def check_refresh()

检查 cookies 是否需要刷新

**Returns:** bool: cookies 是否需要刷新

---

**@dataclasses.dataclass**
## class Picture()

图片类，包含图片链接、尺寸以及下载操作。

Args:
    height    (int)  : 高度           
    imageType (str)  : 格式，例如: png
    size      (Any)  : 尺寸           
    url       (str)  : 图片链接        
    width     (int)  : 宽度           
    content   (bytes): 图片内容   

可以不实例化，用 `from_url` 或 `from_file` 或 `from_content` 加载。

### Functions

**@staticmethod**
#### def from_url

| name | type | description |
| ---- | ---- | ----------- |
| url  | str  | 图片链接。   |

加载网络图片。

**Returns:** Picture: 加载后的图片对象。

**@staticmethod**
#### def from_file

| name | type | description |
| ---- | ---- | ----------- |
| path | str  | 图片地址。   |

加载本地图片。

**@staticmethod**
#### def from_content

| name | type | description |
| ---- | ---- | ----------- |
| content | bytes | 图片内容 |
| format | str | 图片后缀名，如 `webp`, `jpg`, `ico` |

**Returns:** Picture: 加载后的图片对象。

#### async def upload_file()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类。 |

上传图片至 B 站。

**Returns:** Picture: `self`

#### def convert_format()

| name | type | description |
| ---- | ---- | ----------- |
| new_format | str | 新的格式。例：`png`, `ico`, `webp`. |

将图片转换为另一种格式。

**Returns:** Picture: `self`

#### async def download()

| name | type | description |
| ---- | ---- | ----------- |
| path | str  | 下载地址。    |

下载图片至本地。

**Returns:** Picture: `self`

#### def upload_file_sync()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类。 |

上传图片至 B 站。

**Returns:** Picture: `self`

#### def download_sync()

| name | type | description |
| ---- | ---- | ----------- |
| path | str  | 下载地址。    |

下载图片至本地。

**Returns:** Picture: `self`

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
| credential | Optional[Credential] | 凭据类. |

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

**Returns:** `Tuple[obj, ResourceType]`: 第一项为返回对象，第二项为对象类型。

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

#### def crack_uid()

暴力破解 UID，可能存在误差，请慎重使用。

**Returns:** int: 真实 UID。

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
