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

## _async_ def get_real_url()

| name | type | description |
| - | - | - |
| short_url | str | 短链接 |

获取短链接对应的真实链接。

**注意：** 这个函数可以用于获取一个跳转`url`的目标。

**Returns:** 目标链接（如果不是有效的链接会报错）

## <span id="parse">_async_ def parse_link()</span>

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

[查看示例](https://nemo2011.github.io/bilibili-api/#/parse_link)

**Returns:** `Union[tuple, int]`:如果成功返回元组，失败返回 `-1`。

**元组第一项是对象，第二项是类型**

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

### Functions

#### def \_\_init\_\_()

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

#### def crack_uid()

破解 uid, 依赖 zlib

**Returns:** int: 真实 UID。
