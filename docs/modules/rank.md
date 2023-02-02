# Module rank.py

```python
from bilibili_api import rank
```

## class RankAPIType

**Extends:enum.Enum**

排行榜 API 接口类型

- PGC: https://api.bilibili.com/pgc/web/rank/list
- V2: https://api.bilibili.com/x/web-interface/ranking/v2

## class RankDayType

**Extends:enum.Enum**

排行榜时间类型

- THREE_DAY: 三日排行
- WEEK: 周排行

## class RankType

排行榜类型

- All: 全部
- Bangumi: 番剧
- GuochuanAnime: 国产动画
- Guochuang: 国创相关
- Documentary: 纪录片
- Douga: 动画
- Music: 音乐
- Dance: 舞蹈
- Game: 游戏
- Knowledge: 知识
- Technology: 科技
- Sports: 运动
- Car: 汽车
- Life: 生活
- Food: 美食
- Animal: 动物圈
- Kitchen: 鬼畜
- Fashion: 时尚
- Ent: 娱乐
- Cinephile: 影视
- Movie: 电影
- TV: 电视剧
- Variety: 综艺
- Original: 原创
- Rookie: 新人

## class VIPRankType

大会员中心热播榜单类型，即 rank_id

- VIP: 会员
- BANGUMI: 番剧
- GUOCHUANG: 国创
- MOVIE: 电影
- DOCUMENTARY: 纪录片
- TV: 电视剧
- VARIETY: 综艺

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
| day | RankDayType | 时间类型. Defaults to RankDayType.THREE_DAY |

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

## async def get_vip_rank()

| name | type | description |
| - | - | - |
| type_ | RankType | 排行榜类型. Defaults to RankType.VIP |

获取大会员中心的排行榜

**Returns:** dict: 调用 API 返回的结果