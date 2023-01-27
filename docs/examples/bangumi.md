# 示例：获取番剧剧集 BV 号

番剧剧集也是视频，只不过是特殊的视频，也有 BV 号。

若想下载，首先得获取到 BV 号。

```python
from bilibili_api import bangumi, sync


async def main():
    ep = bangumi.Episode(374717)
    # 打印 bv 号
    print(ep.get_bvid())

sync(main())
```

# 示例：获取番剧所有长评

```python
from bilibili_api import bangumi, sync

async def main():
    b = bangumi.Bangumi(28231846)
    next = None
    cmts = []
    while next != 0:
        cm = await b.get_long_comment_list(next=next)
        cmts.extend(cm['list'])
        next = cm['next']

    for cmt in cmts:
        print(cmt)

sync(main())
```

# 示例：获取番剧索引

```python
from bilibili_api import bangumi, sync
from bilibili_api.bangumi import Index_Filter as IF
async def main():
    filters = bangumi.Index_Filter_Meta.Anime(area=IF.Area.JAPAN,
        year=IF.make_time_filter(start=2019, end=2022, include_end=True),
        season=IF.Season.SPRING,
        style=IF.Style.Anime.NOVEL)
    index = await bangumi.get_index_info(filters=filters, order=IF.Order.SCORE, sort=IF.Sort.DESC, pn=2, ps=20)
    print(index)

sync(main())

```