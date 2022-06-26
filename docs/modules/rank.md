# Module rank.py

```python
from bilibili_api import rank
```

## _async_ def get_hot_videos()

获取热门视频

**Returns:**:调用 API 返回的结果

## _async_ def get_weakly_hot_videos_list()

获取每周必看列表(仅概述)

**Returns:**:调用 API 返回的结果

## _async_ def get_weakly_hot_videos()

获取一周的每周必看视频列表

| name | type | description |
| ---- | ---- | ----------- |
| week | int | 第几周，default to 1 |

**Returns:**:调用 API 返回的结果

## _async_ def get_history_popular_videos()

获取入站必刷 85 个视频

**Returns:**:调用 API 返回的结果

## _async_ def get_rank()

获取视频排行榜

**Returns:**:调用 API 返回的结果
