# Module dynamic.py

```python
from bilibili_api import dynamic
```

动态相关

## async def upload_image()

| name         | type              | description |
| ------------ | ----------------- | ----------- |
| image        | Picture           | 图片流      |
| credential   | Credential        | 凭据        |

上传动态图片

**Returns:** dict: 调用 API 返回的结果

---

## async def send_dynamic()

| name         | type                              | description                         |
| ------------ | --------------------------------- | ----------------------------------- |
| text         | str                               | 动态文本                            |
| images       | List[Picture] \| None, optional | 图片流列表. Defaults to None.       |
| send_time    | datetime.datetime \| None, optional       | 定时动态发送时间. Defaults to None. |
| credential   | Credential \| None, optional              | 凭据. Defaults to None.             |

自动判断动态类型选择合适的 API 并发送动态。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_schedules_list()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| credential | Credential | 凭据        |

获取待发送定时动态列表

**Returns:** dict: 调用 API 返回的结果

---

## async def send_schedule_now()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| draft_id   | int        | 定时动态 ID |
| credential | Credential | 凭据        |

立即发送定时动态

**Returns:** dict: 调用 API 返回的结果

---

## async def delete_schedule()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| draft_id   | int        | 定时动态 ID |
| credential | Credential | 凭据        |

删除定时动态

**Returns:** dict: 调用 API 返回的结果

---

## class Dynamic

动态类

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

### Functions

#### def \_\_init\_\_()

| name       | type       | description |
| ---------- | ---------- | ----------- |
| dynamic_id | int        | 动态 ID     |
| credential | Credential \| None | 凭据        |

#### def get_dynamic_id()

获取 dynamic_id

#### async def get_info()

获取动态信息

**Returns:** dict: 调用 API 返回的结果

#### async def get_reposts()

| name   | type          | description                                                  |
| ------ | ------------- | ------------------------------------------------------------ |
| offset | str, optional | 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to "0" |

获取动态转发列表

**Returns:** dict: 调用 API 返回的结果

#### async def get_like()

| name   | type           | description                 |
| ------ | -------------- | --------------------------- |
| pn | int | 页码. Defaults to 1. |
| ps | int | 每页大小. Defaults to 30. |

获取动态点赞列表

**Returns:** dict: 调用 API 返回的结果

#### async def set_like()

| name   | type           | description                 |
| ------ | -------------- | --------------------------- |
| status | bool, optional | 点赞状态. Defaults to True. |

设置动态点赞状态

**Returns:** dict: 调用 API 返回的结果

#### async def delete()

删除动态

**Returns:** dict: 调用 API 返回的结果

#### async def repost()

| name | type          | description                                  |
| ---- | ------------- | -------------------------------------------- |
| text | str \| None, optional | 转发动态时的文本内容. Defaults to "转发动态" |

转发动态

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_new_dynamic_users()

| name | type | description |
| - | - | - |
| credential | Credential \| None | 凭据类. Defaults to None. |

获取更新动态的关注者

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_live_users()

| name | type | description |
| - | - | - |
| size | int | 获取的数据数量. Defaults to 10.  |
| credential | Credential \| None | 凭据类. Defaults to None. |

获取正在直播的关注者

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_dynamic_page_info()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类. |

获取自己的动态页的信息

**Returns:** dict: 调用 API 返回的结果
