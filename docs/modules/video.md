# Module video.py

```python
from bilibili_api import video
```

视频相关操作。

?> 注意，同时存在 page_index 和 cid 的参数，两者至少提供一个。

## class DanmakuOperatorType(Enum)

**Extends:** enum.Enum

弹幕操作枚举

+ DELETE - 删除弹幕
+ PROTECT - 保护弹幕
+ UNPROTECT - 取消保护弹幕

---

## class VideoAppealReasonType

视频投诉原因枚举

注意: 每一项均为函数，部分项有参数，没有参数的函数无需调用函数，直接传入即可，有参数的函数请调用结果之后传入。

- ILLEGAL(): 违法违禁
- PRON(): 色情
- VULGAR(): 低俗
- GAMBLED_SCAMS(): 赌博诈骗
- VIOLENT(): 血腥暴力
- PERSONAL_ATTACK(): 人身攻击
- PLAGIARISM(bvid: str): 与站内其他视频撞车
- BAD_FOR_YOUNGS(): 青少年不良信息
- CLICKBAIT(): 不良封面/标题
- POLITICAL_RUMORS(): 涉政谣言
- SOCIAL_RUMORS(): 涉社会事件谣言
- COVID_RUMORS(): 疫情谣言
- UNREAL_EVENT(): 虚假不实消息
- OTHER(): 有其他问题
- LEAD_WAR(): 引战
- CANNOT_CHARGE(): 不能参加充电
- UNREAL_COPYRIGHT(source: str): 转载/自制类型错误

---

## class VideoQuality()

**Extends:enum.Enum**

- _360P: 流畅 360P
- _480P: 清晰 480P
- _720P: 高清 720P60
- _1080P: 高清 1080P
- _1080P_PLUS: 高清 1080P 高码率
- _1080P_60: 高清 1080P 60 帧码率
- _4K: 超清 4K
- HDR: 真彩 HDR
- DOLBY: 杜比视界
- _8K: 超高清 8K

---

## class VideoCodecs()

**Extends:enum.Enum**

- HEV: HEVC(H.265)
- AVC: AVC(H.264)
- AV1: AV1

---

## class AudioQuality()

**Extends:enum.Enum**

- _64K: 64K
- _132K: 132K
- _192K: 192K
- HI_RES: Hi-Res 无损
- DOLBY: 杜比全景声

---

## async def get_cid_info()

| name | type | description |
| ---- | ---- | ----------- |
| cid | int | 分 P 编码 |

获取 cid 信息 (对应的视频，具体分 P 序号，up 等)

**Returns:** dict: 调用 https://hd.biliplus.com 的 API 返回的结果

---

## class Video

视频类，各种对视频的操作均在里面。

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

### Functions

#### def \_\_init\_\_()

| name       | type                 | description                           |
| ---------- | -------------------- | ------------------------------------- |
| bvid       | str \| None, optional        | BV 号。bvid 和 aid 必须提供其中之一。 |
| aid        | int \| None, optional        | AV 号。bvid 和 aid 必须提供其中之一。 |
| credential | Credential \| None, optional | Credential 类。Defaults to None.      |

#### def set_bvid()

| name | type | description |
| ---- | ---- | ----------- |
| bvid | str  | BV 号。     |

设置 bvid。

**Returns:** None

#### def get_bvid()

获取 bvid。

**Returns:** str: bvid

#### def set_aid()

| name | type | description |
| ---- | ---- | ----------- |
| aid  | int  | AV 号。     |

设置 aid。

**Returns:** None

#### def get_aid()

获取 aid。

**Returns:** int: aid

#### async def get_info()

获取视频信息。

**Returns:** API 调用返回结果。

#### async def get_stat()

获取视频统计数据（播放量，点赞数等）。

**Returns:** API 调用返回结果。

#### async def get_tags()

| name | type | description |
| ---- | ---- | ----------- |
| page_index | int \| None | 分 P 序号 |
| cid | int \| None | 分 P 编码 |

获取视频标签。

