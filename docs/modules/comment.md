# Module comment.py


bilibili_api.comment

评论相关。

关于资源 ID（oid）的一些示例（{}部分为应该传入的参数）。

+ 视频：AV 号：av{170001} `get_aid() / await get_aid() # for Episode`。
+ 专栏：cv{9762979} `get_cvid()`。
+ 动态/图文：{116859542} `await get_rid()`。
+ 课程：ep{5556} `get_epid()`
+ 音频：au{13998} `get_auid()`
+ 歌单：am{26241} `get_amid()`
+ 小黑屋: ban/{2600321} `get_id()`
+ 漫画：mc{32749} `get_manga_id()`
+ 活动: {16279} `await get_activity_aid()`


``` python
from bilibili_api import comment
```

- [class Comment()](#class-Comment)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def delete()](#async-def-delete)
  - [def get\_oid()](#def-get\_oid)
  - [def get\_rpid()](#def-get\_rpid)
  - [async def get\_sub\_comments()](#async-def-get\_sub\_comments)
  - [def get\_type()](#def-get\_type)
  - [async def hate()](#async-def-hate)
  - [async def like()](#async-def-like)
  - [async def pin()](#async-def-pin)
  - [async def report()](#async-def-report)
- [class CommentResourceType()](#class-CommentResourceType)
- [class OrderType()](#class-OrderType)
- [class ReportReason()](#class-ReportReason)
- [async def get\_comments()](#async-def-get\_comments)
- [async def get\_comments\_lazy()](#async-def-get\_comments\_lazy)
- [async def send\_comment()](#async-def-send\_comment)

---

## class Comment()

对单条评论的相关操作。


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `oid` | `int` | 评论所在资源 ID。 |
| `type_` | `ResourceType` | 评论所在资源类型枚举。 |
| `rpid` | `int` | 评论 ID。 |
| `credential` | `Credential` | 凭据类. Defaults to None. |


### async def delete()

删除评论。



**Returns:** `dict`:  调用 API 返回的结果




### def get_oid()

获取评论对应 oid



**Returns:** `int`:  oid




### def get_rpid()

获取评论 rpid



**Returns:** `int`:  rpid




### async def get_sub_comments()

获取子评论。即评论下的评论。


| name | type | description |
| - | - | - |
| `page_index` | `int, optional` | 页码索引，从 1 开始。Defaults to 1. |
| `page_size` | `int, optional` | 每页评论数。设置大于20的数值不会起作用。Defaults to 10. |

**Returns:** `dict`:  调用 API 返回的结果




### def get_type()

获取评论资源类型



**Returns:** `CommentResourceType`:  资源类型




### async def hate()

点踩评论。


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 状态, Defaults to True. |

**Returns:** `dict`:  调用 API 返回的结果




### async def like()

点赞评论。


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 状态, Defaults to True. |

**Returns:** `dict`:  调用 API 返回的结果




### async def pin()

置顶评论。


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 状态, Defaults to True. |

**Returns:** `dict`:  调用 API 返回的结果




### async def report()

举报评论


| name | type | description |
| - | - | - |
| `report_reason` | `ReportReason` | 举报类型枚举 |
| `content` | `str, optional` | 其他举报备注内容仅 reason=ReportReason.OTHER 可用且不能为 None. |

**Returns:** `dict`:  调用 API 返回的结果


Error Code:
0: 成功
-101: 账号未登录
-102: 账号被封停
-111: csrf校验失败
-400: 请求错误
-403: 权限不足
-404: 无此项
-500: 服务器错误
-509: 请求过于频繁
12002: 评论区已关闭
12006: 没有该评论
12008: 已经举报过了
12009: 评论主体的type不合法
12019: 举报过于频繁
12077: 举报理由过长或过短



---

## class CommentResourceType()

**Extend: enum.Enum**

资源类型枚举。

+ VIDEO: 视频。
+ ARTICLE: 专栏。
+ DYNAMIC_DRAW: 画册（图文）。
+ DYNAMIC: 动态（画册也属于动态的一种，只不过画册还有一个专门的 ID）。
+ AUDIO：音频。
+ AUDIO_LIST：歌单。
+ CHEESE: 课程
+ BLACK_ROOM: 小黑屋
+ MANGA: 漫画
+ ACTIVITY: 活动




---

## class OrderType()

**Extend: enum.Enum**

评论排序方式枚举。

+ LIKE：按点赞数倒序。
+ TIME：按发布时间倒序。




---

## class ReportReason()

**Extend: enum.Enum**

举报类型枚举

+ OTHER: 其他
+ SPAM_AD: 垃圾广告
+ PORNOGRAPHY: 色情
+ FLOOD: 刷屏
+ PROVOCATION: 引战
+ SPOILER: 剧透
+ POLITICS: 政治
+ PERSONAL_ATTACK: 人身攻击
+ IRRELEVANT_CONTENT: 内容不相关
+ ILLEGAL: 违法违规
+ VULGAR: 低俗
+ ILLEGAL_WEBSITE: 非法网站
+ GAMBLING_FRAUD: 赌博诈骗
+ SPREADING_FALSE_INFORMATION: 传播不实信息
+ INCITING_INFORMATION: 怂恿教唆信息
+ PRIVACY_VIOLATION: 侵犯隐私
+ FLOOR_TAKING: 抢楼
+ INAPPROPRIATE_CONTENT_FOR_MINORS: 青少年不良信息




---

## async def get_comments()

获取资源评论列表。

第二页以及往后需要提供 `credential` 参数。


| name | type | description |
| - | - | - |
| `oid` | `int` | 资源 ID。 |
| `type_` | `CommentsResourceType` | 资源类枚举。 |
| `page_index` | `int, optional` | 页码. Defaults to 1. |
| `order` | `OrderType, optional` | 排序方式枚举. Defaults to OrderType.TIME. |
| `credential` | `Credential, optional` | 凭据。Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_comments_lazy()

新版获取资源评论列表。

第二次以及往后需要提供 `credential` 参数。


| name | type | description |
| - | - | - |
| `oid` | `int` | 资源 ID。 |
| `type_` | `CommentsResourceType` | 资源类枚举。 |
| `offset` | `str, optional` | 偏移量。每次请求可获取下次请求对应的偏移量，类似单向链表。对应返回结果的 `["cursor"]["pagination_reply"]["next_offset"]` |
| `order` | `OrderType, optional` | 排序方式枚举. Defaults to OrderType.TIME. |
| `credential` | `Credential, optional` | 凭据。Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def send_comment()

通用发送评论 API。

说明 `root` 和 `parent`，假设评论的是视频，常见的评论有三种情况：

1. 只在视频下面发送评论：root=None, parent=None；
2. 回复视频下面的评论：root=评论 ID, parent=None；
3. 回复视频下面的评论中的评论：root=在哪条评论下评论的 ID, parent=回复哪条评论的 ID。

当 root 为空时，parent 必须为空。


| name | type | description |
| - | - | - |
| `text` | `str` | 评论内容。 |
| `oid` | `str` | 资源 ID。 |
| `type_` | `CommentsResourceType` | 资源类型枚举。 |
| `root` | `int, optional` | 根评论 ID, Defaults to None. |
| `parent` | `int, optional` | 父评论 ID, Defaults to None. |
| `credential` | `Credential` | 凭据 |

**Returns:** `dict`:  调用 API 返回的结果




