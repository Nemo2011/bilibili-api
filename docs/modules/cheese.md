# Module cheese.py

``` python
from bilibili_api import cheese
```

有关 bilibili 课程的 api。</br>
注意，注意！课程中的视频和其他视频几乎没有任何相通的 API！</br>
获取下载链接需要使用 bilibili_api.cheese.</br>get_download_url，video.get_download_url 不适用。</br>
还有，课程的 season_id 和 ep_id 不与番剧相通，井水不犯河水，</br>请不要错用!</br>

## class CheeseList():

教程类
season_id(int): ssid
ep_id(int): 单集 ep_id

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| season_id | int | 课程的 ssid（不与番剧相通）|
| ep_id | int | 单集的 epid（不与番剧相通） |
| credential | Credential | 凭据 |

注意：season_id 和 ep_id 任选一个即可，两个都选的话
以 season_id 为主

**Returns:** None

#### def set_season_id()

设置 season_id

| name | type | description |
| ---- | ---- | ----------- |
| season_id | int | 课程的 ssid（不与番剧相通）|

**Returns:** None

#### def set_ep_id(self, ep_id: int):

设置 ep_id

| name | type | description |
| ---- | ---- | ----------- |
| season_id | int | 课程的 ssid（不与番剧相通）|
| ep_id | int | 单集的 epid（不与番剧相通） |

**Returns:** None

#### def get_season_id(self):

获取 season_id

**Returns:** season_id

#### async def get_meta()

获取教程元数据。

**Returns**: 调用 API 所得的结果。

#### async def get_list()

获取教程所有视频。

**Returns**: List[CheeseVideo]: 课程视频列表

***

## class CheeseVideo()

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| cheese | CheeseList | 对应的课程 |

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| ep_id | int | epid（不与番剧相通） |
| credential | Credential | 凭据 |

#### def get_cheese()

获取所属课程

**Returns:** 课程类

#### def get_aid()

获取 aid

**Returns:** aid

#### def get_cid()

获取 cid

**Returns:** cid

#### def get_meta()

获取课程元数据

**Returns:** 课程元数据

#### def set_epid()

| name | type | description |
| ---- | ---- | ----------- |
| ep_id | int | 新的 epid（不与番剧相通）|

设置 epid

**Returns**: None

#### def get_epid()

获取 epid

#### async def get_download_url()

获取下载链接

**Returns**: 调用 API 所得的结果。

#### async def get_stat()

获取视频统计数据（播放量，点赞数等）。

**Returns**: 调用 API 所得的结果。

#### async def get_pages()

获取分 P 信息。

**Returns**: 调用 API 所得的结果。

#### async def get_danmaku_view()

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。

**Returns**: 调用 API 所得的结果。

#### async def get_danmakus()

| name | type | description |
| ---- | ---- | ----------- |
| date | datetime.Date, optional | 指定日期后为获取历史弹幕，精确到年月日。Defaults to None. |

获取弹幕。

**Returns**: 调用 API 所得的结果。

#### async def get_pbp()

获取高能进度条

**Returns**: 调用 API 所得的结果。

#### async def has_liked()

视频是否点赞过。

**Returns:** bool: 视频是否点赞过。

#### async def get_pay_coins()

获取视频已投币数量。

**Returns:** int: 视频已投币数量。

#### async def has_favoured()

是否已收藏。

**Returns:** bool: 视频是否已收藏。

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

#### async def set_favorite()

| name          | type                | description                         |
| ------------- | ------------------- | ----------------------------------- |
| add_media_ids | List[int], optional | 要添加到的收藏夹 ID. Defaults to [] |
| del_media_ids | List[int], optional | 要移出的收藏夹 ID. Defaults to []   |

设置视频收藏状况。

**Returns:** API 调用返回结果。

#### async def get_danmaku_xml()

获取弹幕(xml 源)

**Return:** str: xml 文件源
