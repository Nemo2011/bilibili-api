# Module creative_center.py

```python
from bilibili_api import creative_center
```

创作中心相关。

## class GraphPeriod

**Extends:** enum.Enum

统计图表时间段枚举。

+ YESTERDAY: 昨天
+ WEEK: 近一周
+ MONTH: 近一月
+ THREE_MONTH: 近三月
+ TOTAL: 历史累计

---

## class GraphType

**Extends:** enum.Enum

统计图表的类型。

+ PLAY: 播放量
+ VISITOR: 访问量
+ FAN: 粉丝数
+ LIKE: 点赞数
+ FAV: 收藏数
+ SHARE: 分享数
+ COMMENT: 评论数
+ DAMKU: 弹幕数
+ COIN: 投币数
+ ELEC: 充电数

---

## class FanGraphPeriod

**Extends:** enum.Enum

粉丝统计图表的时间段。

+ YESTERDAY: 昨天
+ WEEK: 近一周
+ MONTH: 近一月
+ THREE_MONTH: 近三月

---

## class FanGraphType

**Extends:** enum.Enum

粉丝统计图表的类型。

+ ALL_FANS: 粉丝总量
+ FAN: 新增粉丝
+ FOLLOW: 新增关注
+ UNFOLLOW: 取消关注

---

## class Copyright

**Extends:** enum.Enum

稿件播放完成率对比的版权类型。

+ ALL: 全部
+ ORIGINAL: 原创
+ REPRINT: 转载

---

## class ArticleInfoType

**Extends:** enum.Enum

文章统计信息的类型。

+ READ: 阅读
+ COMMENT: 评论
+ SHARE: 分享
+ COIN: 投币
+ FAV: 收藏
+ LIKE: 点赞

---

## class UploadManagerOrder

**Extends:** enum.Enum

内容管理排序字段。

+ CLICK: 点击
+ STOW: 收藏
+ SENDDATE: 上传日期
+ DM_COUNT: 弹幕数量
+ COMMENT_COUNT: 评论数量

---

## class UploadManagerStatus

**Extends:** enum.Enum

内容管理稿件状态字段。

+ ALL: 全部稿件
+ PUBED: 已通过
+ IS_PUBING: 进行中
+ NOT_PUBED: 未通过

## class UploadManagerSort

**Extends:** enum.Enum

内容管理文章排序字段。

| 名称          | 值  | 描述            |
| ------------- | -- | --------------- |
| CREATED_TIME  | 1  | 创建日期         |
| LIKE          | 2  | 点赞             |
| COMMENT       | 3  | 评论             |
| FAV           | 5  | 收藏             |
| COIN          | 6  | 投币             |

## class UploadManagerArticleStatus

**Extends:** enum.Enum

内容管理文章状态字段。

| 名称         | 值  | 描述            |
| ------------ | -- | --------------- |
| ALL          | 0  | 全部稿件         |
| PUBED        | 2  | 已通过           |
| IS_PUBING    | 1  | 进行中           |
| NOT_PUBED    | 3  | 未通过           |

## class ArchiveType

**Extends:** enum.Enum

评论管理中的稿件类型。

| 名称     | 值  | 描述    |
| -------- | -- | ------- |
| VIDEO    | 1  | 视频    |
| ARTICLE  | 12 | 文章    |
| AUDIO    | 14 | 音频    |

## class CommentManagerOrder

**Extends:** enum.Enum

评论管理中的排序字段。

| 名称      | 值  | 描述    |
| --------- | -- | ------- |
| RECENTLY  | 1  | 最近    |
| LIKE      | 2  | 点赞    |
| REPLY     | 3  | 回复    |


## class DanmakuOrder

**Extends:** enum.Enum

弹幕排序依据。

| 名称       | 值      | 描述      |
| ---------- | ------- | --------- |
| CTIME      | ctime   | 发送时间  |
| LIKE_COUNT | like_count | 点赞数    |

