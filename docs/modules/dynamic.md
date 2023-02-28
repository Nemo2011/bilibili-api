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

## class BuildDynmaic

构建动态内容

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| contents | List | 动态内容字段 |
| pics | List | 图片字段 |
| attach_card | dict | 动态卡片字段 |
| topic | dict | 话题字段 |
| options | dict | 选项字段 |

### Functions

#### def add_text()

| name | type | description |
| ---- | ---- | ----------- |
| text | str | 文本内容 |

添加文本内容（可以附加 at 人和表情包）

#### def add_plain_text()

| name | type | description |
| ---- | ---- | ----------- |
| text | str | 文本内容 |

添加纯内容

#### def add_at()

| name | type | description |
| ---- | ---- | ----------- |
| user | int, User | 用户 ID 或用户类 |

添加 @ 用户

#### def add_emoji()

| name | type | description |
| ---- | ---- | ----------- |
| emoji_name | str | 表情中文名称 |

添加表情

#### def add_vote()

| name | type | description |
| ---- | ---- | ----------- |
| vote | Vote, int | 投票类或 vote_id |

添加投票
#### def add_image()

| name | type | description |
| ---- | ---- | ----------- |
| image | Picture | 图片类 |

添加图片

#### def set_attach_card()

| name | type | description |
| ---- | ---- | ----------- |
| oid | int | 卡片id |

设置直播预约

在 live.create_live_reserve 中获取 oid

#### def set_topic()

| name | type | description |
| ---- | ---- | ----------- |
| topic_id | int, Topic | 话题id 或话题类 |

设置话题

#### def set_options()

| name | type | description |
| ---- | ---- | ----------- |
| up_choose_comment | bool | 开启精选评论 |
| close_comment | bool | 关闭评论 |

设置选项

---

## async def send_dynamic()

| name         | type         | description |
| ------------ | ------------ | ----------- |
| info         | BuildDynmaic | 动态构建类    |
| credential   | Credential   | 凭据         |

发送动态（Web端）

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

#### async def get_dynamic_page_UPs_info()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类. |

获取动态页 UP 主列表

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_dynamic_page_info()

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类. |
| _type | DynamicType, optional | 动态类型. Defaults to None. |
| host_mid | int, optional | UP 主 UID. Defaults to None. |
| offset | int, optional | 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to None. |
| pn | int | 页码. Defaults to 1. |

获取动态页动态列表

获取全部动态或者相应类型需传入 _type

获取指定 UP 主动态需传入 host_mid

**Returns:** list[Dynamic]: 动态类列表