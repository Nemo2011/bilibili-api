# Module user.py

```python
from bilibili_api import user
```

用户相关。

## class VideoOrder

**Extends:** enum.Enum

视频排序顺序。

+ PUBDATE : 上传日期倒序。
+ FAVORITE: 收藏量倒序。
+ VIEW  : 播放量倒序。

---

## class ChannelOrder

**Extends:** enum.Enum

合集视频排序顺序。

+ DEFAULT: 默认排序
+ CHANGE : 升序排序

---

## class AudioOrder

**Extends:** enum.Enum

音频排序顺序。

+ PUBDATE : 上传日期倒序。
+ FAVORITE: 收藏量倒序。
+ VIEW    : 播放量倒序。

---

## class ArticleOrder

**Extends:** enum.Enum

专栏排序顺序。

+ PUBDATE : 发布日期倒序。
+ FAVORITE: 收藏量倒序。
+ VIEW    : 阅读量倒序。

---

## class AlbumType

**Extends:** enum.Enum

相册内容类型。

+ ALL : 全部。
+ DRAW: 绘画。
+ PHOTO    : 摄影。
+ DAILY    : 日常。

---

## class ArticleListOrder

**Extends:** enum.Enum

文集排序顺序。

+ LATEST: 最近更新倒序。
+ VIEW  : 总阅读量倒序。

---

## class BangumiType

**Extends:** enum.Enum

番剧类型。

+ BANGUMI: 番剧。
+ DRAMA  : 电视剧/纪录片等。

---

## class RelationType

**Extends:** enum.Enum

用户关系操作类型。

+ SUBSCRIBE: 关注。
+ UNSUBSCRIBE: 取关。
+ SUBSCRIBE_SECRETLY: 悄悄关注。
+ BLOCK: 拉黑。
+ UNBLOCK: 取消拉黑。
+ REMOVE_FANS: 移除粉丝。

---

## class ChannelSeriesType

**Extends:** enum.Enum

合集与列表类型

+ SERIES: 旧版
+ SEASON: 新版

**新版合集名字为`合集·XXX`，请注意区别**

---

## class User

用户相关

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

### Functions

#### def \_\_init\_\_()

| name       | type                 | description |
| ---------- | -------------------- | ----------- |
| uid        | int                  | 用户 UID    |
| credential | Credential. optional | 凭据        |

#### def get_uid()

获取 uid

**Returns:** uid

#### async def get_user_info()

获取用户信息（昵称，性别，生日，签名，头像URL，空间横幅URL等）

**Returns:** 调用接口返回的内容。

#### async def get_space_notice()

获取用户空间公告

**Returns:** 调用接口返回的内容。

#### async def get_user_fav_tag()

获取用户关注的 Tag 信息，如果用户设为隐私，则返回 获取登录数据失败

**Returns:** 调用接口返回的内容。

#### async def get_relation_info()

获取用户关系信息（关注数，粉丝数，悄悄关注，黑名单数）

**Returns:** 调用接口返回的内容。

#### async def get_up_stat()

获取 UP 主数据信息（视频总播放量，文章总阅读量，总点赞数）

**Returns:** 调用接口返回的内容。

#### async def get_top_videos()

获取用户的置顶视频

**Returns:** 调用接口返回的结果

#### async def get_user_medal()

读取用户粉丝牌详细列表，如果隐私则不可以,需要登录状态，返回的数据带有 查询者的 uid

**Returns:** 调用接口返回的内容。

#### async def get_live_info()

获取用户直播间信息。

**Returns:** 调用接口返回的内容。

#### async def get_videos()

| name    | type                 | description                          |
|---------|----------------------|--------------------------------------|
| tid     | int, optional        | 分区 ID. Defaults to 0（全部）             |
| pn      | int, optional        | 页码，从 1 开始. Defaults to 1.            |
| ps      | (int, optional)      | 每一页的视频数. Defaults to 30.             |
| keyword | str, optional        | 搜索关键词. Defaults to "".               |
| order   | VideoOrder, optional | 排序方式. Defaults to VideoOrder.PUBDATE |

获取用户投稿视频信息。

**Returns:** 调用接口返回的内容。

#### async def get_album()

