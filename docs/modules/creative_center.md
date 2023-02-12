# Module creative_center.py

```python
from bilibili_api import creative_center
```

创作中心相关。

## class GraphPeriod

**Extends:** enum.Enum

统计图表时间段枚举。

+ YESTERDAY: 昨天
+ WEEK: 近一周
+ MONTH: 近一月
+ THREE_MONTH: 近三月
+ TOTAL: 历史累计

---

## class GraphType

**Extends:** enum.Enum

统计图表的类型。

+ PLAY: 播放量
+ VISITOR: 访问量
+ FAN: 粉丝数
+ LIKE: 点赞数
+ FAV: 收藏数
+ SHARE: 分享数
+ COMMENT: 评论数
+ DAMKU: 弹幕数
+ COIN: 投币数
+ ELEC: 充电数

---

## class FanGraphPeriod

**Extends:** enum.Enum

粉丝统计图表的时间段。

+ YESTERDAY: 昨天
+ WEEK: 近一周
+ MONTH: 近一月
+ THREE_MONTH: 近三月

---

## class FanGraphType

**Extends:** enum.Enum

粉丝统计图表的类型。

+ ALL_FANS: 粉丝总量
+ FAN: 新增粉丝
+ FOLLOW: 新增关注
+ UNFOLLOW: 取消关注

---

## class Copyright

**Extends:** enum.Enum

稿件播放完成率对比的版权类型。

+ ALL: 全部
+ ORIGINAL: 原创
+ REPRINT: 转载

---

## async def get_compare()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

获取对比数据。

**Returns:** 调用接口返回的内容。

## async def get_graph()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| period | GraphPeriod | 统计图表的时间段 |
| graph_type | GraphType | 统计图表的类型 |

获取统计图表。

**Returns:** 调用接口返回的内容。

## async def get_overview()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| period | GraphPeriod | 统计图表的时间段 |

获取概览数据。

**Returns:** 调用接口返回的内容。

## async def get_video_survey()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

获取视频各分区中占比排行。

**Returns:** 调用接口返回的内容。

## async def get_video_playanalysis()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| copyright | Copyright | 稿件播放完成率对比的版权类型 |

获取视频播放完成率对比。

**Returns:** 调用接口返回的内容。

## async def get_video_source()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

获取视频播放来源分布。

**Returns:** 调用接口返回的内容。

## async def get_fan_overview()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| period | FanGraphPeriod | 粉丝统计图表的时间段 |

获取粉丝概览数据。

**Returns:** 调用接口返回的内容。

## async def get_fan_graph()

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |
| period | FanGraphPeriod | 粉丝统计图表的时间段 |
| graph_type | FanGraphType | 粉丝统计图表的类型 |

获取粉丝统计图表。

**Returns:** 调用接口返回的内容。