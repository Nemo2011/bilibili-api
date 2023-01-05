# Module topic.md

``` python
from bilibili_api import topic
```

## class Topic

### Attributes

| name | type | description |
| - | - | - |
| credential | Credential \| None | 凭据类 |

### Methods

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| topic_id | int | 话题 id |
| credential | Credential | 凭据类 |

#### def get_topic_id()

获取话题 id

**Returns:** int: 话题 id

#### async def get_info()

获取话题简介

**Returns:** dict: 调用 API 返回的结果

#### async def get_cards()

| name | type | description |
| - | - | - |
| size | int | 数据数量. Defaults to 100. |

获取话题下的内容

**Returns:** dict: 调用 API 返回的结果
