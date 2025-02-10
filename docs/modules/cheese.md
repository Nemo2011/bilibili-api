# Module cheese.py


bilibili_api.cheese

有关 bilibili 课程的 api。

注意，注意！课程中的视频和其他视频几乎没有任何相通的 API！

不能将 CheeseVideo 换成 Video 类。(CheeseVideo 类保留了所有的通用的 API)

获取下载链接需要使用 bilibili_api.cheese.get_download_url，video.get_download_url 不适用。

还有，课程的 season_id 和 ep_id 不与番剧相通，井水不犯河水，请不要错用!


``` python
from bilibili_api import cheese
```

- [class CheeseList()](#class-CheeseList)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_list()](#async-def-get\_list)
  - [async def get\_list\_raw()](#async-def-get\_list\_raw)
  - [async def get\_meta()](#async-def-get\_meta)
  - [async def get\_season\_id()](#async-def-get\_season\_id)
  - [async def set\_ep\_id()](#async-def-set\_ep\_id)
  - [async def set\_season\_id()](#async-def-set\_season\_id)
- [class CheeseVideo()](#class-CheeseVideo)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_aid()](#async-def-get\_aid)
  - [async def get\_cheese()](#async-def-get\_cheese)
  - [async def get\_cid()](#async-def-get\_cid)
  - [async def get\_danmaku\_view()](#async-def-get\_danmaku\_view)
  - [async def get\_danmaku\_xml()](#async-def-get\_danmaku\_xml)
  - [async def get\_danmakus()](#async-def-get\_danmakus)
  - [async def get\_download\_url()](#async-def-get\_download\_url)
  - [def get\_epid()](#def-get\_epid)
  - [async def get\_meta()](#async-def-get\_meta)
  - [async def get\_pages()](#async-def-get\_pages)
  - [async def get\_pay\_coins()](#async-def-get\_pay\_coins)
  - [async def get\_pbp()](#async-def-get\_pbp)
  - [async def get\_stat()](#async-def-get\_stat)
  - [async def has\_favoured()](#async-def-has\_favoured)
  - [async def has\_liked()](#async-def-has\_liked)
  - [async def like()](#async-def-like)
  - [async def pay\_coin()](#async-def-pay\_coin)
  - [async def send\_danmaku()](#async-def-send\_danmaku)
  - [async def set\_epid()](#async-def-set\_epid)
  - [async def set\_favorite()](#async-def-set\_favorite)

---

## class CheeseList()

课程类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()

注意：season_id 和 ep_id 任选一个即可，两个都选的话
以 season_id 为主


| name | type | description |
| - | - | - |
| `season_id` | `int` | ssid |
| `ep_id` | `int` | 单集 ep_id |
| `credential` | `Credential` | 凭据类 |


### async def get_list()

获取教程所有视频



**Returns:** `List[CheeseVideo]`:  课程视频列表




### async def get_list_raw()

获取教程所有视频 (返回原始数据)



**Returns:** `dict`:  调用 API 返回的结果




### async def get_meta()

获取教程元数据



**Returns:** `dict`:  调用 API 返回的结果




### async def get_season_id()

获取季度 id



**Returns:** `int`:  季度 id




### async def set_ep_id()

设置 epid 并通过 epid 找到课程


| name | type | description |
| - | - | - |
| `ep_id` | `int` | epid |




### async def set_season_id()

设置季度 id


| name | type | description |
| - | - | - |
| `season_id` | `int` | 季度 id |




---

## class CheeseVideo()

教程视频类
因为不和其他视频相通，所以这里是一个新的类，无继承


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |
| `cheese` | `CheeseList` | 所属的课程 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `epid` | `int` | 单集 ep_id |
| `credential` | `Credential` | 凭据类 |


### async def get_aid()

获取 aid



**Returns:** `int`:  aid




### async def get_cheese()

获取所属课程



**Returns:** `CheeseList`:  所属课程




### async def get_cid()

获取 cid



**Returns:** `int`:  cid




### async def get_danmaku_view()

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。



**Returns:** `dict`:  调用 API 返回的结果。




### async def get_danmaku_xml()

获取所有弹幕的 xml 源文件（非装填）



**Returns:** `str`:  文件源




### async def get_danmakus()

获取弹幕。


| name | type | description |
| - | - | - |
| `date` | `datetime.Date \| None, optional` | 指定日期后为获取历史弹幕，精确到年月日。Defaults to None. |
| `from_seg` | `int, optional` | 从第几段开始(0 开始编号，None 为从第一段开始，一段 6 分钟). Defaults to None. |
| `to_seg` | `int, optional` | 到第几段结束(0 开始编号，None 为到最后一段，包含编号的段，一段 6 分钟). Defaults to None. |

**Returns:** `List[Danmaku]`:  Danmaku 类的列表。


注意：
- 1. 段数可以通过视频时长计算。6分钟为一段。
- 2. `from_seg` 和 `to_seg` 仅对 `date == None` 的时候有效果。
- 3. 例：取前 `12` 分钟的弹幕：`from_seg=0, to_seg=1`



### async def get_download_url()

获取下载链接



**Returns:** `dict`:  调用 API 返回的结果。




### def get_epid()

获取 epid



**Returns:** `int`:  epid




### async def get_meta()

获取课程元数据



**Returns:** `dict`:  视频元数据




### async def get_pages()

获取分 P 信息。



**Returns:** `dict`:  调用 API 返回的结果。




### async def get_pay_coins()

获取视频已投币数量。



**Returns:** `int`:  视频已投币数量。




### async def get_pbp()

获取高能进度条



**Returns:** `dict`:  调用 API 返回的结果




### async def get_stat()

获取视频统计数据（播放量，点赞数等）。



**Returns:** `dict`:  调用 API 返回的结果。




### async def has_favoured()

是否已收藏。



**Returns:** `bool`:  视频是否已收藏。




### async def has_liked()

视频是否点赞过。



**Returns:** `bool`:  视频是否点赞过。




### async def like()

点赞视频。


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 点赞状态。Defaults to True. |

**Returns:** `dict`:  调用 API 返回的结果。




### async def pay_coin()

投币。


| name | type | description |
| - | - | - |
| `num` | `int, optional` | 硬币数量，为 1 ~ 2 个。Defaults to 1. |
| `like` | `bool, optional` | 是否同时点赞。Defaults to False. |

**Returns:** `dict`:  调用 API 返回的结果。




### async def send_danmaku()

发送弹幕。


| name | type | description |
| - | - | - |
| `danmaku` | `Danmaku \| None` | Danmaku 类。Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果。




### async def set_epid()

设置 epid


| name | type | description |
| - | - | - |
| `epid` | `int` | epid |




### async def set_favorite()

设置视频收藏状况。


| name | type | description |
| - | - | - |
| `add_media_ids` | `List[int], optional` | 要添加到的收藏夹 ID. Defaults to []. |
| `del_media_ids` | `List[int], optional` | 要移出的收藏夹 ID. Defaults to []. |

**Returns:** `dict`:  调用 API 返回结果。




