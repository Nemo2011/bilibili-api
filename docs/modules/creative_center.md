# Module creative_center.py


bilibili_api.creative_center

创作中心相关。

务必携带 Credential 信息，否则无法获取到数据。


``` python
from bilibili_api import creative_center
```

- [class ArchiveType()](#class-ArchiveType)
- [class ArticleInfoType()](#class-ArticleInfoType)
- [class CommentManagerOrder()](#class-CommentManagerOrder)
- [class Copyright()](#class-Copyright)
- [class DanmakuMode()](#class-DanmakuMode)
- [class DanmakuOrder()](#class-DanmakuOrder)
- [class DanmakuPool()](#class-DanmakuPool)
- [class DanmakuSort()](#class-DanmakuSort)
- [class DanmakuType()](#class-DanmakuType)
- [class FanGraphPeriod()](#class-FanGraphPeriod)
- [class FanGraphType()](#class-FanGraphType)
- [class GraphPeriod()](#class-GraphPeriod)
- [class GraphType()](#class-GraphType)
- [class UploadManagerArticleStatus()](#class-UploadManagerArticleStatus)
- [class UploadManagerOrder()](#class-UploadManagerOrder)
- [class UploadManagerSort()](#class-UploadManagerSort)
- [class UploadManagerStatus()](#class-UploadManagerStatus)
- [async def del\_comments()](#async-def-del\_comments)
- [async def del\_danmaku()](#async-def-del\_danmaku)
- [async def edit\_danmaku\_pool()](#async-def-edit\_danmaku\_pool)
- [async def edit\_danmaku\_state()](#async-def-edit\_danmaku\_state)
- [async def get\_article\_graph()](#async-def-get\_article\_graph)
- [async def get\_article\_list\_upload\_manager\_info()](#async-def-get\_article\_list\_upload\_manager\_info)
- [async def get\_article\_overview()](#async-def-get\_article\_overview)
- [async def get\_article\_rank()](#async-def-get\_article\_rank)
- [async def get\_article\_source()](#async-def-get\_article\_source)
- [async def get\_article\_upload\_manager\_info()](#async-def-get\_article\_upload\_manager\_info)
- [async def get\_comments()](#async-def-get\_comments)
- [async def get\_compare()](#async-def-get\_compare)
- [async def get\_danmakus()](#async-def-get\_danmakus)
- [async def get\_fan\_graph()](#async-def-get\_fan\_graph)
- [async def get\_fan\_overview()](#async-def-get\_fan\_overview)
- [async def get\_graph()](#async-def-get\_graph)
- [async def get\_overview()](#async-def-get\_overview)
- [async def get\_recently\_danmakus()](#async-def-get\_recently\_danmakus)
- [async def get\_video\_draft\_upload\_manager\_info()](#async-def-get\_video\_draft\_upload\_manager\_info)
- [async def get\_video\_playanalysis()](#async-def-get\_video\_playanalysis)
- [async def get\_video\_source()](#async-def-get\_video\_source)
- [async def get\_video\_survey()](#async-def-get\_video\_survey)
- [async def get\_video\_upload\_manager\_info()](#async-def-get\_video\_upload\_manager\_info)

---

## class ArchiveType()

**Extend: enum.Enum**

评论管理中的稿件类型。

+ VIDEO: 视频
+ ARTICLE: 文章
+ AUDIO: 音频




---

## class ArticleInfoType()

**Extend: enum.Enum**

文章统计信息的类型。

+ READ: 阅读
+ COMMENT: 评论
+ SHARE: 分享
+ COIN: 投币
+ FAV: 收藏
+ LIKE: 点赞




---

## class CommentManagerOrder()

**Extend: enum.Enum**

评论管理中的排序字段。

+ RECENTLY: 最近
+ LIKE: 点赞
+ REPLY: 回复




---

## class Copyright()

**Extend: enum.Enum**

稿件播放完成率对比的版权类型。

+ ALL: 全部
+ ORIGINAL: 原创
+ REPRINT: 转载




---

## class DanmakuMode()

**Extend: enum.Enum**

弹幕模式。

+ ROLL: 滚动
+ BOTTOM: 底端
+ TOP: 顶端
+ REVERSE: 逆向
+ ADVANCED: 高级
+ CODE: 代码
+ BAS: BAS 补充注释




---

## class DanmakuOrder()

**Extend: enum.Enum**

弹幕排序依据

+ CTIME: 发送时间
+ LIKE_COUNT: 点赞数




---

## class DanmakuPool()

**Extend: enum.Enum**

子弹幕池类型。

+ NORMAL: 普通
+ SUBTITLE: 字幕
+ SPECIAL: 特殊




---

## class DanmakuSort()

**Extend: enum.Enum**

弹幕排序顺序

+ DESC: 降序
+ ASC: 升序




---

## class DanmakuType()

**Extend: enum.Enum**

弹幕筛选类型

+ ALL: 全部
+ PROTECT: 保护弹幕




---

## class FanGraphPeriod()

**Extend: enum.Enum**

粉丝统计图表的时间段。

+ YESTERDAY: 昨天
+ WEEK: 近一周
+ MONTH: 近一月
+ THREE_MONTH: 近三月




---

## class FanGraphType()

**Extend: enum.Enum**

粉丝统计图表的类型。

+ ALL_FANS: 粉丝总量
+ FAN: 新增粉丝
+ FOLLOW: 新增关注
+ UNFOLLOW: 取消关注




---

## class GraphPeriod()

**Extend: enum.Enum**

统计图表的时间段。

+ YESTERDAY: 昨天
+ WEEK: 近一周
+ MONTH: 近一月
+ THREE_MONTH: 近三月
+ TOTAL: 历史累计




---

## class GraphType()

**Extend: enum.Enum**

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

## class UploadManagerArticleStatus()

**Extend: enum.Enum**

内容管理文章状态字段。

+ ALL: 全部稿件
+ PUBED: 已通过
+ IS_PUBING: 进行中
+ NOT_PUBED: 未通过




---

## class UploadManagerOrder()

**Extend: enum.Enum**

内容管理排序字段。

+ CLICK: 点击
+ STOW: 收藏
+ SENDDATE: 上传日期
+ DM_COUNT: 弹幕数量
+ COMMENT_COUNT: 评论数量




---

## class UploadManagerSort()

**Extend: enum.Enum**

内容管理文章排序字段。

+ CREATED_TIME: 创建日期
+ LIKE: 点赞
+ COMMENT: 评论
+ FAV: 收藏
+ COIN: 投币




---

## class UploadManagerStatus()

**Extend: enum.Enum**

内容管理稿件状态字段。

+ ALL: 全部稿件
+ PUBED: 已通过
+ IS_PUBING: 进行中
+ NOT_PUBED: 未通过




---

## async def del_comments()

删除评论

每个评论对应一个 oid


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `oid` | `int, lsit` | 指定稿件 |
| `rpid` | `int, lsit` | 指定评论 |
| `archive_type` | `ArchiveType` | 稿件类型 |




---

## async def del_danmaku()

删除弹幕


| name | type | description |
| - | - | - |
| `oid` | `int` | 稿件 oid |
| `dmids` | `List[int], int` | 弹幕 id，可以传入列表和 int |




---

## async def edit_danmaku_pool()

操作弹幕池


| name | type | description |
| - | - | - |
| `oid` | `int` | 稿件 oid |
| `dmids` | `List[int], int` | 弹幕 id，可以传入列表和 int |
| `is_subtitle` | `bool` | 是否为字幕 |

**Returns:** `dict`:  API 返回信息




---

## async def edit_danmaku_state()

操作弹幕状态


| name | type | description |
| - | - | - |
| `oid` | `int` | 稿件 oid |
| `dmids` | `List[int], int` | 弹幕 id，可以传入列表和 int |
| `state` | `int, Optional` | 弹幕状态 1 删除 2 保护 3 取消保护 |

**Returns:** `dict`:  API 返回信息




---

## async def get_article_graph()

获取文章图表数据。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `graph_type` | `ArticleInfoType` | 图表类型。 |

**Returns:** `dict`:  文章图表数据。




---

## async def get_article_list_upload_manager_info()

获取内容管理文章信息


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |

**Returns:** `dict`:  内容管理文集信息。




---

## async def get_article_overview()

获取文章概览数据。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |

**Returns:** `dict`:  文章概览数据。




---

## async def get_article_rank()

获取文章排行数据。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `rank_type` | `ArticleInfoType` | 排行依据。 |

**Returns:** `dict`:  文章排行数据。




---

## async def get_article_source()

获取文章阅读终端数据


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |

**Returns:** `dict`:  文章阅读终端数据。




---

## async def get_article_upload_manager_info()

获取内容管理文章信息


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `pn` | `int` | 页码 |
| `status` | `UploadManagerArticleStatus` | 稿件状态 |
| `sort` | `UploadManagerSort` | 稿件排序 |

**Returns:** `dict`:  内容管理文章信息。




---

## async def get_comments()

获取评论


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `oid` | `Optional, int` | 指定稿件 |
| `keyword` | `Optional, str` | 关键词 |
| `archive_type` | `ArchiveType` | 稿件类型 |
| `order` | `CommentManagerOrder` | 排序字段 |
| `filter` | `int` | 筛选器，作用未知 |
| `pn` | `int` | 页码 |
| `ps` | `int` | 每页项数 |
| `charge_plus_filter` | `bool` | charge_plus_filter |

**Returns:** `dict`:  评论管理评论信息。




---

## async def get_compare()

获取对比数据。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |

**Returns:** `dict`:  视频对比数据。




---

## async def get_danmakus()

弹幕搜索


| name | type | description |
| - | - | - |
| `credential` | `Credential` | Credential 凭据 |
| `oid` | `int` | 稿件oid，用逗号分隔 |
| `select_type` | `DanmakuType` | 弹幕类型 |
| `archive_type` | `ArchiveType` | 稿件类型 |
| `mids` | `List[int], int` | 用户mids，用逗号分隔或者直接 int |
| `keyword` | `str` | 关键词 |
| `progress_from` | `int` | 进度开始 |
| `progress_to` | `int` | 进度结束 |
| `ctime_from` | `datetime.datetime` | 创建时间起始 |
| `ctime_to` | `datetime.datetime` | 创建时间结束 |
| `modes` | `DanmakuMode` | 弹幕模式。 |
| `pool` | `DanmakuPool` | 弹幕池 |
| `attrs` | `Unknown` | 弹幕属性，未知参数 |
| `order` | `DanmakuOrder` | 排序字段 |
| `sort` | `DanmakuSort` | 排序方式 |
| `pn` | `int` | 页码。 |
| `ps` | `int` | 每页项数。 |
| `cp_filter` | `bool` | 是否过滤CP弹幕。未知参数，默认为 False |

**Returns:** `dict`:  弹幕搜索结果




---

## async def get_fan_graph()

获取粉丝图表数据。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `period` | `FanGraphPeriod` | 时间段。 |
| `graph_type` | `FanGraphType` | 图表类型。 |

**Returns:** `dict`:  粉丝图表数据。




---

## async def get_fan_overview()

获取粉丝概览数据。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `period` | `FanGraphPeriod` | 时间段。 |

**Returns:** `dict`:  粉丝概览数据。




---

## async def get_graph()

获取统计图表数据。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `period` | `GraphPeriod` | 时间段。 |
| `graph_type` | `GraphType` | 图表类型。 |

**Returns:** `dict`:  视频统计图表数据。




---

## async def get_overview()

获取概览数据。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `period` | `GraphPeriod` | 时间段。 |

**Returns:** `dict`:  视频概览数据。




---

## async def get_recently_danmakus()

最近弹幕


| name | type | description |
| - | - | - |
| `credential` | `Credential` | Credential 凭据。 |
| `pn` | `int` | 页码。 |
| `ps` | `int` | 每页项数。 |

**Returns:** `dict`:  弹幕管理最近弹幕信息。




---

## async def get_video_draft_upload_manager_info()

获取内容管理视频草稿信息


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |

**Returns:** `dict`:  内容管理视频草稿信息。




---

## async def get_video_playanalysis()

获取稿件播放完成率对比。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `copyright` | `Copyright` | 版权类型。 |

**Returns:** `dict`:  稿件播放完成率对比数据。




---

## async def get_video_source()

获取稿件播放来源分布。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |

**Returns:** `dict`:  视频来源分布数据。




---

## async def get_video_survey()

获取视频各分区中占比排行。


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |

**Returns:** `dict`:  视频分区排行数据。




---

## async def get_video_upload_manager_info()

获取内容管理视频信息


| name | type | description |
| - | - | - |
| `credentials` | `Credential` | Credential 凭据。 |
| `is_interative` | `bool` | 是否为互动视频 |
| `pn` | `int` | 页码 |
| `ps` | `int` | 每页项数 |
| `tid` | `VideoZoneTypes, None, int` | 分区 |
| `status` | `UploadManagerStatus` | 稿件状态 |
| `order` | `UploadManagerOrder` | 稿件排序 |

**Returns:** `dict`:  内容管理视频信息。




