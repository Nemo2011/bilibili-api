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

--

## class CheeseList()

课程类


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |


### async def get_list()

获取教程所有视频



**Returns:** List[CheeseVideo]: 课程视频列表




### async def get_list_raw()

获取教程所有视频 (返回原始数据)



**Returns:** dict: 调用 API 返回的结果




### async def get_meta()

获取教程元数据



**Returns:** 调用 API 所得的结果。




### def get_season_id()

获取季度 id



**Returns:** int: 季度 id




### def set_ep_id()

设置 epid 并通过 epid 找到课程


| name | type | description |
| - | - | - |
| ep_id | int | epid |

**Returns:** None



### def set_season_id()

设置季度 id


| name | type | description |
| - | - | - |
| season_id | int | 季度 id |

**Returns:** None



--

## class CheeseVideo()

教程视频类
因为不和其他视频相通，所以这里是一个新的类，无继承


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |
| cheese | CheeseList | 所属的课程 |


### def get_aid()

获取 aid



**Returns:** int: aid




### def get_cheese()

获取所属课程



**Returns:** CheeseList: 所属课程




### def get_cid()

获取 cid



**Returns:** int: cid




### async def get_danmaku_view()

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。



**Returns:** dict: 调用 API 返回的结果。




### async def get_danmaku_xml()

获取弹幕(xml 源)



**Returns:** str: xml 文件源




### async def get_danmakus()

获取弹幕。


| name | type | description |
| - | - | - |
| date | Union[datetime.Date, None] | 指定日期后为获取历史弹幕，精确到年月日。Defaults to None. |

**Returns:** List[Danmaku]: Danmaku 类的列表。




### async def get_download_url()

获取下载链接



**Returns:** dict: 调用 API 返回的结果。




### def get_epid()

获取 epid



**Returns:** int: epid




### def get_meta()

获取课程元数据



**Returns:** dict: 视频元数据




### async def get_pages()

获取分 P 信息。



**Returns:** dict: 调用 API 返回的结果。




### async def get_pay_coins()

获取视频已投币数量。



**Returns:** int: 视频已投币数量。




### async def get_pbp()

获取高能进度条



**Returns:** 调用 API 返回的结果




### async def get_stat()

获取视频统计数据（播放量，点赞数等）。



**Returns:** dict: 调用 API 返回的结果。




### async def has_favoured()

是否已收藏。



**Returns:** bool: 视频是否已收藏。




### async def has_liked()

视频是否点赞过。



**Returns:** bool: 视频是否点赞过。




### async def like()

点赞视频。


| name | type | description |
| - | - | - |
| status | Union[bool, None] | 点赞状态。Defaults to True. |

**Returns:** dict: 调用 API 返回的结果。




### async def pay_coin()

投币。


| name | type | description |
| - | - | - |
| num | Union[int, None] | 硬币数量，为 1 ~ 2 个。Defaults to 1. |
| like | Union[bool, None] | 是否同时点赞。Defaults to False. |

**Returns:** dict: 调用 API 返回的结果。




### async def send_danmaku()

发送弹幕。


| name | type | description |
| - | - | - |
| danmaku | Danmaku \| None | Danmaku 类。Defaults to None. |

**Returns:** dict: 调用 API 返回的结果。




### def set_epid()

设置 epid


| name | type | description |
| - | - | - |
| epid | int | epid |

**Returns:** None



### async def set_favorite()

设置视频收藏状况。


| name | type | description |
| - | - | - |
| add_media_ids | Union[List[int], None] | 要添加到的收藏夹 ID. Defaults to []. |
| del_media_ids | Union[List[int], None] | 要移出的收藏夹 ID. Defaults to []. |

**Returns:** dict: 调用 API 返回结果。




