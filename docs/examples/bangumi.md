# 示例：获取番剧剧集 BV 号

番剧剧集也是视频，只不过是特殊的视频，也有 BV 号。

若想下载，首先得获取到 BV 号。

```python
from bilibili_api import bangumi, sync


async def main():
    b = await bangumi.get_episode_info(374717)
    # 打印 bv 号
    print(b['epInfo']['bvid'])


sync(main())
```

# 示例：获取番剧所有长评

```python
from bilibili_api import bangumi, sync


async def main():
    next = None
    cmts = []
    while next != 0:
        b = await bangumi.get_long_comment_list(28231846, next=next)
        cmts.extend(b['list'])
        next = b['next']

    for cmt in cmts:
        print(cmt)


sync(main())
```

