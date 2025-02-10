# Module video_uploader.py


bilibili_api.video_uploader

视频上传


``` python
from bilibili_api import video_uploader
```

- [class Lines()](#class-Lines)
- [class VideoEditor()](#class-VideoEditor)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def abort()](#async-def-abort)
  - [async def start()](#async-def-start)
- [class VideoEditorEvents()](#class-VideoEditorEvents)
- [class VideoMeta()](#class-VideoMeta)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def verify()](#async-def-verify)
- [class VideoPorderIndustry()](#class-VideoPorderIndustry)
- [class VideoPorderMeta()](#class-VideoPorderMeta)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
- [class VideoPorderShowType()](#class-VideoPorderShowType)
- [class VideoPorderType()](#class-VideoPorderType)
- [class VideoUploader()](#class-VideoUploader)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def abort()](#async-def-abort)
  - [async def start()](#async-def-start)
- [class VideoUploaderEvents()](#class-VideoUploaderEvents)
- [class VideoUploaderPage()](#class-VideoUploaderPage)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def get\_size()](#def-get\_size)
- [async def get\_available\_topics()](#async-def-get\_available\_topics)
- [async def get\_missions()](#async-def-get\_missions)
- [async def upload\_cover()](#async-def-upload\_cover)

---

## class Lines()

**Extend: enum.Enum**

可选线路

bupfetch 模式下 kodo 目前弃用 `{'error': 'no such bucket'}`

+ BDA2：百度
+ QN：七牛
+ WS：网宿
+ BLDSA：bldsa




---

## class VideoEditor()

**Extend: bilibili_api.utils.AsyncEvent.AsyncEvent**

视频稿件编辑


| name | type | description |
| - | - | - |
| `bvid` | `str` | 稿件 BVID |
| `meta` | `Dict` | 视频信息 |
| `cover_path` | `str` | 封面路径. Defaults to None(不更换封面). |
| `credential` | `Credential` | 凭据类. Defaults to None. |


### def \_\_init\_\_()

meta 参数示例: (保留 video, cover, tid, aid 字段)

``` json
{
"title": "str: 标题",
"copyright": "int: 是否原创，0 否 1 是",
"tag": "标签. 用,隔开. ",
"desc_format_id": "const int: 0",
"desc": "str: 描述",
"dynamic": "str: 动态信息",
"interactive": "const int: 0",
"new_web_edit": "const int: 1",
"act_reserve_create": "const int: 0",
"handle_staff": "const bool: false",
"topic_grey": "const int: 1",
"no_reprint": "int: 是否显示“未经允许禁止转载”. 0 否 1 是",
"subtitles # 字幕设置": {
"lan": "str: 字幕投稿语言，不清楚作用请将该项设置为空",
"open": "int: 是否启用字幕投稿，1 or 0"
},
"web_os": "const int: 2"
}
```


| name | type | description |
| - | - | - |
| `bvid` | `str` | 稿件 BVID |
| `meta` | `Dict` | 视频信息 |
| `cover` | `str \| Picture` | 封面地址. Defaults to None(不更改封面). |
| `credential` | `Credential \| None` | 凭据类. Defaults to None. |


### async def abort()

中断更改






### async def start()

开始更改



**Returns:** `dict`:  返回带有 bvid 和 aid 的字典。




---

## class VideoEditorEvents()

**Extend: enum.Enum**

视频稿件编辑事件枚举

+ PRELOAD   : 加载数据前
+ AFTER_PRELOAD : 加载成功
+ PRELOAD_FAILED: 加载失败
+ PRE_COVER : 上传封面前
+ AFTER_COVER   : 上传封面后
+ COVER_FAILED  : 上传封面失败
+ PRE_SUBMIT: 提交前
+ AFTER_SUBMIT  : 提交后
+ SUBMIT_FAILED : 提交失败
+ COMPLETED : 完成
+ ABOTRED   : 停止
+ FAILED: 失败




---

## class VideoMeta()

视频源数据




### def \_\_init\_\_()

基本视频上传参数

可调用 VideoMeta.verify() 验证部分参数是否可用


| name | type | description |
| - | - | - |
| `tid` | `int` | 分区 id |
| `title` | `str` | 视频标题，最多 80 字 |
| `desc` | `str` | 视频简介，最多 2000 字 |
| `cover` | `Union[Picture, str]` | 封面，可以传入路径 |
| `tags` | `List[str], str` | 标签列表，传入 List 或者传入 str 以 "," 为分隔符，至少 1 个 Tag，最多 10 个 |
| `topic` | `Optional[Union[int, Topic]]` | 活动主题，应该从 video_uploader.get_available_topics(tid) 获取，可选 |
| `mission_id` | `Optional[int]` | 任务 id，与 topic 一同获取传入 |
| `original` | `bool` | 是否原创，默认原创 |
| `source` | `Optional[str]` | 转载来源，非原创应该提供 |
| `recreate` | `Optional[bool]` | 是否允许转载. 可选，默认为不允许二创 |
| `no_reprint` | `Optional[bool]` | 未经允许是否禁止转载. 可选，默认为允许转载 |
| `open_elec` | `Optional[bool]` | 是否开启充电. 可选，默认为关闭充电 |
| `up_selection_reply` | `Optional[bool]` | 是否开启评论精选. 可选，默认为关闭评论精选 |
| `up_close_danmu` | `Optional[bool]` | 是否关闭弹幕. 可选，默认为开启弹幕 |
| `up_close_reply` | `Optional[bool]` | 是否关闭评论. 可选，默认为开启评论 |
| `lossless_music` | `Optional[bool]` | 是否开启无损音乐. 可选，默认为关闭无损音乐 |
| `dolby` | `Optional[bool]` | 是否开启杜比音效. 可选，默认为关闭杜比音效 |
| `subtitle` | `Optional[Dict]` | 字幕信息，可选 |
| `dynamic` | `Optional[str]` | 粉丝动态，可选，最多 233 字 |
| `neutral_mark` | `Optional[str]` | 创作者声明，可选 |
| `delay_time` | `Optional[Union[int, datetime]]` | 定时发布时间，可选 |
| `porder` | `Optional[VideoPorderMeta]` | 商业相关参数，可选 |


### async def verify()

验证参数是否可用，仅供参考

检测 tags、delay_time、topic -> mission、cover 和 tid

验证失败会抛出异常






---

## class VideoPorderIndustry()

**Extend: enum.Enum**

商单行业

+ MOBILE_GAME: 手游
+ CONSOLE_GAME: 主机游戏
+ WEB_GAME: 网页游戏
+ PC_GAME: PC单机游戏
+ PC_NETWORK_GAME: PC网络游戏
+ SOFTWARE_APPLICATION: 软件应用
+ DAILY_NECESSITIES_AND_COSMETICS: 日用品化妆品
+ CLOTHING_SHOES_AND_HATS: 服装鞋帽
+ LUGGAGE_AND_ACCESSORIES: 箱包饰品
+ FOOD_AND_BEVERAGE: 食品饮料
+ PUBLISHING_AND_MEDIA: 出版传媒
+ COMPUTER_HARDWARE: 电脑硬件
+ OTHER: 其他
+ MEDICAL: 医疗类
+ FINANCE: 金融




---

## class VideoPorderMeta()

视频商业相关参数




### def \_\_init\_\_()





---

## class VideoPorderShowType()

**Extend: enum.Enum**

商单形式

+ LOGO: Logo
+ OTHER: 其他
+ SPOKEN_AD: 口播
+ PATCH: 贴片
+ TVC_IMBEDDED: TVC植入
+ CUSTOMIZED_AD: 定制软广
+ PROGRAM_SPONSORSHIP: 节目赞助
+ SLOGAN: SLOGAN
+ QR_CODE: 二维码
+ SUBTITLE_PROMOTION: 字幕推广




---

## class VideoPorderType()

视频商业类型

+ FIREWORK: 花火
+ OTHER: 其他




---

## class VideoUploader()

**Extend: bilibili_api.utils.AsyncEvent.AsyncEvent**

视频上传


| name | type | description |
| - | - | - |
| `pages` | `List[VideoUploaderPage]` | 分 P 列表 |
| `meta` | `VideoMeta, Dict` | 视频信息 |
| `credential` | `Credential` | 凭据 |
| `cover_path` | `str` | 封面路径 |
| `line` | `Lines, Optional` | 线路. Defaults to None. 不选择则自动测速选择 |


### def \_\_init\_\_()

建议传入 VideoMeta 对象，避免参数有误

meta 参数示例：

```json
{
"title": "",
"copyright": 1,
"tid": 130,
"tag": "",
"desc_format_id": 9999,
"desc": "",
"recreate": -1,
"dynamic": "",
"interactive": 0,
"act_reserve_create": 0,
"no_disturbance": 0,
"no_reprint": 1,
"subtitle": {
"open": 0,
"lan": "",
},
"dolby": 0,
"lossless_music": 0,
"web_os": 1,
}
```

meta 保留字段：videos, cover


| name | type | description |
| - | - | - |
| `pages` | `List[VideoUploaderPage]` | 分 P 列表 |
| `meta` | `VideoMeta, Dict` | 视频信息 |
| `credential` | `Credential` | 凭据 |
| `cover` | `Union[str, Picture]` | 封面路径或者封面对象. Defaults to ""，传入 meta 类型为 VideoMeta 时可不传 |
| `line` | `Lines, Optional` | 线路. Defaults to None. 不选择则自动测速选择 |


### async def abort()

中断上传






### async def start()

开始上传



**Returns:** `dict`:  返回带有 bvid 和 aid 的字典。




---

## class VideoUploaderEvents()

**Extend: enum.Enum**

上传事件枚举

Events:
+ PRE_PAGE 上传分 P 前
+ PREUPLOAD  获取上传信息
+ PREUPLOAD_FAILED  获取上传信息失败
+ PRE_CHUNK  上传分块前
+ AFTER_CHUNK  上传分块后
+ CHUNK_FAILED  区块上传失败
+ PRE_PAGE_SUBMIT  提交分 P 前
+ PAGE_SUBMIT_FAILED  提交分 P 失败
+ AFTER_PAGE_SUBMIT  提交分 P 后
+ AFTER_PAGE  上传分 P 后
+ PRE_COVER  上传封面前
+ AFTER_COVER  上传封面后
+ COVER_FAILED  上传封面失败
+ PRE_SUBMIT  提交视频前
+ SUBMIT_FAILED  提交视频失败
+ AFTER_SUBMIT  提交视频后
+ COMPLETED  完成上传
+ ABORTED  用户中止
+ FAILED  上传失败




---

## class VideoUploaderPage()

分 P 对象




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `path` | `str` | 视频文件路径 |
| `title` | `str` | 视频标题 |
| `description` | `str, optional` | 视频简介. Defaults to "". |


### def get_size()

获取文件大小



**Returns:** `int`:  文件大小




---

## async def get_available_topics()

获取可用 topic 列表






---

## async def get_missions()

获取活动信息


| name | type | description |
| - | - | - |
| `tid` | `int, optional` | 分区 ID. Defaults to 0. |
| `credential` | `Credential, optional` | 凭据. Defaults to None. |

**Returns:** `dict`:  API 调用返回结果




---

## async def upload_cover()

上传封面



**Returns:** `str`:  封面 URL