**Returns:** API 调用返回结果。

#### async def get_chargers()

获取视频充电用户。

**Returns:** API 调用返回结果。

#### async def get_video_snapshot()

| name | type | description |
| - | - | - |
| cid | int \| None | 分 P 序号 |
| json_index | bool | 是否需要json 数组截取时间表 |
| pvideo | bool | 是否只获取封面预览 |

获取视频快照信息。

Tip:返回的 url 均不带 http 前缀，且只获取封面预览返回的是未转义的 url

**Returns:** WebAPI 调用返回结果

#### async def get_pages()

获取分 P 信息。

**Returns:** API 调用返回结果。

#### async def get_cid()

| name | type | description |
| - | - | - |
| page_index | int | 分 P 序号 |

获取稿件 cid。

#### async def get_download_url()

| name       | type          | description                          |
| ---------- | ------------- | ------------------------------------ |
| page_index | int \| None, optional | 分 P 号，从 0 开始。Defaults to None |
| cid        | int \| None, optional | 分 P 的 ID。Defaults to None         |
| html5      | bool, optional | 是否以 html5 平台访问，这样子能直接在网页中播放，但是链接少。 |

获取视频下载信息。

**Returns:** API 调用返回结果。

#### async def get_related()

获取相关视频信息。

**Returns:** API 调用返回结果。

#### async def get_relation()

获取用户与视频的关系

**Returns:** API 调用返回结果。

#### async def has_liked()

视频是否点赞过。

**Returns:** bool: 视频是否点赞过。

#### async def get_pay_coins()

获取视频已投币数量。

**Returns:** int: 视频已投币数量。

#### async def has_favoured()

是否已收藏。

**Returns:** bool: 视频是否已收藏。

#### async def is_forbid_note()

是否禁止笔记。

**Returns:** bool: 是否禁止笔记。

#### async def get_private_notes_list()

获取稿件私有笔记列表。

**Returns:** list: 私有笔记 note_id 列表。

#### async def get_public_notes_list()

| name | type | description |
| ---- | ---- | ----------- |
| pn   | int  | 第几页.      |
| ps   | int  | 每页内容数量. |

获取稿件公开笔记列表。

**Returns:** dict: 调用 API 返回的结果

#### async def get_ai_conclusion():

| name | type | description |
| ---- | ---- | ----------- |
| page_index | int \| None, optional | 分 P 号，从 0 开始。Defaults to None |
| cid        | int \| None, optional | 分 P 的 ID。Defaults to None         |
| up_mid | int \| None, optional | up 主的 mid。Defaults to None         |

获取 AI 总结结果。

page_index 和 cid 必须提供其中之一。

**Returns:** dict: API 调用返回结果。

#### async def get_danmaku_view():

| name       | type          | description                          |
| ---------- | ------------- | ------------------------------------ |
| page_index | int \| None, optional | 分 P 号，从 0 开始。Defaults to None |
| cid        | int \| None, optional | 分 P 的 ID。Defaults to None         |

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。

**Returns:** API 调用返回结果。

#### async def get_danmakus()

| name       | type                    | description                                               |
| ---------- | ----------------------- | --------------------------------------------------------- |
| page_index | int, optional           | 分 P 号，从 0 开始。Defaults to None                      |
| date       | datetime.Date \| None, optional | 指定日期后为获取历史弹幕，精确到年月日。Defaults to None. |
| cid        | int \| None, optional           | 分 P 的 ID。Defaults to None                              |
| from_seg | int \| None, optional | 从第几段开始(0 开始编号，None 为从第一段开始，一段 6 分钟). Defaults to None. |
| to_seg | int \| None, optional | 到第几段结束(0 开始编号，None 为到最后一段，包含编号的段，一段 6 分钟). Defaults to None. |

**注意**：
- 1. 段数可以使用 `get_danmaku_view()["dm_seg"]["total"]` 查询。
- 2. `from_seg` 和 `to_seg` 仅对 `date == None` 的时候有效果。
- 3. 例：取前 `12` 分钟的弹幕：`from_seg=0, to_seg=1`

