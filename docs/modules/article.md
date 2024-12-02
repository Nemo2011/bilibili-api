# Module article.py


bilibili_api.article

专栏相关


``` python
from bilibili_api import article
```

---

## class Article()

专栏类


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| cvid | int | cv 号 |
| credential | Union[Credential, None] | 凭据. Defaults to None. |


### async def add_coins()

给专栏投币，目前只能投一个



**Returns:** dict: 调用 API 返回的结果




### async def fetch_content()

获取并解析专栏内容

该返回不会返回任何值，调用该方法后请再调用 `self.markdown()` 或 `self.json()` 来获取你需要的值。



**Returns:** None



### async def get_all()

一次性获取专栏尽可能详细数据，包括原始内容、标签、发布时间、标题、相关专栏推荐等



**Returns:** dict: 调用 API 返回的结果




### def get_cvid()

获取 cvid



**Returns:** int: cvid




### async def get_info()

获取专栏信息



**Returns:** dict: 调用 API 返回的结果




### def get_type()

获取专栏类型(专栏/笔记)



**Returns:** ArticleType: 专栏类型




### def is_note()

检查专栏是否笔记



**Returns:** bool: 是否笔记




### def json()

转换为 JSON 数据

请先调用 fetch_content()



**Returns:** dict: JSON 数据




### def markdown()

转换为 Markdown

请先调用 fetch_content()



**Returns:** str: Markdown 内容




### async def set_favorite()

设置专栏收藏状态


| name | type | description |
| - | - | - |
| status | Union[bool, None] | 收藏状态. Defaults to True |

**Returns:** dict: 调用 API 返回的结果




### async def set_like()

设置专栏点赞状态


| name | type | description |
| - | - | - |
| status | Union[bool, None] | 点赞状态. Defaults to True |

**Returns:** dict: 调用 API 返回的结果




### def turn_to_note()

对于完全与 opus 兼容的部分的特殊专栏，将 Article 对象转换为 Dynamic 对象。



**Returns:** Note: 笔记类




### def turn_to_opus()

对于 SPECIAL_ARTICLE，将其转为图文



**Returns:** None



---

## class ArticleList()

文集类


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| rlid | int | 文集 id |
| credential | Union[Credential, None] | 凭据类. Defaults to None. |


### async def get_content()

获取专栏文集文章列表



**Returns:** dict: 调用 API 返回的结果




### def get_rlid()

获取 rlid



**Returns:** int: rlid




---

## class ArticleRankingType()

**Extend: enum.Enum**

专栏排行榜类型枚举。

+ MONTH: 月榜
+ WEEK: 周榜
+ DAY_BEFORE_YESTERDAY: 前日榜
+ YESTERDAY: 昨日榜




---

## class ArticleType()

**Extend: enum.Enum**

专栏类型

- ARTICLE: 普通专栏，不与 opus 图文兼容。
- OPUS   : opus。
- SPECIAL_ARTICLE: 特殊专栏，与 opus 兼容。




---

## async def get_article_rank()

获取专栏排行榜


| name | type | description |
| - | - | - |
| rank_type | ArticleRankingType | 排行榜类别. Defaults to ArticleRankingType.YESTERDAY. |

**Returns:** dict: 调用 API 返回的结果




