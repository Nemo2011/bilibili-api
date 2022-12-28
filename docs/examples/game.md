# 示例：获取游戏详情

``` python
from bilibili_api import game, sync

g = game.Game(105667)
print(sync(g.get_detail()))
```