获取弹幕。

**Returns:** List[Danmaku]: Danmaku 类的列表。

#### async def get_danmaku_xml()

| name | type | description |
| ---- | ---- | ----------- |
| page_index | int, optional | 分 P 号，从 0 开始。 |
| cid | int \| None, optional | 分 P 编号. Defaults to None. |

获取所有弹幕的 XML 源

**Returns** str: XML 源

#### async def get_special_dms()

获取特殊弹幕

| name | type | description |
| ---- | ---- | ----------- |
| page_index | int, optional        | 分 P 号. Defaults to 0.  |
| cid        | int | None, optional | 分 P id. Defaults to None.  |

**Returns:** List[SpecialDanmaku]: 调用接口解析后的结果

#### async def get_history_danmaku_index()

| name       | type                    | description                                               |
| ---------- | ----------------------- | --------------------------------------------------------- |
| page_index | int \| None, optional           | 分 P 号，从 0 开始。Defaults to None                      |
| date       | datetime.Date \| None | 指定日期后为获取历史弹幕，精确到年月日。Defaults to None. |
| cid        | int \| None, optional           | 分 P 的 ID。Defaults to None                              |

获取特定月份存在历史弹幕的日期。

**Returns:** None | List[str]: 调用 API 返回的结果。不存在时为 None。

#### async def has_liked_danmakus()

| name       | type          | description                          |
| ---------- | ------------- | ------------------------------------ |
| page_index | int, optional | 分 P 号，从 0 开始。Defaults to None |
| ids        | List[int]     | 要查询的弹幕 ID 列表。               |
| cid        | int, optional | 分 P 的 ID。Defaults to None         |

是否已点赞弹幕。

**Returns:** API 调用返回结果。

#### async def send_danmaku()

| name       | type          | description                          |
| ---------- | ------------- | ------------------------------------ |
| page_index | int \| None, optional | 分 P 号，从 0 开始。Defaults to None |
| danmaku    | Danmaku \| None       | Danmaku 类。                         |
| cid        | int \| None, optional | 分 P 的 ID。Defaults to None         |

发送弹幕。

**Returns:** API 调用返回结果。

#### async def like_danmaku()

| name       | type           | description                          |
| ---------- | -------------- | ------------------------------------ |
| page_index | int \| None, optional  | 分 P 号，从 0 开始。Defaults to None |
| dmid       | int \| None            | 弹幕 ID。                            |
| status     | bool \| None, optional | 点赞状态。Defaults to True.          |
| cid        | int \| None, optional  | 分 P 的 ID。Defaults to None         |

点赞弹幕。

#### async def operate_danmaku()

| name       | type                | description                          |
| ---------- | ------------------- | ------------------------------------ |
| page_index | int \| None, optional       | 分 P 号，从 0 开始。Defaults to None |
| dmids      | List[int] \| None          | 弹幕 ID 列表。                       |
| type_      | DanmakuOperatorType \| None | 操作类型                             |
| cid        | int \| None, optional       | 分 P 的 ID。Defaults to None         |

操作弹幕（如删除、保护等）。

**Returns:** API 调用返回结果。

#### async def get_danmaku_snapshot()

获取弹幕快照

**Returns:** API 调用返回结果。

#### async def recall_danmaku()

| name | type | description |
| - | - | - |
| page_index | int \| None, optional | 分 P 号 |
| dmid | int | 弹幕 id |
| cid | int \| None, optional | 分 P 编码 |

撤回弹幕

**Returns:** API 调用返回结果。

#### async def get_pbp()

| name | type | description |
| - | - | - |
| page_index | int \| None, optional | 分 P 号 |
| cid | int \| None, optional | 分 P 编码 |

获取高能进度条

**Returns**: 调用 API 所得的结果。

#### async def like()

| name   | type           | description                 |
| ------ | -------------- | --------------------------- |
| status | bool, optional | 点赞状态。Defaults to True. |

点赞视频。

