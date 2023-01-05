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
