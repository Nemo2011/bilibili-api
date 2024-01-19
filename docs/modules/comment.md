# Module comment.py

```python
from bilibili_api import comment
```

评论相关。

关于资源 ID（oid）的一些示例（{}部分为应该传入的参数）。

+ 视频：AV 号：av{170001}。
+ 专栏：cv{9762979}。
+ 动态（画册类型）：{116859542}。
+ 动态（纯文本）：{497080393649439253}。

## class CommentResourceType

**Extends:** enum.Enum

资源类型枚举。

+ VIDEO: 视频。
+ ARTICLE: 专栏。
+ DYNAMIC_DRAW: 画册。
+ DYNAMIC: 动态（画册也属于动态的一种，只不过画册还有一个专门的 ID）。
+ AUDIO：音频。
+ AUDIO_LIST：歌单。
+ CHEESE: 课程
+ BLACK_ROOM: 小黑屋
+ MANGA: 漫画

## class ReportReason

举报原因见 https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/comment/action.md#%E4%B8%BE%E6%8A%A5%E8%AF%84%E8%AE%BA

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

## class OrderType

**Extends:** enum.Enum

评论排序方式枚举。

+ LIKE：按点赞数倒序。
+ TIME：按发布时间倒序。

---


## class Comment

对单条评论的相关操作

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

### Functions

#### def \_\_init\_\_()

| name       | type         | description            |
| ---------- | ------------ | ---------------------- |
| oid        | int          | 评论所在资源 ID。      |
| type\_      | CommentResourceType | 评论所在资源类型枚举。 |
| rpid       | int          | 评论 ID。              |
| credential | Credential \| None   | 凭据                   |

#### def get_oid()

获取 OID

**Returns:** OID

#### def get_type()

获取所在资源类型

**Returns:** 资源类型

#### def get_rpid()

获取 rpid

**Returns:** rpid

#### async def like()

| name   | type           | description             |
| ------ | -------------- | ----------------------- |
| status | bool, optional | 状态, Defaults to True. |

点赞评论。

**Returns:** dict: 调用 API 返回的结果

#### async def hate()

| name   | type           | description             |
| ------ | -------------- | ----------------------- |
| status | bool, optional | 状态, Defaults to True. |

点踩评论。

**Returns:** dict: 调用 API 返回的结果

#### async def pin()

| name   | type           | description             |
| ------ | -------------- | ----------------------- |
| status | bool, optional | 状态, Defaults to True. |

置顶评论。

**Returns:** dict: 调用 API 返回的结果

#### async def delete()

删除评论

**Returns:** dict: 调用 API 返回的结果

#### async def report()

| name    | type          | description                                                    |
| ------- | ------------- | -------------------------------------------------------------- |
| reason  | ReportReason  | 举报原因                                                       |
| content | str, optional | 其他举报备注内容仅 reason=ReportReason.OTHER 可用且不能为 None |

举报评论。

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

**Returns:** dict: 调用 API 返回的结果

#### async def get_sub_comments()

| name       | type          | description                         |
| ---------- | ------------- | ----------------------------------- |
| page_index | int, optional | 页码索引，从 1 开始。Defaults to 1. |

获取子评论。即评论下的评论。

**Returns:** dict: 调用 API 返回的结果

---

## async def send_comment()

| name       | type          | description                  |
| ---------- | ------------- | ---------------------------- |
| text       | str           | 评论内容                     |
| oid        | int           | 资源 ID                      |
| type\_      | CommentResourceType  | 资源类型枚举                 |
| root       | int \| None, optional | 根评论 ID, Defaults to None. |
| parent     | int \| None, optional | 父评论 ID, Defaults to None. |
| credential | Credential \| None    | 凭据                         |

通用发送评论 API。

说明 `root` 和 `parent`，假设评论的是视频，常见的评论有三种情况：

1. 只在视频下面发送评论：root=None, parent=None；
2. 回复视频下面的评论：root=评论 ID, parent=None；
3. 回复视频下面的评论中的评论：root=在哪条评论下评论的 ID, parent=回复哪条评论的 ID。

当 root 为空时，parent 必须为空。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_comments()

| name       | type                 | description                               |
| ---------- | -------------------- | ----------------------------------------- |
| oid        | int                  | 资源 ID                                   |
| type\_     | CommentResourceType         | 资源类型枚举                              |
| page_index | int, optional        | 页码. Defaults to 1.                      |
| order      | OrderType, optional  | 排序方式枚举. Defaults to OrderType.TIME. |
| credential | Credential \| None, optional | 凭据. Defaults to None.                   |

获取资源评论列表。

**Returns:** dict: 调用 API 返回的结果
