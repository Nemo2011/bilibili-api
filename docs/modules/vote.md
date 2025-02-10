# Module vote.py


bilibili_api.vote

投票相关操作。

需要 vote_id,获取 vote_id: https://nemo2011.github.io/bilibili-api/#/vote_id


``` python
from bilibili_api import vote
```

- [class Vote()](#class-Vote)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_info()](#async-def-get\_info)
  - [async def get\_title()](#async-def-get\_title)
  - [def get\_vote\_id()](#def-get\_vote\_id)
  - [async def update\_vote()](#async-def-update\_vote)
- [class VoteChoices()](#class-VoteChoices)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def add\_choice()](#def-add\_choice)
  - [def get\_choices()](#def-get\_choices)
  - [def remove\_choice()](#def-remove\_choice)
- [class VoteType()](#class-VoteType)
- [async def create\_vote()](#async-def-create\_vote)

---

## class Vote()

投票类


| name | type | description |
| - | - | - |
| `vote_id` | `int` | vote_id, 获取：https |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `vote_id` | `int` | vote_id, 获取：https |
| `credential` | `Credential` | 凭据类，非必要. |


### async def get_info()

获取投票详情



**Returns:** `dict`:  调用 API 返回的结果




### async def get_title()

快速获取投票标题



**Returns:** `str`:  投票标题




### def get_vote_id()

获取投票 id



**Returns:** `int`:  投票 id




### async def update_vote()

更新投票内容


| name | type | description |
| - | - | - |
| `vote_id` | `int` | vote_id |
| `title` | `str` | 投票标题 |
| `_type` | `VoteType` | 投票类型 |
| `choice_cnt` | `int` | 最多几项 |
| `duration` | `int` | 投票持续秒数 常用 |
| `choices` | `VoteChoices` | 投票选项 |
| `credential` | `Credential` | Credential 枚举类 |
| `desc` | `Optional[str], optional` | 投票描述. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## class VoteChoices()

投票选项类




### def \_\_init\_\_()





### def add_choice()

往 VoteChoices 添加选项


| name | type | description |
| - | - | - |
| `desc` | `str` | 选项描述 |
| `image` | `str, Picture, optional` | 选项的图片链接，用于图片投票。支持 Picture 类. Defaults to None. |




### def get_choices()

获取 VoteChoices 的 choices



**Returns:** `dict`:  choices




### def remove_choice()

从 VoteChoices 移除选项


| name | type | description |
| - | - | - |
| `index` | `int` | 选项索引 |




---

## class VoteType()

**Extend: enum.Enum**

投票类型枚举类

+ TEXT: 文字投票
+ IMAGE: 图片投票




---

## async def create_vote()

创建投票


| name | type | description |
| - | - | - |
| `title` | `str` | 投票标题 |
| `_type` | `VoteType` | 投票类型 |
| `choice_cnt` | `int` | 最多几项 |
| `duration` | `int` | 投票持续秒数 常用 |
| `choices` | `VoteChoices` | 投票选项 |
| `credential` | `Credential` | Credential |
| `desc` | `Optional[str], optional` | 投票描述. Defaults to None. |

**Returns:** `Vote`:  Vote 类




