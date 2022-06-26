# Module channel.py

```python
from bilibili_api import channel
```

频道相关操作

## def get_channel_info_by_id()

| name | type | description |
| ---- | ---- | ----------- |
| tid  | int  | 频道的 tid  |

根据 tid 获取频道信息。

**Returns:** `tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。

---

## def get_channel_info_by_name()

| name | type | description  |
| ---- | ---- | ------------ |
| name | str  | 频道的名称。 |

根据频道名称获取频道信息。

**Returns:** `tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。

---

## _async_ def get_top10()

| name       | type                 | description                            |
| ---------- | -------------------- | -------------------------------------- |
| tid        | int                  | 频道的 tid                             |
| day        | int, optional        | 3 天排行还是 7 天排行。 Defaults to 7. |
| credential | Credential, optional | Credential 类。Defaults to None.       |

获取分区前十排行榜。

**Returns:** `tuple[dict | None, dict | None]`: 第一个是主分区，第二个是子分区，没有时返回 None。

---

