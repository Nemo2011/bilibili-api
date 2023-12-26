# Module hot.py

```python
from bilibili_api import hot
```

热门相关 API

## async def get_hot_videos()

获取热门视频

| name | type | description          |
|------| ---- |----------------------|
| ps   | int | 每页视频数. Default to 20 |
| pn   | int | 页码. Default to 1     |

**Returns:** dict: 调用 API 返回的结果

## async def get_weekly_hot_videos_list()

获取每周必看列表(仅概述)

**Returns:** dict: 调用 API 返回的结果

## async def get_weekly_hot_videos()

获取一周的每周必看视频列表

| name | type | description |
| ---- | ---- | ----------- |
| week | int | 第几周. Default to 1 |

**Returns:** dict: 调用 API 返回的结果

## async def get_history_popular_videos()

获取入站必刷 85 个视频

**Returns:** dict: 调用 API 返回的结果

## async def get_hot_buzzwords()

| name      | type | description              |
|-----------|------|--------------------------|
| page_num  | int  | 页码. Defaults to 1.       |
| page_size | int  | 每一页的数据量. Defaults to 20. |

获取热词图鉴信息
