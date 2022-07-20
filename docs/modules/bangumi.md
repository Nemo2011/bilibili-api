# Module bangumi.py

```python
from bilibili_api import bangumi
```
番剧相关

概念：
+ media_id: 番剧本身的 ID，有时候也是每季度的 ID，如 https://www.bilibili.com/bangumi/media/md28231846/
+ season_id: 每季度的 ID，只能通过 get_meta() 获取。
+ episode_id: 每集的 ID，如 https://www.bilibili.com/bangumi/play/ep374717

## class BangumiCommentOrder

短评 / 长评 排序方式

+ DEFAULT: 默认
+ CTIME: 发布时间倒序

---

## class Bangumi

番剧类

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| media_id | int | 教程 ID（不与番剧相通） |
| ssid | int | 教程季度 ID（不与番剧相通） |
| credential | Credential | 凭据 |

#### def get_media_id()

获取 media_id

**Returns:** media_id

#### def get_season_id()

获取 season_id

**Returns:** season_id

#### _async_ def set_ssid()

设置 season_id

**Returns:** None

#### _async_ def set_media_id()

设置 media_id

**Returns:** None

#### _async_ def get_meta()

获取番剧元数据信息（评分，封面URL，标题等）

**Returns:** API 调用返回结果。

#### _async_ def get_short_comment_list()

| name       | type                          | description                                                  |
| ---------- | ----------------------------- | ------------------------------------------------------------ |
| order      | BangumiCommentOrder, optional | 排序方式。Defaults to BangumiCommentOrder.DEFAULT            |
| next       | str, optional                 | 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None |

获取短评列表

**Returns:** API 调用返回结果。

#### _async_ def get_long_comment_list()

| name       | type                          | description                                                  |
| ---------- | ----------------------------- | ------------------------------------------------------------ |
| order      | BangumiCommentOrder, optional | 排序方式。Defaults to BangumiCommentOrder.DEFAULT            |
| next       | str, optional                 | 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None |

获取长评列表

**Returns:** API 调用返回结果。

#### _async_ def get_episode_list()

获取季度分集列表

**Returns:** API 调用返回结果。

#### _async_ def get_stat()

获取番剧播放量，追番等信息

**Returns:** API 调用返回结果。

#### _async_ def get_overview()

获取番剧全面概括信息，包括发布时间、剧集情况、stat 等情况

**Returns:** API 调用返回结果。

***

## _async_ def set_follow()

| name       | type                 | description                |
| ---------- | -------------------- | -------------------------- |
| bangumi | Bangumi | 番剧类 |
| status     | bool, optional       | 追番状态，Defaults to True |
| credential | Credential, optional | 凭据. Defaults to None     |

追番状态设置

**Returns:** API 调用返回结果。

## class Episode

**Extends: bilibili_api.video.Video**

番剧剧集类

### Functions

**这里仅列出新增的或重写过的函数，Video 类的其他函数都可使用**

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| epid | int | epid | 
| credential | Credential | 凭据 |

#### _async_ def get_bangumi()

获取对应的番剧

**Returns:** 番剧类

#### _async_ def set_epid()

设置 epid

**Returns:** None

#### _async_ def get_epid()

获取 epid

**Returns:** epid

#### _async_ def get_episode_info()

获取番剧单集信息

**Returns:** API 调用返回结果。

#### _async_ def get_download_url()

获取番剧下载链接

**Returns:** API 调用返回结果。


#### _async_ def get_danmaku_view()

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。


**Returns:** API 调用返回结果。


#### _async_ def get_danmakus()

获取弹幕

**Returns:** API 调用返回结果。


#### _async_ def get_danmaku_xml()

获取所有弹幕的 xml 源文件（非装填的弹幕）

**Returns:** API 调用返回结果。

#### def get_bangumi_from_episode()

通过一个 epid 获取番剧信息

**Returns**:输入的集对应的番剧类