**Returns:** API 调用返回结果。

#### async def pay_coin()

| name | type           | description                          |
| ---- | -------------- | ------------------------------------ |
| num  | int, optional  | 硬币数量，为 1 ~ 2 个。Defaults to 1 |
| like | bool, optional | 是否同时点赞。Defaults to False      |

投币。

**Returns:** API 调用返回结果。

#### async def share()

分享视频。

**Returns:** int: 当前分享数

#### async def triple()

一键三连

**Returns:** dict: 调用 API 返回的结果

#### async def add_tag()

| name | type | description |
| ---- | ---- | ----------- |
| name | str  | 标签名字。  |

添加标签。

**Returns:** API 调用返回结果。

#### async def delete_tag()

| name   | type | description |
| ------ | ---- | ----------- |
| tag_id | int  | 标签 ID。   |

删除标签。

**Returns:** API 调用返回结果。

#### async def appeal()

| name   | type | description |
| ------ | ---- | ----------- |
| reason | Any | 投诉类型。传入 VideoAppealReasonType 中的项目即可。|
| detail | str | 详情信息。|

投诉稿件

**Returns:** API 调用返回结果。

#### async def set_favorite()

| name          | type                | description                         |
| ------------- | ------------------- | ----------------------------------- |
| add_media_ids | List[int], optional | 要添加到的收藏夹 ID. Defaults to [] |
| del_media_ids | List[int], optional | 要移出的收藏夹 ID. Defaults to []   |

设置视频收藏状况。

**Returns:** API 调用返回结果。

#### async def get_subtitle()

| name       | type | description  |
|------------|------|--------------|
| cid        | cid \| None  | 分 P id. 必须参数 |

无需登陆, 获取视频播放信息 Api 中的字幕数据字段。

**Returns:** API 调用返回结果。

#### async def submit_subtitle()

| name       | type | description                                                |
|------------|------|------------------------------------------------------------|
| lan        | str  | 字幕语言代码，参考 http://www.lingoes.cn/zh/translator/langcode.htm |
| data       | dict | 字幕数据                                                       |
| submit     | bool | 是否提交，不提交为草稿                                                |
| sign       | bool | 是否署名                                                       |
| page_index | int \| None  | 分 P 索引. Defaults to None.                                  |
| cid        | cid \| None  | 分 P id. Defaults to None.                                  |

上传字幕

字幕数据 data 参考：

```json
{
  "font_size": "float: 字体大小，默认 0.4",
  "font_color": "str: 字体颜色，默认 \"#FFFFFF\"",
  "background_alpha": "float: 背景不透明度，默认 0.5",
  "background_color": "str: 背景颜色，默认 \"#9C27B0\"",
  "Stroke": "str: 描边，目前作用未知，默认为 \"none\"",
  "body": [
    {
      "from": "int: 字幕开始时间（秒）",
      "to": "int: 字幕结束时间（秒）",
      "location": "int: 字幕位置，默认为 2",
      "content": "str: 字幕内容"
    }
  ]
}
```

**Returns:** API 调用返回结果。

#### async def add_to_toview()

添加视频至稍后再看

**Returns:** API 调用返回结果。

#### async def delete_from_toview()

从稍后再看列表删除视频

**Returns:** API 调用返回结果。

---

## class VideoOnlineMonitor

视频在线人数实时监测。

**示例代码：**

```python
import asyncio
from bilibili_api import video

# 实例化
r = video.VideoOnlineMonitor("BV1Bf4y1Q7QP")


# 装饰器方法注册事件监听器
@r.on("ONLINE")
async def handler(data):
    print(data)


# 函数方法注册事件监听器
async def handler2(data):
    print(data)
    r.add_event_listener("ONLINE", handler2)


asyncio.get_event_loop().run_until_complete(r.connect())
```

**事件表：**

