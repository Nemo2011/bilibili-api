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

### Atrributes

| name       | type       | description                    |
|------------|------------|--------------------------------|
| credential | Credential | 凭据类                            |
| __raw      | dict       | 初始化时从Api拉取的原始数据                |
| __epid     | int        | 剧集ID,如果不传入就为 `-1`              |
| __ssid     | int        | 成功即存在的季度ID                     |
| __media_id | int        | 成功即存在的番剧ID                     |
| __up_info  | dict       | 上传者信息/所属                       |
| ep_list    | list       | 获取到的分集列表                       |
| ep_item    | list       | 如果存在有效`epid`则获取对应数据，不存在为`[{}]` |

### Functions

#### def \_\_init\_\_()

| name       | type       | description        |
|------------|------------|--------------------|
| media_id   | int        | 教程 ID（不与番剧相通）      |
| ssid       | int        | 教程季度 ID（不与番剧相通）    |
| epid       | int        | 剧集 ID              |
| oversea    | bool       | 是否采用港澳台 Api(与大陆通用) |
| credential | Credential | 凭据                 |

media_id ，ssid ,epid 三者必须有其一，如果含有所有参数，字段会被提交到Api查询

#### def get_media_id()

获取 media_id

**Returns:** media_id

#### def get_season_id()

获取 season_id

**Returns:** season_id

#### def get_up_info()

获取番剧的上传者信息，一般为哔哩哔哩出差和哔哩哔哩两种

**Returns:** Api 相关字段

#### def get_episode_info()

获取传入的 epid 剧集相对应的各种数据，比如 标题，avid,bvid 等等,如果没有传入 epid 参数将会抛出错误

**Returns:** Api 相关字段

#### def get_raw()

获取初始化得到的，和 get_overview 一个格式的数据

**Returns:** Api 字段

#### async def set_ssid()

设置 season_id

**Returns:** None

#### async def set_media_id()

设置 media_id

**Returns:** None

#### async def get_meta()

获取番剧元数据信息（评分，封面URL，标题等）

**Returns:** API 调用返回结果。

#### async def get_short_comment_list()

| name  | type                          | description                                  |
|-------|-------------------------------|----------------------------------------------|
| order | BangumiCommentOrder, optional | 排序方式。Defaults to BangumiCommentOrder.DEFAULT |
| next  | str, optional                 | 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None  |

获取短评列表

**Returns:** API 调用返回结果。

#### async def get_long_comment_list()

| name  | type                          | description                                  |
|-------|-------------------------------|----------------------------------------------|
| order | BangumiCommentOrder, optional | 排序方式。Defaults to BangumiCommentOrder.DEFAULT |
| next  | str, optional                 | 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None  |

获取长评列表

**Returns:** API 调用返回结果。

#### async def get_episode_list()

获取季度分集列表

**Returns:** API 调用返回结果。

#### async def get_stat()

获取番剧播放量，追番等信息

**Returns:** API 调用返回结果。

#### async def get_overview()

获取番剧全面概括信息，包括发布时间、剧集情况、stat 等情况

**Returns:** API 调用返回结果。

***

## async def set_follow()

| name       | type                 | description           |
|------------|----------------------|-----------------------|
| bangumi    | Bangumi              | 番剧类                   |
| status     | bool, optional       | 追番状态，Defaults to True |
| credential | Credential, optional | 凭据. Defaults to None  |

追番状态设置

**Returns:** API 调用返回结果。

## class Episode

**Extends: bilibili_api.video.Video**

番剧剧集类

### Atrributes

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |
| video_class | Video | 对应视频 |
| bangumi | Bangumi | 对应番剧 |

### Functions

**这里仅列出新增的或重写过的函数，Video 类的其他函数都可使用**

#### def \_\_init\_\_()

| name       | type       | description |
|------------|------------|-------------|
| epid       | int        | epid        | 
| credential | Credential | 凭据          |

#### def get_bangumi()

获取对应的番剧

**Returns:** 番剧类

#### def set_epid()

设置 epid

**Returns:** None

#### def get_epid()

获取 epid

**Returns:** epid

#### async def get_episode_info()

获取番剧单集信息

**Returns:** API 调用返回结果。

#### async def get_download_url()

获取番剧下载链接

**Returns:** API 调用返回结果。

#### async def get_danmaku_view()

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。

**Returns:** API 调用返回结果。

#### async def get_danmakus()

| name | type                    | description                           |
|------|-------------------------|---------------------------------------|
| date | datetime.Date, optional | 指定日期后为获取历史弹幕，精确到年月日。Defaults to None. |

获取弹幕

**Returns:** API 调用返回结果。

#### async def get_danmaku_xml()

获取所有弹幕的 xml 源文件（非装填的弹幕）

**Returns:** API 调用返回结果。

#### async def get_history_danmaku_index()

| name | type                    | description                           |
|------|-------------------------|---------------------------------------|
| date | datetime.Date, optional | 指定日期后为获取历史弹幕，精确到年月日。Defaults to None. |

获取特定月份存在历史弹幕的日期。

**Returns**: None | List[str]: 调用 API 返回的结果。不存在时为 None。

#### async def get_bangumi_from_episode()

获取剧集对应的番剧

**Returns**:输入的集对应的番剧类
