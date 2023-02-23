# 示例：获取投票信息

``` python
from bilibili_api import vote, sync

print(sync(vote.Vote(2773489).get_vote_info()))
```
