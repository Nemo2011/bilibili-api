# Module rank.py

```python
from bilibili_api import rank
```

## async def get_hot_videos()

获取热门视频

| name | type | description          |
|------| ---- |----------------------|
| ps   | int | 每页视频数. Default to 20 |
| pn   | int | 页码. Default to 1     |

**Returns:** dict: 调用 API 返回的结果

## async def get_weakly_hot_videos_list()

获取每周必看列表(仅概述)

**Returns:** dict: 调用 API 返回的结果

## async def get_weakly_hot_videos()

获取一周的每周必看视频列表

| name | type | description |
| ---- | ---- | ----------- |
| week | int | 第几周. Default to 1 |

**Returns:** dict: 调用 API 返回的结果

## async def get_history_popular_videos()

获取入站必刷 85 个视频

**Returns:** dict: 调用 API 返回的结果

## async def get_rank()

获取视频排行榜

**Returns:** dict: 调用 API 返回的结果

## async def get_music_rank_list()

获取全站音乐榜每周信息(不包括具体的音频列表)

**Returns:** dict: 调用 API 返回的结果

## async def get_music_rank_weakly_detail()

| name | type | description |
| - | - | - |
| week | int | 第几周 |

获取全站音乐榜一周的详细信息(不包括具体的音频列表)

**Returns:** dict: 调用 API 返回的结果

## async def get_music_rank_weakly_musics()

| name | type | description |
| - | - | - |
| week | int | 第几周 |

获取全站音乐榜一周的音频列表

**Returns:** dict: 调用 API 返回的结果
