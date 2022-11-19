# Module live_area.py

```python
from bilibili_api import live_area
```

直播分区相关操作

## def get_channel_info_by_tid()

| name | type | description |
| ---- | ---- | ----------- |
| id  | int  | 频道的 id  |

根据 id 获取频道信息。

**Returns:** `tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。

---

## def get_channel_info_by_name()

| name | type | description  |
| ---- | ---- | ------------ |
| name | str  | 频道的名称。 |

根据频道名称获取频道信息。

**Returns:** `tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。

---

## def get_channel_list()

获取所有分区的数据

**Returns:** dict: 所有分区的数据

---

## def get_channel_list_sub()

获取所有分区的数据

含父子关系（即一层次只有主分区）

**Returns:** dict: 所有分区的数据
