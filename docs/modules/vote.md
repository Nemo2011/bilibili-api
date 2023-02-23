# Module vote.py

```python
from bilibili_api import vote
```

vote_id，投票 ID，可通过 [vote_id](https://nemo2011.github.io/bilibili-api/#/vote_id) 获取

## class VoteType

**Extends:** enum.Enum

投票类型枚举类

+ TEXT: 文字投票
+ IMAGE: 图片投票

## class VoteChoices

投票选项类

### def add_choice()

| name | type | description |
| - | - | - |
| desc | str | 选项描述 |
| image | str, Picture | 选项图片链接或图片类，用于图片投票 |

添加选项

### def remove_choice()

| name | type | description |
| - | - | - |
| index | int | 选项索引 |

删除选项

### def get_choices()

获取选项列表

**Returns:** dict: 选项信息

## class Vote

投票类

### \_\_init\_\_()

| name | type | description |
| - | - | - |
| vote_id | int | 投票 ID |
| credential | Credential | Credential 类，非必要 |

### async def get_info()

获取投票详情

**Returns:** dict: 调用 API 返回的结果

### async def update_vote()

| name | type | description |
| - | - | - |
| title | str | 投票标题 |
| desc | str, optional | 投票描述 |
| duration | int | 投票持续时秒数 |
| choice_cnt | int | 最多选几项 |
| _type | VoteType | 投票类型 |
| choices | VoteChoices | 投票选项 |
| credential | Credential | Credential 枚举类 |
| vote_id | int | 投票 ID |

更新投票内容

**Returns:** dict: 调用 API 返回的结果


## async def create_vote()

| name | type | description |
| - | - | - |
| title | str | 投票标题 |
| desc | str, optional | 投票描述 |
| duration | int | 投票持续时秒数 |
| choice_cnt | int | 最多选几项 |
| _type | VoteType | 投票类型 |
| choices | VoteChoices | 投票选项 |
| credential | Credential | Credential 枚举类 |

创建投票

**Returns:** Vote: 投票类