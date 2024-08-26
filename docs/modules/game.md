# Module game.py


bilibili_api.game

游戏相关


``` python
from bilibili_api import game
```

## class Game

**Extend: builtins.object**

游戏类


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |


### async def get_detail()

获取游戏详情



**Returns:** dict: 调用 API 返回的结果




### def get_game_id()

获取游戏 id



**Returns:** int: 游戏 id




### async def get_info()

获取游戏简介



**Returns:** dict: 调用 API 返回的结果




### async def get_up_info()

获取游戏官方账号



**Returns:** dict: 调用 API 返回的结果




### async def get_videos()

获取游戏介绍视频



**Returns:** dict: 调用 API 返回的结果




### async def get_wiki()

获取游戏教程(wiki)



**Returns:** dict: 调用 API 返回的结果




## class GameRankType

**Extend: enum.Enum**

游戏排行榜类型枚举

- HOT: 热度榜
- SUBSCRIBE: 预约榜
- NEW: 新游榜
- REPUTATION: 口碑榜
- BILIBILI: B指榜
- CLIENT: 端游榜




## async def game_name2id()

将游戏名转换为游戏的编码


| name | type | description |
| - | - | - |
| game_name | str | 游戏名 |

**Returns:** str: 游戏编码




## async def get_game_rank()

获取游戏排行榜


| name | type | description |
| - | - | - |
| rank_type | GameRankType | 游戏排行榜类型 |
| page_num | Union[int, None] | 页码. Defaults to 1. |
| page_size | Union[int, None] | 每页游戏数量. Defaults to 20. |

**Returns:** dict: 调用 API 返回的结果




## async def get_start_test_list()

获取游戏公测时间线


| name | type | description |
| - | - | - |
| page_num | Union[int, None] | 页码. Defaults to 1. |
| page_size | Union[int, None] | 每页游戏数量. Defaults to 20. |

**Returns:** dict: 调用 API 返回的结果




## def get_wiki_api_root()

获取游戏 WIKI 对应的 api 链接，以便传入第三方库进行其他解析操作。


| name | type | description |
| - | - | - |
| game_id | str | 游戏编码 |

**Returns:** str: 游戏 WIKI 对应的 api 链接




