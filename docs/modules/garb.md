# Module garb.py


bilibili_api.garb

装扮/收藏集相关


``` python
from bilibili_api import garb
```

- [class DLC()](#class-DLC)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def get\_act\_id()](#def-get\_act\_id)
  - [async def get\_detail()](#async-def-get\_detail)
  - [async def get\_info()](#async-def-get\_info)
  - [async def get\_lottery\_id()](#async-def-get\_lottery\_id)
  - [def set\_act\_id()](#def-set\_act\_id)
- [class Garb()](#class-Garb)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_detail()](#async-def-get\_detail)
  - [def get\_item\_id()](#def-get\_item\_id)
  - [def set\_item\_id()](#def-set\_item\_id)
- [class GarbSortType()](#class-GarbSortType)
- [class GarbType()](#class-GarbType)
- [async def get\_garb\_dlc\_items()](#async-def-get\_garb\_dlc\_items)
- [async def get\_garb\_dlc\_items\_obj()](#async-def-get\_garb\_dlc\_items\_obj)
- [async def get\_garb\_dlc\_items\_raw()](#async-def-get\_garb\_dlc\_items\_raw)
- [async def search\_garb\_dlc()](#async-def-search\_garb\_dlc)
- [async def search\_garb\_dlc\_obj()](#async-def-search\_garb\_dlc\_obj)
- [async def search\_garb\_dlc\_raw()](#async-def-search\_garb\_dlc\_raw)

---

## class DLC()

收藏集对象


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类。 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `act_id` | `int` | 收藏集的 act_id。 (链接中 blackboard/activity-Mz9T5bO5Q3.html?id={act_id}... 即为 act_id) |
| `credential` | `Credential \| None, optional` | 凭据类。Defaults to None. |


### def get_act_id()

获取 act_id。



**Returns:** `int`:  act_id




### async def get_detail()

获取收藏集详情



**Returns:** `dict`:  调用 API 返回的结果




### async def get_info()

获取收藏集信息



**Returns:** `dict`:  调用 API 返回的结果




### async def get_lottery_id()

获取 lottery_id



**Returns:** `int`:  lottery_id




### def set_act_id()

设置 act_id


| name | type | description |
| - | - | - |
| `act_id` | `int` | act_id |




---

## class Garb()

装扮类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类。 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `act_id` | `int` | 装扮的 item_id。(可通过 garb.search_garb_dlc_raw 获取) |
| `credential` | `Credential \| None, optional` | 凭据类。Defaults to None. |


### async def get_detail()

获取装扮详细



**Returns:** `dict`:  调用 API 返回的结果




### def get_item_id()

获取 item_id



**Returns:** `int`:  item_id




### def set_item_id()

设置 item_id


| name | type | description |
| - | - | - |
| `item_id` | `int` | item_id |




---

## class GarbSortType()

**Extend: enum.Enum**

收藏集/装扮排序方式

- DEFAULT: 默认排序
- SELL: 按销量排序
- LATEST: 按最新上架时间排序




---

## class GarbType()

**Extend: enum.Enum**

收藏集/装扮类型

- GARB: 装扮
- PENDANT: 头像挂件
- CARD: 动态卡片




---

## async def get_garb_dlc_items()

装扮/收藏集列表


| name | type | description |
| - | - | - |
| `type_` | `GarbType` | 装扮/收藏集类型 |
| `sort` | `GarbSortType` | 装扮/收藏集排序方式 |
| `pn` | `int` | 页码. Defaults to 1. |
| `ps` | `int` | 每页大小. Defaults to 20. |
| `credential` | `Credential, optional` | 凭据类. Defaults to None. |

**Returns:** `List[Tuple[dict, DLC | Garb]]`:  装扮/收藏集信息与装扮/收藏集对象列表




---

## async def get_garb_dlc_items_obj()

装扮/收藏集列表


| name | type | description |
| - | - | - |
| `type_` | `GarbType` | 装扮/收藏集类型 |
| `sort` | `GarbSortType` | 装扮/收藏集排序方式 |
| `pn` | `int` | 页码. Defaults to 1. |
| `ps` | `int` | 每页大小. Defaults to 20. |
| `credential` | `Credential, optional` | 凭据类. Defaults to None. |

**Returns:** `List[DLC | Garb]`:  装扮/收藏集对象列表




---

## async def get_garb_dlc_items_raw()

装扮/收藏集列表


| name | type | description |
| - | - | - |
| `type_` | `GarbType` | 装扮/收藏集类型 |
| `sort` | `GarbSortType` | 装扮/收藏集排序方式 |
| `pn` | `int` | 页码. Defaults to 1. |
| `ps` | `int` | 每页大小. Defaults to 20. |
| `credential` | `Credential, optional` | 凭据类. Defaults to None. |

**Returns:** `List[Tuple[dict, DLC | Garb]]`:  装扮/收藏集信息与装扮/收藏集对象列表




---

## async def search_garb_dlc()

搜索装扮/收藏集


| name | type | description |
| - | - | - |
| `keyword` | `str` | 关键词 |
| `pn` | `int` | 页码. Defaults to 1. |
| `ps` | `int` | 每页大小. Defaults to 20. |
| `credential` | `Credential, optional` | 凭据类. Defaults to None. |

**Returns:** `List[Tuple[dict, DLC | Garb]]`:  装扮/收藏集信息与装扮/收藏集对象列表




---

## async def search_garb_dlc_obj()

搜索装扮/收藏集


| name | type | description |
| - | - | - |
| `keyword` | `str` | 关键词 |
| `pn` | `int` | 页码. Defaults to 1. |
| `ps` | `int` | 每页大小. Defaults to 20. |
| `credential` | `Credential, optional` | 凭据类. Defaults to None. |

**Returns:** `List[DLC | Garb]`:  装扮/收藏集对象列表




---

## async def search_garb_dlc_raw()

搜索装扮/收藏集


| name | type | description |
| - | - | - |
| `keyword` | `str` | 关键词 |
| `pn` | `int` | 页码. Defaults to 1. |
| `ps` | `int` | 每页大小. Defaults to 20. |
| `credential` | `Credential, optional` | 凭据类. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果。