| name      | type                | description                     |
|-----------|---------------------|---------------------------------|
| page_num  | int, optional       | 页码，从 1 开始. Defaults to 1.       |
| page_size | int, optional       | 每一页的相簿. Defaults to 30.         |
| biz       | AlbumType, optional | 排序方式. Defaults to AlbumType.ALL |

获取用户投稿相簿。

**Returns:** 调用接口返回的内容。

#### async def get_audios()

| name  | type                 | description                           |
|-------|----------------------|---------------------------------------|
| order | AudioOrder, optional | 排序方式. Defaults to AudioOrder.PUBDATE. |
| pn    | int, optional        | 页码，从 1 开始. Defaults to 1.             |
| ps    | (int, optional)      | 每一页的视频数. Defaults to 30.              |

获取用户投稿音频。

**Returns:** 调用接口返回的内容。

#### async def get_articles()

| name  | type                   | description                             |
|-------|------------------------|-----------------------------------------|
| order | ArticleOrder, optional | 排序方式. Defaults to ArticleOrder.PUBDATE. |
| pn    | int, optional          | 页码，从 1 开始. Defaults to 1.               |

获取用户投稿专栏。

**Returns:** 调用接口返回的内容。

#### async def get_article_list()

| name  | type                       | description                               |
|-------|----------------------------|-------------------------------------------|
| order | ArticleListOrder, optional | 排序方式. Defaults to ArticleListOrder.LATEST |
| pn    | (int, optional)            | 页码数，从 1 开始。 Defaults to 1.                |
| ps    | (int, optional)            | 每一页的视频数. Defaults to 30.                  |

获取用户专栏文集。

**Returns:** 调用接口返回的内容。

#### async def get_channel_list()

查看用户所有的频道（包括新版）和部分视频。
适用于获取列表。

**Returns:** 调用接口返回的内容。

#### async def get_channel_videos_series()

查看频道内所有视频。仅供 series_list。

| name | type | description                            |
|------|------|----------------------------------------|
| sid  | int  | 合集的 series_id (通过 get_channel_list 获取) |
| pn   | int  | 页数，默认为1                                |
| ps   | int  | 每一页显示的视频数量，默认为100                      |

**Returns:** 调用接口返回的内容。

#### async def get_channel_videos_season()

查看频道内所有视频。仅供 season_list。

| name | type         | description                               |
|------|--------------|-------------------------------------------|
| sid  | int          | 季度 id(season_id) (通过 get_channel_list 获取) |
| sort | ChannelOrder | 排序方式，默认为“默认排序”                            |
| pn   | int          | 页数，默认为1                                   |
| ps   | int          | 每一页显示的视频数量，默认为100                         |

**Returns:** 调用接口返回的内容。

#### async def get_dynamics()

| name     | type           | description                                                                                                                                          |
|----------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| offset   | str, optional  | 该值为第一次调用本方法时，数据中会有个 next_offset 字段，<br/>指向下一动态列表第一条动态（类似单向链表）。<br/>根据上一次获取结果中的 next_offset 字段值，<br/>循环填充该值即可获取到全部动态。<br/>0 为从头开始。<br/>Defaults to 0. |
| need_top | bool, optional | 显示置顶动态. Defaults to False.                                                                                                                           |

获取用户动态。

**Returns:** 调用接口返回的内容。

#### async def get_cheese()

查看用户的所有课程

**Returns**:调用接口返回的结果

#### async def get_subscribed_bangumi()

| name  | type                  | description                           |
|-------|-----------------------|---------------------------------------|
| pn    | int, optional         | 页码数，从 1 开始。 Defaults to 1.            |
| type_ | BangumiType, optional | 资源类型. Defaults to BangumiType.BANGUMI |

获取用户追番/追剧列表。

**Returns:** 调用接口返回的内容。

#### async def get_reservation()

获取用户空间预约

**Returns:** 调用 API 返回的结果

#### async def get_followings()

| name | type           | description               |
|------|----------------|---------------------------|
| pn   | int, optional  | 页码，从 1 开始. Defaults to 1. |
| desc | bool, optional | 倒序排序. Defaults to True.   |

获取用户关注列表（不是自己只能访问前5页）

**Returns:** 调用接口返回的内容。

#### async def get_all_followings()

获取所有的关注列表。（如果用户设置保密会没有任何数据）

