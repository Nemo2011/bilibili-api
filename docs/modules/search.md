# Module search.py

```python
from bilibili_api import search
```

各种杂类操作（主页搜索 API）

## class SearchObjectType

**Extends:** enum.Enum

搜索对象。

+ VIDEO : 视频
+ BANGUMI : 番剧
+ FT : 影视
+ LIVE : 直播
+ ARTICLE : 专栏
+ TOPIC : 话题
+ USER : 用户

## class CategoryTypeArticle

**Extends:** enum.Enum

文章分类

+ All 全部
+ Anime
+ Game
+ TV
+ Life
+ Hobby
+ LightNovel
+ Technology

## class CategoryTypePhoto

**Extends:** enum.Enum

相册分类

+ All 全部
+ DrawFriend 画友
+ PhotoFriend 摄影

## class OrderUser

**Extends:** enum.Enum

搜索用户的排序类型

+ FANS : 按照粉丝数量排序
+ LEVEL : 按照等级排序

## class OrderArticle

**Extends:** enum.Enum

文章的排序类型

+ TOTALRANK : 综合排序
+ CLICK : 最多点击
+ PUBDATE : 最新发布
+ ATTENTION : 最多喜欢
+ SCORES : 最多评论

## class OrderLiveRoom

**Extends:** enum.Enum

直播间搜索类型

+ NEWLIVE 最新开播
+ ONLINE 综合排序

## class OrderVideo

**Extends:** enum.Enum

视频搜索类型

+ TOTALRANK : 综合排序
+ CLICK : 最多点击
+ PUBDATE : 最新发布
+ DM : 最多弹幕
+ STOW : 最多收藏
+ SCORES : 最多评论
  Ps: Api 中 的 order_sort 字段决定顺序还是倒序

## async def search()

只指定关键字在 web 进行搜索，返回未经处理的字典

| name    | type   | description      |
|---------|--------|------------------|
| keyword | str | 搜索关键词            |
| page    | int    | 页数. Defaults to 1 |

**Returns:** dict: 调用 API 返回的结果

## async def search_by_type()

指定关键字和类型进行搜索，返回未经处理的字典

| name             | type                                            | description                                                |
|------------------|-------------------------------------------------|------------------------------------------------------------|
| keyword          | str                                          | 搜索关键词                                                      |
| search_type      | SearchObjectType, None                                | 搜索类别                                                       |
| order_type       | UserOrder,VideoOrder,ArticleOrder,LiveRoomOrder,None | 排序分类类型                                                     |
| time_range       | int                                             | 指定时间，自动转换到指定区间，只在视频类型下生效 有四种：10分钟以下，10-30分钟，30-60分钟，60分钟以上 |
| topic_type       | int , channel.ChannelTypes                                 | 话题 tids                                                    |
| order_sort       | int                                             | 仅用于用户用户，设置粉丝数及等级排序顺序,默认,由高到低:0 ,由低到高：1                     |
| category_id      | int,CategoryTypePhoto,CategoryTypeArticle,None    | 专栏/相册专用类型                                                  |
| debug_param_func | Callable,None                                           | 参数回调器，用来存储或者什么的                                            |
| page             | int                                             | 页数，defaults to 1                                           |

**Returns:** dict: 调用 API 返回的结果

## async def get_default_search_keyword()

获取默认的搜索内容

**Returns:** dict: 调用 API 返回的结果

## async def get_hot_search_keywords()

获取热搜

**Returns:** dict: 调用 API 返回的结果

## async def get_suggest_keywords()

| name | type | description |
| - | - | - |
| keyword | str | 搜索关键词 |

通过一些文字输入获取搜索建议。类似搜索词的联想。

**Returns:** List[str]: 关键词列表

## async def search_games()

| name | type | description |
| - | - | - |
| keyword | str | 搜索关键词 |

搜索游戏特用函数

**Returns:** dict: 调用 API 返回的结果

## async def search_manga()

| name | type | description |
| - | - | - |
| keyword | str | 搜索关键词 |
| page_num | int | 页码. Defaults to 1. |
| page_size | int | 每一页的数据大小. Defaults to 9. |

搜索漫画特用函数

**Returns:** dict: 调用 API 返回的结果
