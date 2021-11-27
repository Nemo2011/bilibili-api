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

## async def get_meta()

| name       | type                 | description             |
| ---------- | -------------------- | ----------------------- |
| media_id   | int                  | media_id                |
| credential | Credential, optional | 凭据. Defaults to None. |

获取番剧元数据信息（评分，封面URL，标题等）

**Returns:** API 调用返回结果。

## async def get_short_comment_list()

| name       | type                          | description                                                  |
| ---------- | ----------------------------- | ------------------------------------------------------------ |
| media_id   | int                           | media_id                                                     |
| order      | BangumiCommentOrder, optional | 排序方式。Defaults to BangumiCommentOrder.DEFAULT            |
| next       | str, optional                 | 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None |
| credential | Credential, optional          | 凭据. Defaults to None                                       |

获取短评列表

**Returns:** API 调用返回结果。

## async def get_long_comment_list()

| name       | type                          | description                                                  |
| ---------- | ----------------------------- | ------------------------------------------------------------ |
| media_id   | int                           | media_id                                                     |
| order      | BangumiCommentOrder, optional | 排序方式。Defaults to BangumiCommentOrder.DEFAULT            |
| next       | str, optional                 | 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None |
| credential | Credential, optional          | 凭据. Defaults to None                                       |

获取长评列表

**Returns:** API 调用返回结果。

## async def get_episode_list()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| season_id  | int                  | season_id              |
| credential | Credential, optional | 凭据. Defaults to None |

获取季度分集列表

**Returns:** API 调用返回结果。

## async def get_stat()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| season_id  | int                  | season_id              |
| credential | Credential, optional | 凭据. Defaults to None |

获取番剧播放量，追番等信息

**Returns:** API 调用返回结果。

## async def get_episode_info()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| epid       | int                  | episode_id             |
| credential | Credential, optional | 凭据. Defaults to None |

获取番剧单集信息

**Returns:** API 调用返回结果。

## async def get_overview()

| name       | type                 | description            |
| ---------- | -------------------- | ---------------------- |
| season_id  | int                  | season_id              |
| credential | Credential, optional | 凭据. Defaults to None |

获取番剧全面概括信息，包括发布时间、剧集情况、stat 等情况

**Returns:** API 调用返回结果。

## async def set_follow()

| name       | type                 | description                |
| ---------- | -------------------- | -------------------------- |
| season_id  | int                  | season_id                  |
| status     | bool, optional       | 追番状态，Defaults to True |
| credential | Credential, optional | 凭据. Defaults to None     |

追番状态设置

**Returns:** API 调用返回结果。

