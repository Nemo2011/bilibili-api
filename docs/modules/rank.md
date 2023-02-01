# Module rank.py

```python
from bilibili_api import rank
```

## class RankType

排行榜类型

- ALL: 全部
- BANGUMI: 番剧
- GUOCHUAN_ANIME: 国产动画
- GUOCHUANG: 国创番剧
- DOCUMENTARY: 纪录片
- DOUGA: 动画
- MUSIC: 音乐
- DANCE: 舞蹈
- GAME: 游戏
- KNOWLEDGE: 知识
- TECHNOLOGY: 科技
- SPORTS: 运动
- CAR: 汽车
- LIVE: 直播
- FOOD: 美食
- ANIMAL: 动物圈
- KICHIKU: 鬼畜
- FASHION: 时尚
- ENT: 娱乐
- CINEPHILE: 影视
- MOVIE: 电影
- TV: 电视剧
- VARIETY: 综艺
- ORIGINAL: 原创
- ROOKIE: 新人

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

| name | type | description |
| ---- | ---- | ----------- |
| type_ | RankType | 排行榜类型. Defaults to RankType.ALL |

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
