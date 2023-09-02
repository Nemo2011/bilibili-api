# Module game.py

``` python
from bilibili_api import game
```

## class Game

游戏类

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类 |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| game_id | int | 游戏 id |
| credential | Credential \| None | 凭据类. Defaults to None.  ｜

#### def get_game_id()

获取游戏 id

**Returns:** 游戏 id

#### async def get_info()

获取游戏简介

**Returns:** dict: 调用 API 返回的结果

#### async def get_up_info()

获取游戏官方账号

**Returns:** dict: 调用 API 返回的结果

#### async def get_detail()

获取游戏详情

**Returns:** dict: 调用 API 返回的结果

#### async def get_wiki()

获取游戏教程(wiki)

**Returns:** dict: 调用 API 返回的结果

#### async def get_videos()

获取游戏介绍视频

**Returns:** dict: 调用 API 返回的结果

#### async def get_score()

获取游戏评分

**Returns:** dict: 调用 API 返回的结果

<!-- #### async def get_comments()

获取游戏的评论

**Returns:** dict: 调用 API 返回的结果 -->

---

## class GameRankType

**Extends: enum.Enum**

游戏排行榜类型枚举

- HOT: 热度榜
- SUBSCRIBE: 预约榜
- NEW: 新游榜
- REPUTATION: 口碑榜
- BILIBILI: B指榜
- CLIENT: 端游榜

---

## async def get_game_rank

| name | type | description |
| ---- | ---- | ----------- |
| rank_type | GameRankType | 游戏排行榜类型 |
| page_num | int, optional | 页码. Defaults to 1. |
| page_size | int, optional | 每页游戏数量. Defaults to 20. |

**Returns:** dict: 调用 API 返回的结果

---

## async def get_start_test_list

| name | type | description |
| ---- | ---- | ----------- |
| page_num | int, optional | 页码. Defaults to 1. |
| page_size | int, optional | 每页游戏数量. Defaults to 20. |

**Returns:** dict: 调用 API 返回的结果

---

## async def game_name2id

| name | type | description |
| ---- | ---- | ----------- |
| game_name | str | 游戏名 |

将游戏名转换为游戏的编码

**Returns:** str: 游戏编码

---

## def get_wiki_api_root

| name | type | description |
| ---- | ---- | ----------- |
| game_id | str | 游戏编码 |

获取游戏 WIKI 对应的 api 链接，以便传入第三方库进行其他解析操作。

**Returns:** str: 游戏 WIKI 对应的 api 链接
