# Module search.py


bilibili_api.search

搜索


``` python
from bilibili_api import search
```

- [class CategoryTypeArticle()](#class-CategoryTypeArticle)
- [class CategoryTypePhoto()](#class-CategoryTypePhoto)
- [class OrderArticle()](#class-OrderArticle)
- [class OrderCheese()](#class-OrderCheese)
- [class OrderLiveRoom()](#class-OrderLiveRoom)
- [class OrderUser()](#class-OrderUser)
- [class OrderVideo()](#class-OrderVideo)
- [class SearchObjectType()](#class-SearchObjectType)
- [async def get\_default\_search\_keyword()](#async-def-get\_default\_search\_keyword)
- [async def get\_hot\_search\_keywords()](#async-def-get\_hot\_search\_keywords)
- [async def get\_suggest\_keywords()](#async-def-get\_suggest\_keywords)
- [async def search()](#async-def-search)
- [async def search\_by\_type()](#async-def-search\_by\_type)
- [async def search\_cheese()](#async-def-search\_cheese)
- [async def search\_games()](#async-def-search\_games)
- [async def search\_manga()](#async-def-search\_manga)

---

## class CategoryTypeArticle()

**Extend: enum.Enum**

文章分类
+ All 全部
+ Anime 动画
+ Game 游戏
+ TV 电视
+ Life 生活
+ Hobby 兴趣
+ LightNovel 轻小说
+ Technology 科技




---

## class CategoryTypePhoto()

**Extend: enum.Enum**

相册分类
+ All 全部
+ DrawFriend 画友
+ PhotoFriend 摄影




---

## class OrderArticle()

**Extend: enum.Enum**

文章的排序类型
+ TOTALRANK : 综合排序
+ CLICK : 最多点击
+ PUBDATE : 最新发布
+ ATTENTION : 最多喜欢
+ SCORES : 最多评论




---

## class OrderCheese()

**Extend: enum.Enum**

课程搜索排序类型

+ RECOMMEND: 综合
+ SELL : 销量最高
+ NEW  : 最新上架
+ CHEEP: 售价最低




---

## class OrderLiveRoom()

**Extend: enum.Enum**

直播间搜索类型
+ NEWLIVE 最新开播
+ ONLINE 综合排序




---

## class OrderUser()

**Extend: enum.Enum**

搜索用户的排序类型
+ FANS : 按照粉丝数量排序
+ LEVEL : 按照等级排序




---

## class OrderVideo()

**Extend: enum.Enum**

视频搜索类型
+ TOTALRANK : 综合排序
+ CLICK : 最多点击
+ PUBDATE : 最新发布
+ DM : 最多弹幕
+ STOW : 最多收藏
+ SCORES : 最多评论
Ps: Api 中 的 order_sort 字段决定顺序还是倒序





---

## class SearchObjectType()

**Extend: enum.Enum**

搜索对象。
+ VIDEO : 视频
+ BANGUMI : 番剧
+ FT : 影视
+ LIVE : 直播
+ ARTICLE : 专栏
+ TOPIC : 话题
+ USER : 用户
+ LIVEUSER : 直播间用户




---

## async def get_default_search_keyword()

获取默认的搜索内容



**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_hot_search_keywords()

获取热搜



**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_suggest_keywords()

通过一些文字输入获取搜索建议。类似搜索词的联想。


| name | type | description |
| - | - | - |
| `keyword` | `str` | 搜索关键词 |

**Returns:** `List[str]`:  关键词列表




---

## async def search()

只指定关键字在 web 进行搜索，返回未经处理的字典


| name | type | description |
| - | - | - |
| `keyword` | `str` | 搜索关键词 |
| `page` | `int` | 页码. Defaults to 1. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def search_by_type()

指定分区，类型，视频长度等参数进行搜索，返回未经处理的字典

类型：视频(video)、番剧(media_bangumi)、影视(media_ft)、直播(live)、直播用户(liveuser)、专栏(article)、话题(topic)、用户(bili_user)


| name | type | description |
| - | - | - |
| `keyword` | `str` | 搜索关键词 |
| `search_type` | `SearchObjectType \| None, optional` | 搜索类型 |
| `order_type` | `OrderUser \| OrderLiveRoom \| OrderArticle \| OrderVideo \| None, optional` | 排序分类类型 |
| `time_range` | `int, optional` | 指定时间，自动转换到指定区间，只在视频类型下生效 有四种：10分钟以下，10-30分钟，30-60分钟，60分钟以上 |
| `video_zone_type` | `int \| ZoneTypes \| None, optional` | 话题类型，指定 tid (可使用 video_zone 模块查询) |
| `order_sort` | `int \| None, optional` | 用户粉丝数及等级排序顺序 默认为0 由高到低：0 由低到高：1 |
| `category_id` | `CategoryTypeArticle \| CategoryTypePhoto \| int \| None, optional` | 专栏/相簿分区筛选，指定分类，只在相册和专栏类型下生效 |
| `time_start` | `str, optional` | 指定开始时间，与结束时间搭配使用，格式为："YYYY-MM-DD" |
| `time_end` | `str, optional` | 指定结束时间，与开始时间搭配使用，格式为："YYYY-MM-DD" |
| `page` | `int, optional` | 页码 |
| `page_size` | `int, optional` | 每一页的数据大小 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def search_cheese()

搜索课程特用函数


| name | type | description |
| - | - | - |
| `keyword` | `str` | 搜索关键词 |
| `page_num` | `int` | 页码. Defaults to 1. |
| `page_size` | `int` | 每一页的数据大小. Defaults to 30. |
| `order` | `OrderCheese` | 排序方式. Defaults to OrderCheese.RECOMMEND |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def search_games()

搜索游戏特用函数


| name | type | description |
| - | - | - |
| `keyword` | `str` | 搜索关键词 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def search_manga()

搜索漫画特用函数


| name | type | description |
| - | - | - |
| `keyword` | `str` | 搜索关键词 |
| `page_num` | `int` | 页码. Defaults to 1. |
| `page_size` | `int` | 每一页的数据大小. Defaults to 9. |
| `credential` | `Credential` | 凭据类. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




