# Module vote.py


bilibili_api.vote

投票相关操作。

需要 vote_id,获取 vote_id: https://nemo2011.github.io/bilibili-api/#/vote_id


``` python
from bilibili_api import vote
```

---

## class Vote()

投票类


| name | type | description |
| - | - | - |
| vote_id | int | vote_id, 获取：https |
| credential | Credential | 凭据类 |


### async def get_info()

获取投票详情



**Returns:** dict: 调用 API 返回的结果




### def get_info_sync()

获取投票详情



**Returns:** dict: 调用 API 返回的结果




### async def get_title()

快速获取投票标题



**Returns:** str: 投票标题




### def get_vote_id()

获取投票 id



**Returns:** int: 投票 id




### async def update_vote()

更新投票内容


| name | type | description |
| - | - | - |
| vote_id | int | vote_id |
| title | str | 投票标题 |
| _type | VoteType | 投票类型 |
| choice_cnt | int | 最多几项 |
| duration | int | 投票持续秒数 常用 |
| choices | VoteChoices | 投票选项 |
| credential | Credential | Credential 枚举类 |
| desc | Union[optional, None] | 投票描述. Defaults to None. |

**Returns:** dict: 调用 API 返回的结果




---

## class VoteChoices()

投票选项类




### def add_choice()

往 VoteChoices 添加选项


| name | type | description |
| - | - | - |
| desc | str | 选项描述 |
| image | Union[str, None] | 选项的图片链接，用于图片投票。支持 Picture 类. Defaults to None. |

**Returns:** None



### def get_choices()

获取 VoteChoices 的 choices



**Returns:** dict: choices




### def remove_choice()

从 VoteChoices 移除选项


| name | type | description |
| - | - | - |
| index | int | 选项索引 |

**Returns:** None



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
| title | str | 投票标题 |
| _type | VoteType | 投票类型 |
| choice_cnt | int | 最多几项 |
| duration | int | 投票持续秒数 常用 |
| choices | VoteChoices | 投票选项 |
| credential | Credential | Credential |
| desc | Union[optional, None] | 投票描述. Defaults to None. |

**Returns:** Vote: Vote 类




