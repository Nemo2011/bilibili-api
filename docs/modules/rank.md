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

## class MangaRankType

**Extends:enum.Enum**

漫画排行榜类型

- NEW: 新作
- BOY: 男生
- GRIL: 女生
- GUOCHUANG: 国漫
- JAPAN: 日漫
- SOUTHKOREA: 韩漫
- OFFICAL: 宝藏
- FREE: 免费
- FINISH: 完结

## class LiveRankType

**Extends:enum.Enum**

直播通用榜类型

- SAIL_BOAT_VALUE: 主播舰队榜
- SAIL_BOAT_TICKET: 船员价值榜
- SAIL_BOAT_NUMBER: 舰船人数榜
- MASTER_LEVEL: 主播等级榜
- USER_LEVEL: 用户等级榜

## class LiveEnergyRankType

**Extends:enum.Enum**

直播超能用户榜类型

- MONTH: 本月
- PRE_MONTH: 上月

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

## async def get_music_rank_weekly_detail()

| name | type | description |
| - | - | - |
| week | int | 第几周 |

获取全站音乐榜一周的详细信息(不包括具体的音频列表)

**Returns:** dict: 调用 API 返回的结果

## async def get_music_rank_weekly_musics()

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

## async def get_manga_rank()

| name | type | description |
| - | - | - |
| type_ | MangaRankType | 漫画排行榜类型. Defaults to MangaRankType.NEW |

获取漫画专属排行榜

**Returns:** dict: 调用 API 返回的结果

## async def get_live_hot_rank()

获取直播首页人气排行榜

**Returns:** dict: 调用 API 返回的结果

## async def get_live_sailing_rank()

获取首页直播大航海排行榜

**Returns:** dict: 调用 API 返回的结果

## async def get_live_energy_user_rank()

| name | type | description |
| - | - | - |
| date | LiveEnergyRankType | 直播超能用户榜月份类型. Defaults to LiveEnergyRankType.MONTH |
| pn | int | 页数. Defaults to 1 |
| ps | int | 每页数量. Defaults to 20 |

获取直播超能用户榜

**Returns:** dict: 调用 API 返回的结果

## async def get_live_rank()

| name | type | description |
| - | - | - |
| type_ | LiveRankType | 直播通用榜类型. Defaults to LiveRankType.SAIL_BOAT_VALUE |
| pn | int | 页数. Defaults to 1 |
| ps | int | 每页数量. Defaults to 20 |

获取直播通用榜单

**Returns:** dict: 调用 API 返回的结果

## async def get_live_user_medal_rank()

| name | type | description |
| - | - | - |
| pn | int | 页数. Defaults to 1 |
| ps | int | 每页数量. Defaults to 20 |

获取直播用户勋章榜

**Returns:** dict: 调用 API 返回的结果

## async def subscribe_music_rank()

| name | type | description |
| ---- | ---- | ----------- |
| status | bool | 是否订阅的状态. Defaults to True. |
| credential | Credential | 凭据类 |

设置关注全站音乐榜

**Returns:** dict: 调用 API 返回的结果


## async def get_playlet_rank_phases

获取全站短剧榜期数

**Returns:** dict: 调用 API 返回的结果

## async def get_playlet_rank_info

| name | type | description |
| ---- | ---- | ----------- |
| phase_id | int | 期数，从 get_playlet_rank_phase 获取 |

获取全站短剧榜

https://www.bilibili.com/v/popular/drama/

**Returns:** dict: 调用 API 返回的结果