| name         | description    | callback                        |
| ------------ | -------------- | ------------------------------- |
| ONLINE       | 在线人数更新 | dict                            |
| DANMAKU      | 收到实时弹幕   | Danmaku                         |
| DISCONNECTED | 正常断开连接   | None                            |
| ERROR        | 发生错误       | aiohttp.ClientWebSocketResponse |
| CONNECTED    | 成功连接       | None                            |

### Sub classes

#### class Datapack

**Extends:** enum.Enum

数据包类型枚举。

+ CLIENT_VERIFY  : 客户端发送验证信息。
+ SERVER_VERIFY  : 服务端响应验证信息。
+ CLIENT_HEARTBEAT: 客户端发送心跳包。
+ SERVER_HEARTBEAT: 服务端响应心跳包。
+ DANMAKU: 实时弹幕更新。

### Functions

#### def \_\_init\_\_()

| name       | type                 | description                                    |
| ---------- | -------------------- | ---------------------------------------------- |
| bvid       | str \| None, optional        | BVID                                           |
| aid        | int \| None, optional        | AID                                            |
| page_index | int, optional        | 分 P 序号. Defaults to 0.                      |
| credential | Credential \| None, optional | Credential 类. Defaults to None.               |
| debug      | bool, optional       | 调试模式，将输出更详细信息. Defaults to False. |

#### async def connect()

连接服务器。

**Returns:** None

#### async def disconnect()

断开服务器。

**Returns:** None

---

**@dataclass.dataclass**
## class VideoStreamDownloadURL

视频流 URL 类

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| url  | str  | 视频流 url |
| video_quality | VideoQuality | 视频流清晰度 |
| video_codecs | VideoCodecs | 视频流编码 |

---

**@dataclass.dataclass**
## class AudioStreamDownloadURL

音频流 URL 类

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| url  | str  | 音频流 url |
| audio_quality | AudioQuality | 音频流清晰度 |

---

**@dataclass.dataclass**
## class FLVStreamDownloadURL

FLV 视频流

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| url  | str  | FLV 流 url |

---

**@dataclass.dataclass**
## class HTML5MP4DownloadURL

可供 HTML5 播放的 mp4 视频流

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| url  | str  | HTML5 mp4 视频流 |

---

## class VideoDownloadURLDataDetecter

`Video.get_download_url` 返回结果解析类。

在调用 `Video.get_download_url` 之后可以将代入 `VideoDownloadURLDataDetecter`，此类将一键解析。

目前支持:

- 视频清晰度: 360P, 480P, 720P, 1080P, 1080P 高码率, 1080P 60 帧, 4K, HDR, 杜比视界, 8K
- 视频编码: HEVC(H.265), AVC(H.264), AV1
- 音频清晰度: 64K, 132K, Hi-Res 无损音效, 杜比全景声, 192K
- FLV 视频流
- 番剧/课程试看视频流

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| data | dict | `Video.get_download_url` 返回的结果 |

#### def check_video_and_audio_stream()

判断是否为音视频分离流

**Returns:** bool: 是否为音视频分离流

#### def flv_stream()

判断是否为 FLV 视频流

**Returns:** bool: 是否为 FLV 视频流

#### def check_html5_mp4_stream()

判断是否为 HTML5 可播放的 mp4 视频流

**Returns:** bool: 是否为 HTML5 可播放的 mp4 视频流

#### def check_episode_try_mp4_stream()

判断是否为番剧/课程试看的 mp4 视频流

**Returns:**bool: 是否为番剧试看的 mp4 视频流

#### def detect()

解析数据

**以下参数仅能在音视频流分离的情况下产生作用，flv / mp4 试看流 / html5 mp4 流下以下参数均没有作用**