## class DanmakuSort

**Extends:** enum.Enum

弹幕排序顺序。

| 名称  | 值   | 描述   |
| ----- | ---- | ------ |
| DESC  | desc | 降序   |
| ASC   | asc  | 升序   |

## class DanmakuType

**Extends:** enum.Enum

弹幕筛选类型。

| 名称     | 值  | 描述      |
| -------- | -- | --------- |
| ALL      | 0  | 全部      |
| PROTECT  | 2  | 保护弹幕  |


---

## async def get_compare()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

获取对比数据。

**Returns:** 调用接口返回的内容。

## async def get_graph()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| period | GraphPeriod | 统计图表的时间段 |
| graph_type | GraphType | 统计图表的类型 |

获取统计图表。

**Returns:** 调用接口返回的内容。

## async def get_overview()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| period | GraphPeriod | 统计图表的时间段 |

获取概览数据。

**Returns:** 调用接口返回的内容。

## async def get_video_survey()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

获取视频各分区中占比排行。

**Returns:** 调用接口返回的内容。

## async def get_video_playanalysis()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| copyright | Copyright | 稿件播放完成率对比的版权类型 |

获取视频播放完成率对比。

**Returns:** 调用接口返回的内容。

## async def get_video_source()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

获取视频播放来源分布。

**Returns:** 调用接口返回的内容。

## async def get_fan_overview()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| period | FanGraphPeriod | 粉丝统计图表的时间段 |

获取粉丝概览数据。

**Returns:** 调用接口返回的内容。

## async def get_fan_graph()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| period | FanGraphPeriod | 粉丝统计图表的时间段 |
| graph_type | FanGraphType | 粉丝统计图表的类型 |

获取粉丝统计图表。

**Returns:** 调用接口返回的内容。

## async def get_article_overview()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

获取文章概览数据。

**Returns:** 调用接口返回的内容。

## async def get_article_graph()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| graph_type | ArticleInfoType | 文章统计信息的类型 |

获取文章统计图表。

**Returns:** 调用接口返回的内容。

## async def get_article_survey()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| rank_type | ArticleInfoType | 文章统计信息的类型 |

获取文章排行数据。

**Returns:** 调用接口返回的内容。

## async def get_article_source()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

获取文章来源分布。

**Returns:** 调用接口返回的内容。

## async def get_video_draft_upload_manager_info

| name       | type      | description                   |
| ---------- | --------- | ----------------------------- |
| credential | Credential| 凭据                          |

获取内容管理视频草稿信息。

**Returns:** 内容管理视频草稿信息。

---

## async def get_video_upload_manager_info

| name          | type                            | description                   |
| ------------- | ------------------------------- | ----------------------------- |
| credential    | Credential                      | 凭据                          |
| is_interative | bool (可选)                    | 是否为互动视频                 |
| pn            | int (可选)                      | 页码                          |
| ps            | int (可选)                      | 每页项数                       |
| order         | UploadManagerOrder (可选)      | 稿件排序                       |
| tid           | VideoZoneTypes, None, int (可选) | 分区                 |
| status        | UploadManagerStatus (可选)     | 稿件状态                       |

获取内容管理视频信息。

**Returns:** 内容管理视频信息。

## async def get_article_upload_manager_info

| name          | type                                | description        |
| ------------- | ----------------------------------- | ------------------ |
| credential    | Credential                          | 凭据               |
| status        | UploadManagerArticleStatus (可选)  | 稿件状态           |
| sort          | UploadManagerSort (可选)           | 稿件排序           |
| pn            | int (可选)                          | 页码               |

获取内容管理文章信息。

**Returns:** 内容管理文章信息。

## async def get_article_list_upload_manager_info

| name       | type       | description |
| ---------- | ---------- | ----------- |
| credential | Credential | 凭据        |

获取内容管理文集信息。

**Returns:** 内容管理文集信息。

## async def get_comments

