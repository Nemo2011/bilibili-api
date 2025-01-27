# 示例：动态转发抽奖

```python
"""
请注意，获取转发数量有限制，上限大概在 540 个左右
若转发人数超过这个数字，将产生不公平，请勿使用该脚本
"""
from bilibili_api import dynamic, sync
import random

# 动态 ID
DYNAMIC_ID = 0

# 抽取人数
COUNT = 3

async def main():
    # 初始化
    dy = dynamic.Dynamic(DYNAMIC_ID)
    # 存储所有转发信息
    reposters = []
    # 存储下一页起始位置
    offset = "0"
    while True:
        # 循环拉取动态
        r = await dy.get_reposts(offset)
        # 存入
        reposters.extend(r['items'])
        print(f'拉取转发信息中 {len(reposters)} / {r["total"]}')

        if r['has_more'] != 1:
            # 无更多，退出循环
            break

        # 设置下一页起始位置
        offset = r['offset']

    # 中奖名单
    lucky_dogs = []

    for i in range(COUNT):
        # 随机取
        index = random.randint(0, len(reposters) - 1)
        lucky_dogs.append(reposters[index])

        # 取完后删除，以免重复
        reposters.remove(reposters[index])

    # 打印中奖名单
    print('中奖名单：')
    for p in lucky_dogs:
        print(f'{p["desc"]["user_profile"]["info"]["uname"]}  https://space.bilibili.com/{p["desc"]["user_profile"]["info"]["uid"]}')


sync(main())
```

# 示例：定时发送动态

``` python
from bilibili_api import dynamic, Credential, sync
import datetime

async def main():
    dy = (
        dynamic.BuildDynamic()
        .add_text("114514")
        .add_at(uid=1)          # uid 添加 @
        .add_at(uname="bishi")  # 昵称添加 @
        .add_emoji("[tv_doge]")
        .add_text("1919810")
        .set_send_time(datetime.datetime(2025, 2, 1, 0, 0, 0)) # 设置定时发送
    )
    await dynamic.send_dynamic(dy, credential=Credential(
        sessdata="",
        bili_jct=""
    ))

sync(main())

```
