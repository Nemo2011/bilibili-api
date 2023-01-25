# Module channel.md

频道相关，与视频分区不互通。

``` python
from bilibili_api import channel
```

## async def get_channel_categories()

获取所有的频道分类（如游戏、鬼畜等）。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_channel_category_detail()

| name | type | description |
| ---- | ---- | ----------- |
| category_id | int | 频道分类的 id。 |
| offset | str | 偏移值（下面的数据的第一个频道 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to "0" |

获取频道分类的频道列表及其详细信息

---

## class ChannelVideosOrder()

**Extends: enum.Enum**

- NEW: 最新
- HOT: 最火
- VIEW: 播放量最高

---

## class ChannelVideosFilter()

**Extends: enum.Enum**

- ALL     : 全部
- YEAR_年份: 指定年份筛选

---

## class Channel

频道类。

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| channel_id | int | 频道 id. |

#### def get_channel_id()

获取频道 id

**Returns:** int: 频道 id

#### async def get_info()

获取频道详细信息

**Returns:** dict: HTML 中 window.\_\_INITIAL_STATE\_\_ 中的信息

#### async def get_related()

获取相关频道

**Returns:** dict: HTML 中 window.\_\_INITIAL_STATE\_\_ 中的信息

#### async def get_list()

| name | type | description |
| ---- | ---- | ----------- |
| order_or_filter | ChannelVideosOrder \| ChannelVideosFilter \| None | 获取视频的相关选项 |
| offset | str | 偏移值（下面的第一个视频的 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to "" |
| page_size | int | 每页的数据大小. Defaults to 30.  |

获取频道的所有视频

**Returns:** dict: 调用 API 返回的结果

---

## async def get_channels_in_category()

获取频道分类中的所有频道。

| name | type | description |
| ---- | ---- | ----------- |
| category_id | int | 频道 id |

**Returns:** List[Channel]: 频道分类中的所有频道。

---

## async def get_self_subscribe_channels()

获取自己订阅的频道

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类 |

**Returns:** dict: 调用 API 返回的结果

---

## async def subscribe_channel()

订阅频道

| name | type | description |
| ---- | ---- | ----------- |
| channel | Channel | 要订阅的频道 |
| credential | Credential | 凭据类 |

**Returns:** dict: 调用 API 返回的结果