| name                | type                                | description                |
| ------------------- | ----------------------------------- | -------------------------- |
| credential          | Credential                          | 凭据                       |
| oid (Optional)      | int (Optional)                      | 指定稿件                   |
| keyword (Optional)  | str (Optional)                      | 关键词                     |
| archive_type        | ArchiveType                         | 稿件类型                   |
| order               | CommentManagerOrder                 | 排序字段                   |
| filter              | int                                 | 筛选器，作用未知           |
| pn                  | int                                 | 页码                       |
| ps                  | int                                 | 每页项数                   |
| charge_plus_filter  | bool                                | charge_plus_filter         |

获取评论。

**Returns: dict** 评论管理评论信息。


## async def del_comments

| name                | type             | description                |
| ------------------- | ---------------- | -------------------------- |
| credential          | Credential       | 凭据                       |
| oid                 | Union[int, List] | 指定稿件                   |
| rpid                | Union[int, List] | 指定评论                   |
| archive_type        | ArchiveType      | 稿件类型                   |

删除评论。

每个评论对应一个 oid。


## async def get_recently_danmakus

| 参数名       | 类型             | 描述                     |
| ------------ | ---------------- | ------------------------ |
| credential   | Credential        | 凭据                     |
| pn (可选)    | int              | 页码                     |
| ps (可选)    | int              | 每页项数                 |

获取最近弹幕。

**Returns:** dict 弹幕管理最近弹幕信息。


## async def del_danmaku

| 参数 | 类型 | 描述 |
| ---- | ---- | ---- |
| credential | Credential | 凭据 |
| oid | int | 稿件 oid |
| dmids | Union[int, List[int]] | 弹幕 id，可以传入列表或单个整数 |

删除弹幕。

**返回: dict** API 返回信息。

---

## async def edit_danmaku_state

| 参数 | 类型 | 描述 |
| ---- | ---- | ---- |
| credential | Credential | 凭据 |
| oid | int | 稿件 oid |
| dmids | Union[int, List[int]] | 弹幕 id，可以传入列表或单个整数 |
| state | Optional[int] | 弹幕状态 (1 删除, 2 保护, 3 取消保护) |

操作弹幕状态。

**返回: dict** API 返回信息。

---

## async def edit_danmaku_pool

| 参数 | 类型 | 描述 |
| ---- | ---- | ---- |
| credential | Credential | 凭据 |
| oid | int | 稿件 oid |
| dmids | Union[int, List[int]] | 弹幕 id，可以传入列表或单个整数 |
| is_subtitle | bool | 是否为字幕 |

操作弹幕池。

**返回: dict** API 返回信息。

## async def get_danmakus

| 参数 | 类型 | 描述 |
| ---- | ---- | ---- |
| credential | Credential | 凭据 |
| oid | int | 稿件 oid，用逗号分隔 |
| select_type | DanmakuType | 弹幕类型 |
| archive_type | ArchiveType | 稿件类型 |
| mids (Optional) | Union[int, List[int]] | 用户 mids，用逗号分隔或直接传入整数 |
| keyword (Optional) | str | 关键词 |
| progress_from (Optional) | int | 进度开始 |
| progress_to (Optional) | int | 进度结束 |
| ctime_from (Optional) | datetime.datetime | 创建时间起始 |
| ctime_to (Optional) | datetime.datetime | 创建时间结束 |
| modes (Optional) | Union[DanmakuMode, List[DanmakuMode]] | 弹幕模式 |
| pools (Optional) | Union[DanmakuPool, List[DanmakuPool]] | 弹幕池 |
| attrs | Unknown | 弹幕属性，未知参数 |
| order | DanmakuOrder | 排序字段 |
| sort | DanmakuSort | 排序方式 |
| pn | int | 页码 |
| ps | int | 每页项数 |
| cp_filter | bool | 是否过滤 CP 弹幕，默认为 False |

弹幕搜索。

**返回: dict** 弹幕搜索结果。
