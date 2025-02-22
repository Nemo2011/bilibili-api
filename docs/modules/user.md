# Module user.py


bilibili_api.user

用户相关


``` python
from bilibili_api import user
```

- [class AlbumType()](#class-AlbumType)
- [class ArticleListOrder()](#class-ArticleListOrder)
- [class ArticleOrder()](#class-ArticleOrder)
- [class AudioOrder()](#class-AudioOrder)
- [class BangumiFollowStatus()](#class-BangumiFollowStatus)
- [class BangumiType()](#class-BangumiType)
- [class HistoryBusinessType()](#class-HistoryBusinessType)
- [class HistoryType()](#class-HistoryType)
- [class MedialistOrder()](#class-MedialistOrder)
- [class OpusType()](#class-OpusType)
- [class OrderType()](#class-OrderType)
- [class RelationType()](#class-RelationType)
- [class User()](#class-User)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_access\_id()](#async-def-get\_access\_id)
  - [async def get\_album()](#async-def-get\_album)
  - [async def get\_all\_followings()](#async-def-get\_all\_followings)
  - [async def get\_article\_list()](#async-def-get\_article\_list)
  - [async def get\_articles()](#async-def-get\_articles)
  - [async def get\_audios()](#async-def-get\_audios)
  - [async def get\_channel\_list()](#async-def-get\_channel\_list)
  - [async def get\_channel\_videos\_season()](#async-def-get\_channel\_videos\_season)
  - [async def get\_channel\_videos\_series()](#async-def-get\_channel\_videos\_series)
  - [async def get\_channels()](#async-def-get\_channels)
  - [async def get\_cheese()](#async-def-get\_cheese)
  - [async def get\_dynamics()](#async-def-get\_dynamics)
  - [async def get\_dynamics\_new()](#async-def-get\_dynamics\_new)
  - [async def get\_elec\_user\_monthly()](#async-def-get\_elec\_user\_monthly)
  - [async def get\_followers()](#async-def-get\_followers)
  - [async def get\_followings()](#async-def-get\_followings)
  - [async def get\_live\_info()](#async-def-get\_live\_info)
  - [async def get\_masterpiece()](#async-def-get\_masterpiece)
  - [async def get\_media\_list()](#async-def-get\_media\_list)
  - [async def get\_opus()](#async-def-get\_opus)
  - [async def get\_overview\_stat()](#async-def-get\_overview\_stat)
  - [async def get\_relation()](#async-def-get\_relation)
  - [async def get\_relation\_info()](#async-def-get\_relation\_info)
  - [async def get\_reservation()](#async-def-get\_reservation)
  - [async def get\_self\_same\_followers()](#async-def-get\_self\_same\_followers)
  - [async def get\_space\_notice()](#async-def-get\_space\_notice)
  - [async def get\_subscribed\_bangumi()](#async-def-get\_subscribed\_bangumi)
  - [async def get\_top\_videos()](#async-def-get\_top\_videos)
  - [def get\_uid()](#def-get\_uid)
  - [async def get\_up\_stat()](#async-def-get\_up\_stat)
  - [async def get\_uplikeimg()](#async-def-get\_uplikeimg)
  - [async def get\_user\_fav\_tag()](#async-def-get\_user\_fav\_tag)
  - [async def get\_user\_info()](#async-def-get\_user\_info)
  - [async def get\_user\_medal()](#async-def-get\_user\_medal)
  - [async def get\_videos()](#async-def-get\_videos)
  - [async def modify\_relation()](#async-def-modify\_relation)
  - [async def set\_space\_notice()](#async-def-set\_space\_notice)
  - [async def top\_followers()](#async-def-top\_followers)
- [class VideoOrder()](#class-VideoOrder)
- [async def check\_nickname()](#async-def-check\_nickname)
- [async def clear\_toview\_list()](#async-def-clear\_toview\_list)
- [async def create\_subscribe\_group()](#async-def-create\_subscribe\_group)
- [async def delete\_subscribe\_group()](#async-def-delete\_subscribe\_group)
- [async def delete\_viewed\_videos\_from\_toview()](#async-def-delete\_viewed\_videos\_from\_toview)
- [async def edit\_self\_info()](#async-def-edit\_self\_info)
- [async def get\_self\_black\_list()](#async-def-get\_self\_black\_list)
- [async def get\_self\_coins()](#async-def-get\_self\_coins)
- [async def get\_self\_events()](#async-def-get\_self\_events)
- [async def get\_self\_experience\_log()](#async-def-get\_self\_experience\_log)
- [async def get\_self\_friends()](#async-def-get\_self\_friends)
- [async def get\_self\_history()](#async-def-get\_self\_history)
- [async def get\_self\_history\_new()](#async-def-get\_self\_history\_new)
- [async def get\_self\_info()](#async-def-get\_self\_info)
- [async def get\_self\_jury\_info()](#async-def-get\_self\_jury\_info)
- [async def get\_self\_login\_log()](#async-def-get\_self\_login\_log)
- [async def get\_self\_moral\_log()](#async-def-get\_self\_moral\_log)
- [async def get\_self\_notes\_info()](#async-def-get\_self\_notes\_info)
- [async def get\_self\_public\_notes\_info()](#async-def-get\_self\_public\_notes\_info)
- [async def get\_self\_special\_followings()](#async-def-get\_self\_special\_followings)
- [async def get\_self\_whisper\_followings()](#async-def-get\_self\_whisper\_followings)
- [async def get\_toview\_list()](#async-def-get\_toview\_list)
- [async def name2uid()](#async-def-name2uid)
- [async def rename\_subscribe\_group()](#async-def-rename\_subscribe\_group)
- [async def set\_subscribe\_group()](#async-def-set\_subscribe\_group)

---

## class AlbumType()

**Extend: enum.Enum**

相册类型

+ ALL : 全部。
+ DRAW: 绘画。
+ PHOTO: 摄影。
+ DAILY: 日常。




---

## class ArticleListOrder()

**Extend: enum.Enum**

文集排序顺序。

+ LATEST: 最近更新倒序。
+ VIEW  : 总阅读量倒序。




---

## class ArticleOrder()

**Extend: enum.Enum**

专栏排序顺序。

+ PUBDATE : 发布日期倒序。
+ FAVORITE: 收藏量倒序。
+ VIEW: 阅读量倒序。




---

## class AudioOrder()

**Extend: enum.Enum**

音频排序顺序。

+ PUBDATE : 上传日期倒序。
+ FAVORITE: 收藏量倒序。
+ VIEW: 播放量倒序。




---

## class BangumiFollowStatus()

**Extend: enum.Enum**

番剧追番状态类型。

+ ALL: 全部
+ WANT   : 想看
+ WATCHING   : 在看
+ WATCHED: 已看




---

## class BangumiType()

**Extend: enum.Enum**

番剧类型。

+ BANGUMI: 番剧。
+ DRAMA  : 电视剧/纪录片等。




---

## class HistoryBusinessType()

**Extend: enum.Enum**

历史记录 Business 分类

+ archive：稿件
+ pgc：剧集（番剧 / 影视）
+ live：直播
+ article-list：文集
+ article：文章




---

## class HistoryType()

**Extend: enum.Enum**

历史记录分类

+ ALL  : 全部
+ archive  : 稿件
+ live : 直播
+ article  : 专栏




---

## class MedialistOrder()

**Extend: enum.Enum**

medialist排序顺序。

+ PUBDATE : 上传日期。
+ PLAY: 播放量。
+ COLLECT : 收藏量。




---

## class OpusType()

**Extend: enum.Enum**

图文类型

+ ALL: 所有
+ ARTICLE: 属于专栏的图文
+ DYNAMIC: 不属于专栏（但为动态）的图文




---

## class OrderType()

**Extend: enum.Enum**

排序字段

+ desc：倒序
+ asc：正序




---

## class RelationType()

**Extend: enum.Enum**

用户关系操作类型。

+ SUBSCRIBE : 关注。
+ UNSUBSCRIBE   : 取关。
+ SUBSCRIBE_SECRETLY: 悄悄关注。已失效
+ BLOCK : 拉黑。
+ UNBLOCK   : 取消拉黑。
+ REMOVE_FANS   : 移除粉丝。




---

## class User()

用户相关




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `uid` | `int` | 用户 UID |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |


### async def get_access_id()

获取用户 access_id (w_webid) 如未过期直接从本地获取 防止重复请求



**Returns:** `str`:  access_id




### async def get_album()

获取用户投稿相簿。


| name | type | description |
| - | - | - |
| `biz` | `AlbumType, optional` | 排序方式. Defaults to AlbumType.ALL. |
| `page_num` | `int, optional` | 页码数，从 1 开始。 Defaults to 1. |
| `page_size` | `int` | 每一页的相簿条目. Defaults to 30. |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_all_followings()

获取所有的关注列表。（如果用户设置保密会没有任何数据）



**Returns:** `list`:  关注列表




### async def get_article_list()

获取用户专栏文集。


| name | type | description |
| - | - | - |
| `order` | `ArticleListOrder, optional` | 排序方式. Defaults to ArticleListOrder.LATEST |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_articles()

获取用户投稿专栏。


| name | type | description |
| - | - | - |
| `order` | `ArticleOrder, optional` | 排序方式. Defaults to ArticleOrder.PUBDATE. |
| `pn` | `int, optional` | 页码数，从 1 开始。 Defaults to 1. |
| `ps` | `int, optional` | 每一页的视频数. Defaults to 30. |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_audios()

获取用户投稿音频。


| name | type | description |
| - | - | - |
| `order` | `AudioOrder, optional` | 排序方式. Defaults to AudioOrder.PUBDATE. |
| `pn` | `int, optional` | 页码数，从 1 开始。 Defaults to 1. |
| `ps` | `int, optional` | 每一页的视频数. Defaults to 30. |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_channel_list()

查看用户所有的频道（包括新版）和部分视频。

适用于获取列表。

未处理数据。不推荐。



**Returns:** `dict`:  调用接口返回的结果




### async def get_channel_videos_season()

查看频道内所有视频。仅供 season_list。


| name | type | description |
| - | - | - |
| `sid` | `int` | 频道的 season_id |
| `sort` | `ChannelOrder` | 排序方式 |
| `pn` | `int` | 页数，默认为 1 |
| `ps` | `int` | 每一页显示的视频数量 |

**Returns:** `dict`:  调用接口返回的内容




### async def get_channel_videos_series()

查看频道内所有视频。仅供 series_list。


| name | type | description |
| - | - | - |
| `sid` | `int` | 频道的 series_id |
| `pn` | `int` | 页数，默认为 1 |
| `ps` | `int` | 每一页显示的视频数量 |

**Returns:** `dict`:  调用接口返回的内容




### async def get_channels()

获取用户所有合集



**Returns:** `List[ChannelSeries]`:  合集与列表类的列表




### async def get_cheese()

查看用户的所有课程



**Returns:** `dict`:  调用接口返回的结果




### async def get_dynamics()

获取用户动态。

建议使用 user.get_dynamics_new() 新接口。


| name | type | description |
| - | - | - |
| `offset` | `str, optional` | 该值为第一次调用本方法时，数据中会有个 next_offset 字段，指向下一动态列表第一条动态（类似单向链表）。根据上一次获取结果中的 next_offset 字段值，循环填充该值即可获取到全部动态。0 为从头开始。Defaults to 0. |
| `need_top` | `bool, optional` | 显示置顶动态. Defaults to False. |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_dynamics_new()

获取用户动态。


| name | type | description |
| - | - | - |
| `offset` | `str, optional` | 该值为第一次调用本方法时，数据中会有个 offset 字段，指向下一动态列表第一条动态（类似单向链表）。根据上一次获取结果中的 next_offset 字段值，循环填充该值即可获取到全部动态。空字符串为从头开始。Defaults to "". |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_elec_user_monthly()

获取空间充电公示信息



**Returns:** `dict`:  调用接口返回的结果




### async def get_followers()

获取用户粉丝列表（不是自己只能访问前 5 页，是自己也不能获取全部的样子）


| name | type | description |
| - | - | - |
| `pn` | `int, optional` | 页码，从 1 开始. Defaults to 1. |
| `ps` | `int, optional` | 每页的数据量. Defaults to 100. |
| `desc` | `bool, optional` | 倒序排序. Defaults to True. |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_followings()

获取用户关注列表（不是自己只能访问前 5 页）


| name | type | description |
| - | - | - |
| `pn` | `int, optional` | 页码，从 1 开始. Defaults to 1. |
| `ps` | `int, optional` | 每页的数据量. Defaults to 100. |
| `attention` | `bool, optional` | 是否采用“最常访问”排序，否则为“关注顺序”排序. Defaults to False. |
| `order` | `OrderType, optional` | 排序方式. Defaults to OrderType.desc. |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_live_info()

获取用户直播间信息。



**Returns:** `dict`:  调用接口返回的内容。




### async def get_masterpiece()

获取用户代表作



**Returns:** `list`:  调用接口返回的内容。




### async def get_media_list()

以 medialist 形式获取用户投稿信息。


| name | type | description |
| - | - | - |
| `oid` | `int, optional` | 起始视频 aid， 默认为列表开头 |
| `ps` | `int, optional` | 每一页的视频数. Defaults to 20. Max 100 |
| `direction` | `bool, optional` | 相对于给定oid的查询方向 True 向列表末尾方向 False 向列表开头方向 Defaults to False. |
| `desc` | `bool, optional` | 倒序排序. Defaults to True. |
| `sort_field` | `int, optional` | 用于排序的栏  1 发布时间，2 播放量，3 收藏量 |
| `tid` | `int, optional` | 分区 ID. Defaults to 0（全部）. 1 部分（未知） |
| `with_current` | `bool, optional` | 返回的列表中是否包含给定oid自身 Defaults to False. |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_opus()

获取用户发布过的图文


| name | type | description |
| - | - | - |
| `type_` | `OpusType, optional` | 获取的图文类型. Defaults to OpusType.ALL. |
| `offset` | `str, optional` | 偏移量。每次请求可获取下次请求对应的偏移量，类似单向链表。对应返回结果的 `["offset"]` Defaults to "". |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_overview_stat()

获取用户的简易订阅和投稿信息。



**Returns:** `dict`:  调用接口返回的内容。




### async def get_relation()

获取与某用户的关系



**Returns:** `dict`:  调用接口返回的内容。




### async def get_relation_info()

获取用户关系信息（关注数，粉丝数，悄悄关注，黑名单数）



**Returns:** `dict`:  调用接口返回的内容。




### async def get_reservation()

获取用户空间预约



**Returns:** `dict`:  调用接口返回的结果




### async def get_self_same_followers()

获取用户与自己共同关注的 up 主


| name | type | description |
| - | - | - |
| `pn` | `int` | 页码. Defaults to 1. |
| `ps` | `int` | 单页数据量. Defaults to 50. |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_space_notice()

获取用户空间公告



**Returns:** `dict`:  调用接口返回的内容。




### async def get_subscribed_bangumi()

获取用户追番/追剧列表。


| name | type | description |
| - | - | - |
| `pn` | `int, optional` | 页码数，从 1 开始。 Defaults to 1. |
| `ps` | `int, optional` | 每一页的番剧数. Defaults to 15. |
| `type_` | `BangumiType, optional` | 资源类型. Defaults to BangumiType.BANGUMI |
| `follow_status` | `BangumiFollowStatus, optional` | 追番状态. Defaults to BangumiFollowStatus.ALL |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_top_videos()

获取用户的指定视频（代表作）



**Returns:** `dict`:  调用接口返回的内容。




### def get_uid()

获取用户 UID



**Returns:** `int`:  用户 UID




### async def get_up_stat()

获取 UP 主数据信息（视频总播放量，文章总阅读量，总点赞数）



**Returns:** `dict`:  调用接口返回的内容。




### async def get_uplikeimg()

视频三联特效



**Returns:** `dict`:  调用 API 返回的结果




### async def get_user_fav_tag()

获取用户关注的 Tag 信息，如果用户设为隐私，则返回 获取登录数据失败


| name | type | description |
| - | - | - |
| `pn` | `int, optional` | 页码，从 1 开始. Defaults to 1. |
| `ps` | `int, optional` | 每页的数据量. Defaults to 20. |

**Returns:** `dict`:  调用接口返回的内容。




### async def get_user_info()

获取用户信息（昵称，性别，生日，签名，头像 URL，空间横幅 URL 等）



**Returns:** `dict`:  调用接口返回的内容。


[用户空间详细信息](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/user/info.md#%E7%94%A8%E6%88%B7%E7%A9%BA%E9%97%B4%E8%AF%A6%E7%BB%86%E4%BF%A1%E6%81%AF)



### async def get_user_medal()

读取用户粉丝牌详细列表，如果隐私则不可以



**Returns:** `dict`:  调用接口返回的内容。




### async def get_videos()

获取用户投稿视频信息。


| name | type | description |
| - | - | - |
| `tid` | `int, optional` | 分区 ID. Defaults to 0（全部）. |
| `pn` | `int, optional` | 页码，从 1 开始. Defaults to 1. |
| `ps` | `int, optional` | 每一页的视频数. Defaults to 30. |
| `keyword` | `str, optional` | 搜索关键词. Defaults to "". |
| `order` | `VideoOrder, optional` | 排序方式. Defaults to VideoOrder.PUBDATE |

**Returns:** `dict`:  调用接口返回的内容。




### async def modify_relation()

修改和用户的关系，比如拉黑、关注、取关等。


| name | type | description |
| - | - | - |
| `relation` | `RelationType` | 用户关系。 |

**Returns:** `dict`:  调用接口返回的内容。




### async def set_space_notice()

修改用户空间公告


| name | type | description |
| - | - | - |
| `content` | `str` | 需要修改的内容 |

**Returns:** `dict`:  调用接口返回的内容。




### async def top_followers()

获取用户粉丝排行

| name | type | description |
| - | - | - |
| `since` | `int, optional` | 开始时间(msec) |

**Returns:** `dict`:  调用接口返回的内容。




---

## class VideoOrder()

**Extend: enum.Enum**

视频排序顺序。

+ PUBDATE : 上传日期倒序。
+ FAVORITE: 收藏量倒序。
+ VIEW: 播放量倒序。




---

## async def check_nickname()

检验昵称是否可用


| name | type | description |
| - | - | - |
| `nick_name` | `str` | 昵称 |

**Returns:** `List[bool, str]`:  昵称是否可用 + 不可用原因




---

## async def clear_toview_list()

清空稍后再看列表


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def create_subscribe_group()

创建用户关注分组


| name | type | description |
| - | - | - |
| `name` | `str` | 分组名 |
| `credential` | `Credential` | Credential |

**Returns:** `dict`:  API 调用返回结果。




---

## async def delete_subscribe_group()

删除用户关注分组


| name | type | description |
| - | - | - |
| `group_id` | `int` | 分组 ID |
| `credential` | `Credential` | Credential |

**Returns:** `dict`:  调用 API 返回结果




---

## async def delete_viewed_videos_from_toview()

删除稍后再看列表已经看过的视频


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def edit_self_info()

修改自己的信息 (Web)


| name | type | description |
| - | - | - |
| `birthday` | `str` | 生日 YYYY-MM-DD |
| `sex` | `str` | 性别 男|女|保密 |
| `uname` | `str` | 用户名 |
| `usersign` | `str` | 个性签名 |
| `credential` | `Credential` | Credential |




---

## async def get_self_black_list()

获取自己的黑名单信息


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |
| `pn` | `int, optional` | 页码. Defaults to 1. |
| `ps` | `int, optional` | 每页数据大小. Defaults to 50. |




---

## async def get_self_coins()

获取自己的硬币数量。



**Returns:** `int`:  硬币数量




---

## async def get_self_events()

获取自己入站后每一刻的事件


| name | type | description |
| - | - | - |
| `ts` | `int, optional` | 时间戳. Defaults to 0. |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_self_experience_log()

获取自己的经验记录


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭证。 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_self_friends()

获取与自己互粉的人


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |




---

## async def get_self_history()

获取用户浏览历史记录（旧版）


| name | type | description |
| - | - | - |
| `page_num` | `int` | 页码数 |
| `per_page_item` | `int` | 每页多少条历史记录 |
| `credential` | `Credential` | Credential |

**Returns:** `list(dict)`:  返回当前页的指定历史记录列表




---

## async def get_self_history_new()

获取用户浏览历史记录（新版），与旧版不同有分类参数，但相对缺少视频信息

max、business、view_at 参数用于历史记录列表的 IFS (无限滚动)，其用法类似链表的 next 指针

将返回值某历史记录的 oid、business、view_at 作为上述参数传入，即可获取此 oid 之前的历史记录


| name | type | description |
| - | - | - |
| `credential` | `Credential` | Credential |
| `_type` | `HistroyType` | 历史记录分类, 默认为 HistroyType.ALL |
| `ps` | `int` | 每页多少条历史记录, 默认为 20 |
| `view_at` | `int` | 时间戳，获取此时间戳之前的历史记录 |
| `max` | `int` | 历史记录截止目标 oid |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_self_info()

获取自己的信息


| name | type | description |
| - | - | - |
| `credential` | `Credential` | Credential |




---

## async def get_self_jury_info()

获取自己风纪委员信息






---

## async def get_self_login_log()

获取自己的登录记录


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭证。 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_self_moral_log()

获取自己的节操记录


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭证。 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_self_notes_info()

获取自己的笔记列表


| name | type | description |
| - | - | - |
| `page_num` | `int` | 页码 |
| `page_size` | `int` | 每页项数 |
| `credential` | `Credential` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_self_public_notes_info()

获取自己的公开笔记列表


| name | type | description |
| - | - | - |
| `page_num` | `int` | 页码 |
| `page_size` | `int` | 每页项数 |
| `credential` | `Credential` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_self_special_followings()

获取自己特殊关注的列表


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |
| `pn` | `int, optional` | 页码. Defaults to 1. |
| `ps` | `int, optional` | 每页数据大小. Defaults to 50. |




---

## async def get_self_whisper_followings()

获取自己悄悄关注的列表。


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |
| `pn` | `int, optional` | 页码. Defaults to 1. |
| `ps` | `int, optional` | 每页数据大小. Defaults to 50. |




---

## async def get_toview_list()

获取稍后再看列表


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def name2uid()

将用户名转为 uid


| name | type | description |
| - | - | - |
| `names` | `str/List[str]` | 用户名 |
| `credential` | `Credential, optional` | 凭据类. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def rename_subscribe_group()

重命名关注分组


| name | type | description |
| - | - | - |
| `group_id` | `int` | 分组 ID |
| `new_name` | `str` | 新的分组名 |
| `credential` | `Credential` | Credential |

**Returns:** `dict`:  调用 API 返回结果




---

## async def set_subscribe_group()

设置用户关注分组


| name | type | description |
| - | - | - |
| `uids` | `List[int]` | 要设置的用户 UID 列表，必须已关注。 |
| `group_ids` | `List[int]` | 要复制到的分组列表 |
| `credential` | `Credential` | Credential |

**Returns:** `dict`:  API 调用结果