| name | type | description |
| ---- | ---- | ----------- |
| video_max_quality | VideoQuality | 设置提取的视频流清晰度最大值，设置此参数绝对不会禁止 HDR/杜比. Defaults to VideoQuality._8K. |
| audio_max_quality | AudioQuality | 设置提取的音频流清晰度最大值. 设置此参数绝对不会禁止 Hi-Res/杜比. Defaults to AudioQuality._192K. |
| video_min_quality | VideoQuality | 设置提取的视频流清晰度最小值，设置此参数绝对不会禁止 HDR/杜比. Defaults to VideoQuality._360P. |
| audio_min_quality | AudioQuality | 设置提取的音频流清晰度最小值. 设置此参数绝对不会禁止 Hi-Res/杜比. Defaults to AudioQuality._64K. |
| video_accepted_qualities | List\[VideoQuality\] | 设置允许的所有视频流清晰度. Defaults to ALL. |
| audio_accepted_qualities | List\[AudioQuality\] | 设置允许的所有音频清晰度. Defaults to ALL. |
| codecs | List\[VideoCodecs\] | 设置所有允许提取出来的视频编码. 此项不会忽略 HDR/杜比. Defaults to ALL codecs. |
| no_dolby_video | bool | 是否禁止提取杜比视界视频流. Defaults to False. |
| no_dolby_audio | bool | 是否禁止提取杜比全景声音频流. Defaults to False. |
| no_hdr | bool | 是否禁止提取 HDR 视频流. Defaults to False. |
| no_hires | bool | 是否禁止提取 Hi-Res 音频流. Defaults to False. |

**Returns:** List[VideoStreamDownloadURL | AudioStreamDownloadURL | FLVStreamDownloadURL | HTML5MP4DownloadURL | EpisodeTryMP4DownloadURL]: 提取出来的视频/音频流

#### def detect_all()

解析并返回所有数据

**Returns:** List[VideoStreamDownloadURL | AudioStreamDownloadURL | FLVStreamDownloadURL | HTML5MP4DownloadURL | EpisodeTryMP4DownloadURL]: 所有的视频/音频流

#### def detect_best_streams()

提取出分辨率、音质等信息最好的音视频流

| name | type | description |
| ---- | ---- | ----------- |
| video_max_quality | VideoQuality | 设置提取的视频流清晰度最大值，设置此参数绝对不会禁止 HDR/杜比. Defaults to VideoQuality._8K. |
| audio_max_quality | AudioQuality | 设置提取的音频流清晰度最大值. 设置此参数绝对不会禁止 Hi-Res/杜比. Defaults to AudioQuality._192K. |
| video_min_quality | VideoQuality | 设置提取的视频流清晰度最小值，设置此参数绝对不会禁止 HDR/杜比. Defaults to VideoQuality._360P. |
| audio_min_quality | AudioQuality | 设置提取的音频流清晰度最小值. 设置此参数绝对不会禁止 Hi-Res/杜比. Defaults to AudioQuality._64K. |
| video_accepted_qualities | List\[VideoQuality\] | 设置允许的所有视频流清晰度. Defaults to ALL. |
| audio_accepted_qualities | List\[AudioQuality\] | 设置允许的所有音频清晰度. Defaults to ALL. |
| codecs | List\[VideoCodecs\] | 设置所有允许提取出来的视频编码. 在数组中越靠前的编码选择优先级越高. 此项不会忽略 HDR/杜比. Defaults to [VideoCodecs.AV1, VideoCodecs.AVC, VideoCodecs.HEV]. |
| no_dolby_video | bool | 是否禁止提取杜比视界视频流. Defaults to False. |
| no_dolby_audio | bool | 是否禁止提取杜比全景声音频流. Defaults to False. |
| no_hdr | bool | 是否禁止提取 HDR 视频流. Defaults to False. |
| no_hires | bool | 是否禁止提取 Hi-Res 音频流. Defaults to False. |

**Returns:** List[VideoStreamDownloadURL | AudioStreamDownloadURL | FLVStreamDownloadURL | HTML5MP4DownloadURL | None]: FLV 视频流 / HTML5 MP4 视频流 / 番剧或课程试看 MP4 视频流返回 `[FLVStreamDownloadURL | HTML5MP4StreamDownloadURL | EpisodeTryMP4DownloadURL]`, 否则为 `[VideoStreamDownloadURL, AudioStreamDownloadURL]`, 如果未匹配上任何合适的流则对应的位置位 `None`