**Returns:** list: 关注列表

#### async def get_followers()

| name | type           | description               |
|------|----------------|---------------------------|
| pn   | int, optional  | 页码，从 1 开始. Defaults to 1. |
| desc | bool, optional | 倒序排序. Defaults to True.   |

获取用户粉丝列表（不是自己只能访问前5页，是自己也不能获取全部的样子）

**Returns:** 调用接口返回的内容。

#### async def top_followers()

| name | type           | description                     |
| ---- | -------------- | ------------------------------- |
| since   | int, optional  | 开始查找的时间戳， 毫秒为单位|

粉丝排行

**Returns:** 调用接口返回的内容。

#### async def get_overview_stat()

获取用户的简易订阅和投稿信息。

**Returns:** 调用接口返回的内容。

#### async def modify_relation()

| name     | type         | description |
|----------|--------------|-------------|
| relation | RelationType | 用户关系        |

修改和用户的关系，比如拉黑、关注、取关等。

**Returns:** 调用接口返回的内容。

#### async def set_space_notice()

| name   | type | description |
|--------|------|-------------|
| notice | str  | 需要修改为？可以留空  |

修改用户空间公告。

**Returns:** 调用接口返回的内容。

---

## async def get_self_info()

| name       | type       | description |
|------------|------------|-------------|
| credential | Credential | 凭据          |

获取自己的信息。

**Returns:** 调用接口返回的内容。

---

## class ChannelSeries

合集与列表类

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| uid | int | 用户 uid |
| type_ | ChannelSeriesType | 合集与列表的类型，分旧版和新版 |
| id_ | int | season_id 或 series_id |
| credential | Credential | 凭据类 |

#### def get_meta()

获取元数据

**Returns:** 调用接口返回的内容。

#### async def get_videos()

获取合集视频

**Returns:** 调用接口返回的内容。

---

## async def create_subscribe_group()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| name       | str        | 分组名      |
| credential | Credential | 凭据        |

创建用户关注分组

**Returns:** 调用接口返回的内容。

---

## async def delete_subscribe_group()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| group_id   | int        | 分组 ID     |
| credential | Credential | 凭据        |

删除用户关注分组

**Returns:** 调用接口返回的内容。

---

## async def rename_subscribe_group()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| group_id   | int        | 分组 ID     |
| new_name   | str        | 新的分组名  |
| credential | Credential | 凭据        |

重命名关注分组

**Returns:** 调用接口返回的内容。

---

## async def set_subscribe_group()

| name       | type       | description                         |
| ---------- | ---------- | ----------------------------------- |
| uids       | List[int]  | 要设置的用户 UID 列表，必须已关注。 |
| group_ids  | List[int]  | 要复制到的分组列表                  |
| credential | Credential | 凭据                                |

设置用户关注分组

**Returns:** 调用接口返回的内容。

---

## async def get_self_history()

| name          | type          | description                         |
| ------------- | ------------- | ----------------------------------- |
| page_num      | int, optional | 页码数. Defaults to 1               |
| per_page_item | int, optional | 每页多少条历史记录, Defaults to 100 |
| credential    | Credential    | 凭据                                |

获取用户浏览历史记录

**Returns:** 返回当前页的指定历史记录列表。

---

## async def get_self_coins()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据 |

获取自己的硬币数量

**Returns:** int: 硬币数量

---

## async def get_toview_list()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据 |

获取自己的稍后再看列表

**Returns:** dict: 调用 API 返回的结果

---

## async def clear_toview_list()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据 |

清空自己的稍后再看列表

**Returns:** dict: 调用 API 返回的结果

---

## async def delete_viewed_videos_from_toview()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据 |

删除稍后再看列表中已经看过（看完）的视频

**Returns:** dict: 调用 API 返回的结果

---

## async def get_self_level()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据 |

获取自己的电磁力等级

**Returns:** tuple[bool, str]: 第一项为昵称是否可用，第二项为不可用的原因。

---

## async def get_self_events()

| name | type | description |
| - | - | - |
| ts | int, optional | 时间戳. Defaults to 0 |
| credential | Credential, optional | 凭据类. Defaults to None |

获取自己入站后每一刻的事件(可以不带 credential)

**Returns:** dict: 调用 API 返回的结果