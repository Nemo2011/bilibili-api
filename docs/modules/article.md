# Module article.py


bilibili_api.article

专栏相关


``` python
from bilibili_api import article
```

- [class Article()](#class-Article)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def add\_coins()](#async-def-add\_coins)
  - [async def fetch\_content()](#async-def-fetch\_content)
  - [async def get\_all()](#async-def-get\_all)
  - [def get\_cvid()](#def-get\_cvid)
  - [async def get\_detail()](#async-def-get\_detail)
  - [async def get\_info()](#async-def-get\_info)
  - [async def is\_note()](#async-def-is\_note)
  - [def json()](#def-json)
  - [def markdown()](#def-markdown)
  - [async def set\_favorite()](#async-def-set\_favorite)
  - [async def set\_like()](#async-def-set\_like)
  - [async def turn\_to\_dynamic()](#async-def-turn\_to\_dynamic)
  - [def turn\_to\_note()](#def-turn\_to\_note)
  - [async def turn\_to\_opus()](#async-def-turn\_to\_opus)
- [class ArticleList()](#class-ArticleList)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_content()](#async-def-get\_content)
  - [def get\_rlid()](#def-get\_rlid)
- [class ArticleRankingType()](#class-ArticleRankingType)
- [async def get\_article\_rank()](#async-def-get\_article\_rank)

---

## class Article()

专栏类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `cvid` | `int` | cv 号 |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |


### async def add_coins()

给专栏投币，目前只能投一个



**Returns:** `dict`:  调用 API 返回的结果




### async def fetch_content()

获取并解析专栏内容

该返回不会返回任何值，调用该方法后请再调用 `self.markdown()` 或 `self.json()` 来获取你需要的值。






### async def get_all()

一次性获取专栏尽可能详细数据，包括原始内容、标签、发布时间、标题、相关专栏推荐等



**Returns:** `dict`:  调用 API 返回的结果




### def get_cvid()

获取 cvid



**Returns:** `int`:  cvid




### async def get_detail()

获取专栏详细信息



**Returns:** `dict`:  调用 API 返回的结果




### async def get_info()

获取专栏信息



**Returns:** `dict`:  调用 API 返回的结果




### async def is_note()

判断专栏是否为笔记



**Returns:** `bool`:  是否为笔记




### def json()

转换为 JSON 数据

请先调用 fetch_content()



**Returns:** `dict`:  JSON 数据




### def markdown()

转换为 Markdown

请先调用 fetch_content()



**Returns:** `str`:  Markdown 内容




### async def set_favorite()

设置专栏收藏状态


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 收藏状态. Defaults to True |

**Returns:** `dict`:  调用 API 返回的结果




### async def set_like()

设置专栏点赞状态


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 点赞状态. Defaults to True |

**Returns:** `dict`:  调用 API 返回的结果




### async def turn_to_dynamic()

将专栏转为对应动态（评论、点赞等数据专栏/动态/图文共享）

专栏完全包含于动态，因此此函数绝对成功。

转换后可查看“赞和转发”列表。



**Returns:** `Dynamic`:  动态实例




### def turn_to_note()

将专栏转为笔记，不会核验。如需核验使用 `await is_note()`



**Returns:** `Note`:  笔记实例




### async def turn_to_opus()

将专栏转为对应图文（评论、点赞等数据专栏/动态/图文共享）

专栏完全包含于图文，因此此函数绝对成功。

转换后可查看“赞和转发”列表。



**Returns:** `Opus`:  动态实例




---

## class ArticleList()

文集类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `rlid` | `int` | 文集 id |
| `credential` | `Credential \| None, optional` | 凭据类. Defaults to None. |


### async def get_content()

获取专栏文集文章列表



**Returns:** `dict`:  调用 API 返回的结果




### def get_rlid()

获取 rlid



**Returns:** `int`:  rlid




---

## class ArticleRankingType()

**Extend: enum.Enum**

专栏排行榜类型枚举。

+ MONTH: 月榜
+ WEEK: 周榜
+ DAY_BEFORE_YESTERDAY: 前日榜
+ YESTERDAY: 昨日榜




---

## async def get_article_rank()

获取专栏排行榜


| name | type | description |
| - | - | - |
| `rank_type` | `ArticleRankingType` | 排行榜类别. Defaults to ArticleRankingType.YESTERDAY. |

**Returns:** `dict`:  调用 API 返回的结果




