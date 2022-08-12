# Module channel.ts(channel.js)

```typescript
import {} from "bilibili-api-ts/channel";
```

频道相关操作

## def get_channel_info_by_tid()

| name | type | description |
| ---- | ---- | ----------- |
| tid  | int  | 频道的 tid  |

根据 tid 获取频道信息。

**Returns:** `Object[Object, Object]`: 第一个是主分区，第二个是子分区，没有时返回 None。

---

## def get_channel_info_by_name()

| name | type | description  |
| ---- | ---- | ------------ |
| name | str  | 频道的名称。 |

根据频道名称获取频道信息。

**Returns:** `Object[Object, Object]`: 第一个是主分区，第二个是子分区，没有时返回 None。

---

## async def get_top10()

| name       | type                 | description                            |
| ---------- | -------------------- | -------------------------------------- |
| tid        | int                  | 频道的 tid                             |
| day        | int, optional        | 3 天排行还是 7 天排行。 Defaults to 7. |
| credential | Credential, optional | Credential 类。Defaults to None.       |

获取分区前十排行榜。

**Returns:** `Object`: 调用 API 返回的结果

---

