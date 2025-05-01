# Module video.py


bilibili_api.video

视频相关操作

注意，同时存在 page_index 和 cid 的参数，两者至少提供一个。


``` python
from bilibili_api import video
```

- [class AudioQuality()](#class-AudioQuality)
- [class AudioStreamDownloadURL()](#class-AudioStreamDownloadURL)
- [class DanmakuOperatorType()](#class-DanmakuOperatorType)
- [class FLVStreamDownloadURL()](#class-FLVStreamDownloadURL)
- [class MP4StreamDownloadURL()](#class-MP4StreamDownloadURL)
- [class Video()](#class-Video)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def add\_tag()](#async-def-add\_tag)
  - [async def add\_to\_toview()](#async-def-add\_to\_toview)
  - [async def appeal()](#async-def-appeal)
  - [async def delete\_from\_toview()](#async-def-delete\_from\_toview)
  - [async def delete\_tag()](#async-def-delete\_tag)
  - [async def get\_ai\_conclusion()](#async-def-get\_ai\_conclusion)
  - [def get\_aid()](#def-get\_aid)
  - [def get\_bvid()](#def-get\_bvid)
  - [async def get\_chargers()](#async-def-get\_chargers)
  - [async def get\_cid()](#async-def-get\_cid)
  - [async def get\_danmaku\_snapshot()](#async-def-get\_danmaku\_snapshot)
  - [async def get\_danmaku\_view()](#async-def-get\_danmaku\_view)
  - [async def get\_danmaku\_xml()](#async-def-get\_danmaku\_xml)
  - [async def get\_danmakus()](#async-def-get\_danmakus)
  - [async def get\_detail()](#async-def-get\_detail)
  - [async def get\_download\_url()](#async-def-get\_download\_url)
  - [async def get\_history\_danmaku\_index()](#async-def-get\_history\_danmaku\_index)
  - [async def get\_info()](#async-def-get\_info)
  - [async def get\_online()](#async-def-get\_online)
  - [async def get\_pages()](#async-def-get\_pages)
  - [async def get\_pay\_coins()](#async-def-get\_pay\_coins)
  - [async def get\_pbp()](#async-def-get\_pbp)
  - [async def get\_player\_info()](#async-def-get\_player\_info)
  - [async def get\_private\_notes\_list()](#async-def-get\_private\_notes\_list)
  - [async def get\_public\_notes\_list()](#async-def-get\_public\_notes\_list)
  - [async def get\_related()](#async-def-get\_related)
  - [async def get\_relation()](#async-def-get\_relation)
  - [async def get\_special\_dms()](#async-def-get\_special\_dms)
  - [async def get\_subtitle()](#async-def-get\_subtitle)
  - [async def get\_tags()](#async-def-get\_tags)
  - [async def get\_up\_mid()](#async-def-get\_up\_mid)
  - [async def get\_video\_snapshot()](#async-def-get\_video\_snapshot)
  - [async def has\_favoured()](#async-def-has\_favoured)
  - [async def has\_liked()](#async-def-has\_liked)
  - [async def has\_liked\_danmakus()](#async-def-has\_liked\_danmakus)
  - [async def is\_episode()](#async-def-is\_episode)
  - [async def is\_forbid\_note()](#async-def-is\_forbid\_note)
  - [async def like()](#async-def-like)
  - [async def like\_danmaku()](#async-def-like\_danmaku)
  - [async def operate\_danmaku()](#async-def-operate\_danmaku)
  - [async def pay\_coin()](#async-def-pay\_coin)
  - [async def recall\_danmaku()](#async-def-recall\_danmaku)
  - [async def send\_danmaku()](#async-def-send\_danmaku)
  - [def set\_aid()](#def-set\_aid)
  - [def set\_bvid()](#def-set\_bvid)
  - [async def set\_favorite()](#async-def-set\_favorite)
  - [async def share()](#async-def-share)
  - [async def submit\_subtitle()](#async-def-submit\_subtitle)
  - [async def triple()](#async-def-triple)
  - [async def turn\_to\_episode()](#async-def-turn\_to\_episode)
- [class VideoAppealReasonType()](#class-VideoAppealReasonType)
  - [def PLAGIARISM()](#def-PLAGIARISM)
  - [def UNREAL\_COPYRIGHT()](#def-UNREAL\_COPYRIGHT)
- [class VideoCodecs()](#class-VideoCodecs)
- [class VideoDownloadURLDataDetecter()](#class-VideoDownloadURLDataDetecter)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def check\_flv\_mp4\_stream()](#def-check\_flv\_mp4\_stream)
  - [def check\_video\_and\_audio\_stream()](#def-check\_video\_and\_audio\_stream)
  - [def detect()](#def-detect)
  - [def detect\_all()](#def-detect\_all)
  - [def detect\_best\_streams()](#def-detect\_best\_streams)
- [class VideoOnlineMonitor()](#class-VideoOnlineMonitor)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def connect()](#async-def-connect)
  - [async def disconnect()](#async-def-disconnect)
- [class VideoQuality()](#class-VideoQuality)
- [class VideoStreamDownloadURL()](#class-VideoStreamDownloadURL)
- [async def get\_cid\_info()](#async-def-get\_cid\_info)

---

## class AudioQuality()

**Extend: enum.Enum**

视频的音频流清晰度枚举

- _64K: 64K
- _132K: 132K
- _192K: 192K
- HI_RES: Hi-Res 无损
- DOLBY: 杜比全景声




---

**@dataclasses.dataclass** 

## class AudioStreamDownloadURL()

(@dataclass)

音频流 URL 类


| name | type | description |
| - | - | - |
| `url` | `str` | 音频流 url |
| `audio_quality` | `AudioQuality` | 音频流清晰度 |


---

## class DanmakuOperatorType()

**Extend: enum.Enum**

弹幕操作枚举

+ DELETE - 删除弹幕
+ PROTECT - 保护弹幕
+ UNPROTECT - 取消保护弹幕




---

**@dataclasses.dataclass** 

## class FLVStreamDownloadURL()

(@dataclass)

FLV 视频流


| name | type | description |
| - | - | - |
| `url` | `str` | FLV 流 url |


---

**@dataclasses.dataclass** 

## class MP4StreamDownloadURL()

(@dataclass)

MP4 视频流


| name | type | description |
| - | - | - |
| `url` | `str` | HTML5 mp4 视频流 |


---

## class Video()

视频类，各种对视频的操作均在里面。




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `bvid` | `str \| None, optional` | BV 号. bvid 和 aid 必须提供其中之一。 |
| `aid` | `int \| None, optional` | AV 号. bvid 和 aid 必须提供其中之一。 |
| `credential` | `Credential \| None, optional` | Credential 类. Defaults to None. |


### async def add_tag()

添加标签。


| name | type | description |
| - | - | - |
| `name` | `str` | 标签名字。 |

**Returns:** `dict`:  调用 API 返回的结果。会返回标签 ID。




### async def add_to_toview()

添加视频至稍后再看列表



**Returns:** `dict`:  调用 API 返回的结果




### async def appeal()

投诉稿件


| name | type | description |
| - | - | - |
| `reason` | `Any` | 投诉类型。传入 VideoAppealReasonType 中的项目即可。 |
| `detail` | `str` | 详情信息。 |

**Returns:** `dict`:  调用 API 返回的结果




### async def delete_from_toview()

从稍后再看列表删除视频



**Returns:** `dict`:  调用 API 返回的结果




### async def delete_tag()

删除标签。


| name | type | description |
| - | - | - |
| `tag_id` | `int` | 标签 ID。 |

**Returns:** `dict`:  调用 API 返回的结果。




### async def get_ai_conclusion()

获取稿件 AI 总结结果。

cid 和 page_index 至少提供其中一个，其中 cid 优先级最高


| name | type | description |
| - | - | - |
| `cid` | `Optional, int` | 分 P 的 cid。 |
| `page_index` | `Optional, int` | 分 P 号，从 0 开始。 |
| `up_mid` | `Optional, int` | up 主的 mid。 |

**Returns:** `dict`:  调用 API 返回的结果。




### def get_aid()

获取 AID。



**Returns:** `int`:  aid。




### def get_bvid()

获取 BVID。



**Returns:** `str`:  BVID。




### async def get_chargers()

获取视频充电用户。



**Returns:** `dict`:  调用 API 返回的结果。




### async def get_cid()

获取稿件 cid


| name | type | description |
| - | - | - |
| `page_index` | `int` | 分 P |

**Returns:** `int`:  cid




### async def get_danmaku_snapshot()

获取弹幕快照



**Returns:** `dict`:  调用 API 返回的结果




### async def get_danmaku_view()

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。


| name | type | description |
| - | - | - |
| `page_index` | `int, optional` | 分 P 号，从 0 开始。Defaults to None |
| `cid` | `int, optional` | 分 P 的 ID。Defaults to None |

**Returns:** `dict`:  调用 API 返回的结果。




### async def get_danmaku_xml()

获取所有弹幕的 xml 源文件（非装填）


| name | type | description |
| - | - | - |
| `page_index` | `int, optional` | 分 P 序号. Defaults to 0. |
| `cid` | `int \| None, optional` | cid. Defaults to None. |

**Returns:** `str`:  xml 文件源




### async def get_danmakus()

获取弹幕。


| name | type | description |
| - | - | - |
| `page_index` | `int, optional` | 分 P 号，从 0 开始。Defaults to None |
| `date` | `datetime.Date \| None, optional` | 指定日期后为获取历史弹幕，精确到年月日。Defaults to None. |
| `cid` | `int \| None, optional` | 分 P 的 ID。Defaults to None |
| `from_seg` | `int, optional` | 从第几段开始(0 开始编号，None 为从第一段开始，一段 6 分钟). Defaults to None. |
| `to_seg` | `int, optional` | 到第几段结束(0 开始编号，None 为到最后一段，包含编号的段，一段 6 分钟). Defaults to None. |

**Returns:** `List[Danmaku]`:  Danmaku 类的列表。


注意：
- 1. 段数可以通过视频时长计算。6分钟为一段。
- 2. `from_seg` 和 `to_seg` 仅对 `date == None` 的时候有效果。
- 3. 例：取前 `12` 分钟的弹幕：`from_seg=0, to_seg=1`



### async def get_detail()

获取视频详细信息



**Returns:** `dict`:  调用 API 返回的结果。




### async def get_download_url()

获取视频下载信息。

返回结果可以传入 `VideoDownloadURLDataDetecter` 进行解析。

page_index 和 cid 至少提供其中一个，其中 cid 优先级最高


| name | type | description |
| - | - | - |
| `page_index` | `int \| None, optional` | 分 P 号，从 0 开始。Defaults to None |
| `cid` | `int \| None, optional` | 分 P 的 ID。Defaults to None |

**Returns:** `dict`:  调用 API 返回的结果。




### async def get_history_danmaku_index()

获取特定月份存在历史弹幕的日期。


| name | type | description |
| - | - | - |
| `page_index` | `int \| None, optional` | 分 P 号，从 0 开始。Defaults to None |
| `date` | `datetime.date \| None` | 精确到年月. Defaults to None。 |
| `cid` | `int \| None, optional` | 分 P 的 ID。Defaults to None |

**Returns:** `None | List[str]`:  调用 API 返回的结果。不存在时为 None。




### async def get_info()

获取视频信息。



**Returns:** `dict`:  调用 API 返回的结果。




### async def get_online()

获取实时在线人数



**Returns:** `dict`:  调用 API 返回的结果。




### async def get_pages()

获取分 P 信息。



**Returns:** `dict`:  调用 API 返回的结果。




### async def get_pay_coins()

获取视频已投币数量。



**Returns:** `int`:  视频已投币数量。




### async def get_pbp()

获取高能进度条


| name | type | description |
| - | - | - |
| `page_index` | `int \| None` | 分 P 号 |
| `cid` | `int \| None` | 分 P 编码 |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_player_info()

获取视频上一次播放的记录，字幕和地区信息。需要分集的 cid, 返回数据中含有json字幕的链接


| name | type | description |
| - | - | - |
| `cid` | `int \| None` | 分 P ID,从视频信息中获取 |
| `epid` | `int \| None` | 番剧分集 ID,从番剧信息中获取 |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_private_notes_list()

获取稿件私有笔记列表。



**Returns:** `list`:  note_Ids。




### async def get_public_notes_list()

获取稿件公开笔记列表。


| name | type | description |
| - | - | - |
| `pn` | `int` | 页码 |
| `ps` | `int` | 每页项数 |

**Returns:** `dict`:  调用 API 返回的结果。




### async def get_related()

获取相关视频信息。



**Returns:** `dict`:  调用 API 返回的结果。




### async def get_relation()

获取用户与视频的关系



**Returns:** `dict`:  调用 API 返回的结果。




### async def get_special_dms()

获取特殊弹幕


| name | type | description |
| - | - | - |
| `page_index` | `int, optional` | 分 P 号. Defaults to 0. |
| `cid` | `int \| None, optional` | 分 P id. Defaults to None. |

**Returns:** `List[SpecialDanmaku]`:  调用接口解析后的结果




### async def get_subtitle()

获取字幕信息


| name | type | description |
| - | - | - |
| `cid` | `int \| None` | 分 P ID,从视频信息中获取 |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_tags()

获取视频标签。


| name | type | description |
| - | - | - |
| `page_index` | `int \| None` | 分 P 序号. Defaults to 0. |
| `cid` | `int \| None` | 分 P 编码. Defaults to None. |

**Returns:** `List[dict]`:  调用 API 返回的结果。




### async def get_up_mid()

获取视频 up 主的 mid。



**Returns:** `int`:  up_mid




### async def get_video_snapshot()

获取视频快照(视频各个时间段的截图拼图)


| name | type | description |
| - | - | - |
| `cid` | `int` | 分 P CID(可选) |
| `json_index` | `bool` | json 数组截取时间表 True 为需要，False 不需要 |
| `pvideo` | `bool` | 是否只获取预览 |

**Returns:** `dict`:  调用 API 返回的结果,数据中 Url 没有 http 头




### async def has_favoured()

是否已收藏。



**Returns:** `bool`:  视频是否已收藏。




### async def has_liked()

视频是否点赞过。



**Returns:** `bool`:  视频是否点赞过。




### async def has_liked_danmakus()

是否已点赞弹幕。


| name | type | description |
| - | - | - |
| `page_index` | `int \| None, optional` | 分 P 号，从 0 开始。Defaults to None |
| `ids` | `List[int] \| None` | 要查询的弹幕 ID 列表。 |
| `cid` | `int \| None, optional` | 分 P 的 ID。Defaults to None |

**Returns:** `dict`:  调用 API 返回的结果。




### async def is_episode()

判断视频是否是番剧



**Returns:** `bool`:  是否是番剧




### async def is_forbid_note()

是否禁止笔记。



**Returns:** `bool`:  是否禁止笔记。




### async def like()

点赞视频。


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 点赞状态。Defaults to True. |

**Returns:** `dict`:  调用 API 返回的结果。




### async def like_danmaku()

点赞弹幕。


| name | type | description |
| - | - | - |
| `page_index` | `int \| None, optional` | 分 P 号，从 0 开始。Defaults to None |
| `dmid` | `int \| None` | 弹幕 ID。 |
| `status` | `bool \| None, optional` | 点赞状态。Defaults to True |
| `cid` | `int \| None, optional` | 分 P 的 ID。Defaults to None |

**Returns:** `dict`:  调用 API 返回的结果。




### async def operate_danmaku()

操作弹幕


| name | type | description |
| - | - | - |
| `page_index` | `int \| None, optional` | 分 P 号，从 0 开始。Defaults to None |
| `dmids` | `List[int] \| None` | 弹幕 ID 列表。 |
| `cid` | `int \| None, optional` | 分 P 的 ID。Defaults to None |
| `type_` | `DanmakuOperatorType \| None` | 操作类型 |

**Returns:** `dict`:  调用 API 返回的结果。




### async def pay_coin()

投币。


| name | type | description |
| - | - | - |
| `num` | `int, optional` | 硬币数量，为 1 ~ 2 个。Defaults to 1. |
| `like` | `bool, optional` | 是否同时点赞。Defaults to False. |

**Returns:** `dict`:  调用 API 返回的结果。




### async def recall_danmaku()

撤回弹幕


| name | type | description |
| - | - | - |
| `page_index` | `int \| None, optional` | 分 P 号 |
| `dmid` | `int` | 弹幕 id |
| `cid` | `int \| None, optional` | 分 P 编码 |

**Returns:** `dict`:  调用 API 返回的结果




### async def send_danmaku()

发送弹幕。


| name | type | description |
| - | - | - |
| `page_index` | `int \| None, optional` | 分 P 号，从 0 开始。Defaults to None |
| `danmaku` | `Danmaku \| None` | Danmaku 类。 |
| `cid` | `int \| None, optional` | 分 P 的 ID。Defaults to None |

**Returns:** `dict`:  调用 API 返回的结果。




### def set_aid()

设置 aid。


| name | type | description |
| - | - | - |
| `aid` | `int` | AV 号。 |




### def set_bvid()

设置 bvid。


| name | type | description |
| - | - | - |
| `bvid` | `str` | 要设置的 bvid。 |




### async def set_favorite()

设置视频收藏状况。

**如果视频是番剧 `await is_bangumi()`，请转为 `Episode` 类收藏**


| name | type | description |
| - | - | - |
| `add_media_ids` | `List[int], optional` | 要添加到的收藏夹 ID. Defaults to []. |
| `del_media_ids` | `List[int], optional` | 要移出的收藏夹 ID. Defaults to []. |

**Returns:** `dict`:  调用 API 返回结果。




### async def share()

分享视频



**Returns:** `int`:  当前分享数




### async def submit_subtitle()

上传字幕

字幕数据 data 参考：

```json
{
  "font_size": "float: 字体大小，默认 0.4",
  "font_color": "str: 字体颜色，默认 "#FFFFFF"",
  "background_alpha": "float: 背景不透明度，默认 0.5",
  "background_color": "str: 背景颜色，默认 "#9C27B0"",
  "Stroke": "str: 描边，目前作用未知，默认为 "none"",
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


| name | type | description |
| - | - | - |
| `lan` | `str` | 字幕语言代码，参考 https |
| `data` | `Dict` | 字幕数据 |
| `submit` | `bool` | 是否提交，不提交为草稿 |
| `sign` | `bool` | 是否署名 |
| `page_index` | `int \| None, optional` | 分 P 索引. Defaults to None. |
| `cid` | `int \| None, optional` | 分 P id. Defaults to None. |

**Returns:** `dict`:  API 调用返回结果





### async def triple()

给阿婆主送上一键三连



**Returns:** `dict`:  调用 API 返回的结果




### async def turn_to_episode()

将视频转换为番剧



**Returns:** `Episode`:  番剧对象




---

## class VideoAppealReasonType()

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
- UNREAL_EVENT(): 虚假不实消息
- OTHER(): 有其他问题
- LEAD_WAR(): 引战
- CANNOT_CHARGE(): 不能参加充电
- UNREAL_COPYRIGHT(source: str): 转载/自制类型错误
- ILLEGAL_POPULARIZE(): 违规推广
- ILLEGAL_OTHER(): 其他不规范行为
- DANGEROUS(): 危险行为
- OTHER_NEW(): 其他
- COOPERATE_INFRINGEMENT(): 企业商誉侵权
- INFRINGEMENT(): 侵权申诉
- VIDEO_INFRINGEMENT(): 盗搬稿件-路人举报
- DISCOMFORT(): 观感不适
- ILLEGAL_URL(): 违法信息外链




**@staticmethod** 

### def PLAGIARISM()

与站内其他视频撞车


| name | type | description |
| - | - | - |
| `bvid` | `str` | 撞车对象 |




**@staticmethod** 

### def UNREAL_COPYRIGHT()

转载/自制类型错误


| name | type | description |
| - | - | - |
| `source` | `str` | 原创视频出处 |




---

## class VideoCodecs()

**Extend: enum.Enum**

视频的视频流编码枚举

- HEV: HEVC(H.265)
- AVC: AVC(H.264)
- AV1: AV1




---

## class VideoDownloadURLDataDetecter()

`Video.get_download_url` 返回结果解析类。

在调用 `Video.get_download_url` 之后可以将代入 `VideoDownloadURLDataDetecter`，此类将一键解析。

目前支持:
  - 视频清晰度: 360P, 480P, 720P, 1080P, 1080P 高码率, 1080P 60 帧, 4K, HDR, 杜比视界, 8K
  - 视频编码: HEVC(H.265), AVC(H.264), AV1
  - 音频清晰度: 64K, 132K, Hi-Res 无损音效, 杜比全景声, 192K
  - FLV 视频流
  - 番剧/课程试看视频流




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `data` | `Dict` | `Video.get_download_url` 返回的结果 |


### def check_flv_mp4_stream()

判断是否为 FLV / MP4 流



**Returns:** `bool`:  是否为 FLV / MP4 流




### def check_video_and_audio_stream()

判断是否为 DASH （音视频分离）



**Returns:** `bool`:  是否为 DASH




### def detect()

解析数据


| name | type | description |
| - | - | - |
| `video_max_quality` | `VideoQuality, optional` | 设置提取的视频流清晰度最大值，设置此参数绝对不会禁止 HDR/杜比. Defaults to VideoQuality._8K. |
| `audio_max_quality` | `AudioQuality, optional` | 设置提取的音频流清晰度最大值. 设置此参数绝对不会禁止 Hi-Res/杜比. Defaults to AudioQuality._192K. |
| `video_min_quality` | `VideoQuality, optional` | 设置提取的视频流清晰度最小值，设置此参数绝对不会禁止 HDR/杜比. Defaults to VideoQuality._360P. |
| `audio_min_quality` | `AudioQuality, optional` | 设置提取的音频流清晰度最小值. 设置此参数绝对不会禁止 Hi-Res/杜比. Defaults to AudioQuality._64K. |
| `video_accepted_qualities` | `List[VideoQuality], optional` | 设置允许的所有视频流清晰度. Defaults to ALL. |
| `audio_accepted_qualities` | `List[AudioQuality], optional` | 设置允许的所有音频清晰度. Defaults to ALL. |
| `codecs` | `List[VideoCodecs], optional` | 设置所有允许提取出来的视频编码. 此项不会忽略 HDR/杜比. Defaults to ALL codecs. |
| `no_dolby_video` | `bool, optional` | 是否禁止提取杜比视界视频流. Defaults to False. |
| `no_dolby_audio` | `bool, optional` | 是否禁止提取杜比全景声音频流. Defaults to False. |
| `no_hdr` | `bool, optional` | 是否禁止提取 HDR 视频流. Defaults to False. |
| `no_hires` | `bool, optional` | 是否禁止提取 Hi-Res 音频流. Defaults to False. |

**Returns:** `List[VideoStreamDownloadURL | AudioStreamDownloadURL | FLVStreamDownloadURL | HTML5MP4DownloadURL | EpisodeTryMP4DownloadURL]`:  提取出来的视频/音频流


**参数仅能在音视频流分离的情况下产生作用，flv / mp4 流下以下参数均没有作用**



### def detect_all()

解析并返回所有数据



**Returns:** `List[VideoStreamDownloadURL | AudioStreamDownloadURL | FLVStreamDownloadURL | HTML5MP4DownloadURL | EpisodeTryMP4DownloadURL]`:  所有的视频/音频流




### def detect_best_streams()

提取出分辨率、音质等信息最好的音视频流。


| name | type | description |
| - | - | - |
| `video_max_quality` | `VideoQuality` | 设置提取的视频流清晰度最大值，设置此参数绝对不会禁止 HDR/杜比. Defaults to VideoQuality._8K. |
| `audio_max_quality` | `AudioQuality` | 设置提取的音频流清晰度最大值. 设置此参数绝对不会禁止 Hi-Res/杜比. Defaults to AudioQuality._192K. |
| `video_min_quality` | `VideoQuality, optional` | 设置提取的视频流清晰度最小值，设置此参数绝对不会禁止 HDR/杜比. Defaults to VideoQuality._360P. |
| `audio_min_quality` | `AudioQuality, optional` | 设置提取的音频流清晰度最小值. 设置此参数绝对不会禁止 Hi-Res/杜比. Defaults to AudioQuality._64K. |
| `video_accepted_qualities` | `List[VideoQuality], optional` | 设置允许的所有视频流清晰度. Defaults to ALL. |
| `audio_accepted_qualities` | `List[AudioQuality], optional` | 设置允许的所有音频清晰度. Defaults to ALL. |
| `codecs` | `List[VideoCodecs]` | 设置所有允许提取出来的视频编码. 在数组中越靠前的编码选择优先级越高. 此项不会忽略 HDR/杜比. Defaults to [VideoCodecs.AV1, VideoCodecs.AVC, VideoCodecs.HEV]. |
| `no_dolby_video` | `bool` | 是否禁止提取杜比视界视频流. Defaults to False. |
| `no_dolby_audio` | `bool` | 是否禁止提取杜比全景声音频流. Defaults to False. |
| `no_hdr` | `bool` | 是否禁止提取 HDR 视频流. Defaults to False. |
| `no_hires` | `bool` | 是否禁止提取 Hi-Res 音频流. Defaults to False. |

**Returns:** `List[VideoStreamDownloadURL | AudioStreamDownloadURL | FLVStreamDownloadURL | HTML5MP4DownloadURL | None]`:  FLV 视频流 / HTML5 MP4 视频流 / 番剧或课程试看 MP4 视频流返回 `[FLVStreamDownloadURL | HTML5MP4StreamDownloadURL | EpisodeTryMP4DownloadURL]`, 否则为 `[VideoStreamDownloadURL, AudioStreamDownloadURL]`, 如果未匹配上任何合适的流则对应的位置位 `None`


**以上参数仅能在音视频流分离的情况下产生作用，flv / mp4 试看流 / html5 mp4 流下以下参数均没有作用**



---

## class VideoOnlineMonitor()

**Extend: bilibili_api.utils.AsyncEvent.AsyncEvent**

视频在线人数实时监测。

示例代码：

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

Extends: AsyncEvent

Logger: VideoOnlineMonitor().logger

Events:
ONLINE：在线人数更新。  CallbackData: dict。
DANMAKU：   收到实时弹幕。  CallbackData: Danmaku。
DISCONNECTED：  正常断开连接。  CallbackData: None。
ERROR:  发生错误。 CallbackData: None。
CONNECTED:  成功连接。 CallbackData: None。




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `bvid` | `str \| None, optional` | BVID. Defaults to None. |
| `aid` | `int \| None, optional` | AID. Defaults to None. |
| `page_index` | `int, optional` | 分 P 序号. Defaults to 0. |
| `credential` | `Credential \| None, optional` | Credential 类. Defaults to None. |
| `debug` | `bool, optional` | 调试模式，将输出更详细信息. Defaults to False. |


### async def connect()

连接服务器






### async def disconnect()

断开服务器






---

## class VideoQuality()

**Extend: enum.Enum**

视频的视频流分辨率枚举

- _360P: 流畅 360P
- _480P: 清晰 480P
- _720P: 高清 720P60
- _1080P: 高清 1080P
- AI_REPAIR: 智能修复（人工智能修复画质）
- _1080P_PLUS: 高清 1080P 高码率
- _1080P_60: 高清 1080P 60 帧码率
- _4K: 超清 4K
- HDR: 真彩 HDR
- DOLBY: 杜比视界
- _8K: 超高清 8K




---

**@dataclasses.dataclass** 

## class VideoStreamDownloadURL()

(@dataclass)

视频流 URL 类


| name | type | description |
| - | - | - |
| `url` | `str` | 视频流 url |
| `video_quality` | `VideoQuality` | 视频流清晰度 |
| `video_codecs` | `VideoCodecs` | 视频流编码 |


---

## async def get_cid_info()

获取 cid 信息 (对应的视频，具体分 P 序号，up 等)



**Returns:** `dict`:  调用 https//hd.biliplus.com 的 API 返回的结果




