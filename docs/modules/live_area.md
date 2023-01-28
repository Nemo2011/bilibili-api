# Module live_area.py

```python
from bilibili_api import live_area
```

直播分区相关操作

## def get_area_info_by_tid()

| name | type | description |
| ---- | ---- | ----------- |
| id  | int  | 频道的 id  |

根据 id 获取频道信息。

**Returns:** `Tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。

---

## def get_area_info_by_name()

| name | type | description  |
| ---- | ---- | ------------ |
| name | str  | 频道的名称。 |

根据频道名称获取频道信息。

**Returns:** `Tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。

---

## def get_area_list()

获取所有分区的数据

**Returns:** List[dict]: 所有分区的数据

---

## def get_area_list_sub()

获取所有分区的数据

含父子关系（即一层次只有主分区）

**Returns:** dict: 所有分区的数据

---

## class LiveRoomOrder()

**Extends: enum.Enum**

直播间排序方式

- RECOMMEND: 综合
- NEW: 最新

---

## async def get_list_by_area()

| name | type | description |
| ---- | ---- | ----------- |
| area_id | int | 分区 id |
| page | int | 第几页. Defaults to 1. |
| order | LiveRoomOrder | 直播间排序方式. Defaults to LiveRoomOrder.RECOMMEND. |

根据分区获取直播间列表

**Returns:** dict: 调用 API 返回的结果
