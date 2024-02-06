# Module article.py

```python
from bilibili_api import article
```

专栏相关

---

## const dict ARTICLE_COLOR_MAP

专栏颜色表

---

## class ArticleRankingType

**Extends:** enum.Enum

专栏排行榜类型枚举。

+ MONTH: 月榜
+ WEEK: 周榜
+ DAY_BEFORE_YESTERDAY: 前日榜
+ YESTERDAY: 昨日榜

---

## async def get_article_rank()

| name | type | description |
| ---- | ---- | ----------- |
| rank_type | ArticleRankingType | 排行榜类别. Defaults to ArticleRankingType.YESTERDAY. |

获取专栏排行榜

**Returns:** dict: 调用 API 返回的结果

---

## class ArticleType

**Extends:** enum.Enum

- ARTICLE        : 普通专栏，不与 opus 图文兼容。
- NOTE           : 笔记专栏
- SPECIAL_ARTICLE: 特殊专栏，采用笔记格式，且与 opus 图文完全兼容。

## class ArticleList

### Atrributes

| name | type | description |
| - | - | - |
| credential | Credential \| None | 凭据类 |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| rlid       | int                  | 文集 ID，如 https://www.bilibili.com/read/readlist/rl000010 省略前导 0 |
| credential | Credential \| None, optional | 凭据. Defaults to None.                                      |

#### def get_rlid()

获取 rlid

**Returns:** rlid

#### async def get_content()

获取专栏文集文章列表

**Returns:** dict: 调用 API 返回的结果

---

## class Article

专栏类

### Atrributes

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |

### Functions

#### def \_\_init\_\_()

| name       | type                 | description             |
| ---------- | -------------------- | ----------------------- |
| cvid       | int                  | 专栏 ID                 |
| credential | Credential \| None, optional | 凭据. Defaults to None. |

#### def get_rlid()

获取 rlid

**Returns:** rlid

#### def is_note()

专栏是否公开笔记

**Returns:** bool: 是否公开笔记

#### def turn_to_note()

将专栏转换为笔记类（公开笔记）。需要保证专栏是公开笔记。

**Returns:** Note: 笔记类

#### def markdown()

转换为 Markdown

请先调用 fetch_content()

**Returns:** str: Markdown 内容

#### def json()

转换为 JSON 数据

请先调用 fetch_content()

**Returns:** dict: JSON 数据

#### async def to_note()

转换为 Note 类

请确保是此专栏是笔记

**Returns:** Note: Note 类

#### async def fetch_content()

加载专栏内容。该方法不会返回任何值，调用该方法后请再调用 `self.markdown()` 或 `self.json() `来获取你需要的值。

**Returns:** None

#### async def get_info()

获取专栏信息。

**Returns:** API 调用返回结果。

#### async def get_all()

一次性获取专栏尽可能详细数据，包括原始内容、标签、发布时间、标题、相关专栏推荐等		。

**Returns:** API 调用返回结果。

#### def get_type()

获取专栏类型。

**Returns:** ArticleType: 专栏类型

#### async def set_like()

| name   | type           | description                |
| ------ | -------------- | -------------------------- |
| status | bool, optional | 点赞状态. Defaults to True |

设置专栏点赞状态

**Returns:** API 调用返回结果。

#### async def set_favorite()

| name   | type           | description                |
| ------ | -------------- | -------------------------- |
| status | bool, optional | 收藏状态. Defaults to True |

设置专栏收藏状态

**Returns:** API 调用返回结果。

#### async def add_coins()

给专栏投币，目前只能投一个

**Returns:** API 调用返回结果。
