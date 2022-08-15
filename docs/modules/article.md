# Module article.py

```python
from bilibili_api import article
```

专栏相关

## async def get_article_list()

| name       | type                 | description                                                  |
| ---------- | -------------------- | ------------------------------------------------------------ |
| rlid       | int                  | 文集 ID，如 https://www.bilibili.com/read/readlist/rl000010 省略前导 0 |
| credential | Credential, optional | 凭据. Defaults to None.                                      |

获取专栏文集文章列表

---

## class Article

专栏类

### Functions

#### def \_\_init\_\_()

| name       | type                 | description             |
| ---------- | -------------------- | ----------------------- |
| cvid       | int                  | 专栏 ID                 |
| credential | Credential, optional | 凭据. Defaults to None. |

#### def markdown()

转换为 Markdown

请先调用 get_content()

**Returns:** str: Markdown 内容

#### def json()

转换为 JSON 数据

请先调用 get_content()

**Returns:** dict: JSON 数据

#### async def fetch_content()

获取并解析专栏内容

该返回不会返回任何值，调用该方法后请再调用 `self.markdown()` 或 `self.json() `来获取你需要的值。

**Returns:** None

#### async def get_info()

获取专栏信息。

**Returns:** API 调用返回结果。

#### async def get_all()

一次性获取专栏尽可能详细数据，包括原始内容、标签、发布时间、标题、相关专栏推荐等		。

**Returns:** API 调用返回结果。

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

