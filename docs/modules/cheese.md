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

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| season_id | int | 课程的 ssid（不与番剧相通）|
| ep_id | int | 单集的 epid（不与番剧相通） |
| credential | Credential | 凭据 |

注意：season_id 和 ep_id 任选一个即可，两个都选的话
以 season_id 为主

#### async def get_meta()

获取教程元数据。

**Returns**: 调用 API 所得的结果。

#### async def get_list()

获取教程所有视频。

**Returns**: 调用 API 所得的结果。

***

## class CheeseVideo()

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| ep_id | int | epid（不与番剧相通） |
| credential | Credential | 凭据 |

#### def set_epid()

| name | type | description |
| ---- | ---- | ----------- |
| ep_id | int | 新的 epid（不与番剧相通）|

设置 epid

**Returns**: None

#### async def get_download_url()

获取下载链接

**Returns**: 调用 API 所得的结果。
