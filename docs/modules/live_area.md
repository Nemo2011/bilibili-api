# Module live_area.py


bilibili_api.live_area

直播间分区相关操作。


``` python
from bilibili_api import live_area
```

- [class LiveRoomOrder()](#class-LiveRoomOrder)
- [async def fetch\_live\_area\_data()](#async-def-fetch\_live\_area\_data)
- [def get\_area\_info\_by\_id()](#def-get\_area\_info\_by\_id)
- [def get\_area\_info\_by\_name()](#def-get\_area\_info\_by\_name)
- [def get\_area\_list()](#def-get\_area\_list)
- [def get\_area\_list\_sub()](#def-get\_area\_list\_sub)
- [async def get\_list\_by\_area()](#async-def-get\_list\_by\_area)

---

## class LiveRoomOrder()

**Extend: enum.Enum**

直播间排序方式

- RECOMMEND: 综合
- NEW: 最新




---

## async def fetch_live_area_data()

抓取直播分区数据

因为直播分区容易出现变动，故不像视频分区一样直接使用文件保存，而是每次查询时先抓取一遍。

一次运行整个程序仅需执行一次此函数即可，无需多次调用。






---

## def get_area_info_by_id()

根据 id 获取分区信息。


| name | type | description |
| - | - | - |
| `id` | `int` | 分区的 id。 |

**Returns:** `Tuple[dict | None, dict | None]`:  第一个是主分区，第二个是子分区，没有时返回 None。




---

## def get_area_info_by_name()

根据频道名称获取频道信息。


| name | type | description |
| - | - | - |
| `name` | `str` | 分区的名称。 |

**Returns:** `Tuple[dict | None, dict | None]`:  第一个是主分区，第二个是子分区，没有时返回 None。




---

## def get_area_list()

获取所有分区的数据



**Returns:** `List[dict]`:  所有分区的数据




---

## def get_area_list_sub()

获取所有分区的数据
含父子关系（即一层次只有主分区）



**Returns:** `dict`:  所有分区的数据




---

## async def get_list_by_area()

根据分区获取直播间列表


| name | type | description |
| - | - | - |
| `area_id` | `int` | 分区 id |
| `page` | `int` | 第几页. Defaults to 1. |
| `order` | `LiveRoomOrder` | 直播间排序方式. Defaults to LiveRoomOrder.RECOMMEND. |
| `credential` | `Credential, optional` | 凭据类. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




