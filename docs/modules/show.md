# Module show.py


bilibili_api.show

展出相关


``` python
from bilibili_api import show
```

- [class BuyerInfo()](#class-BuyerInfo)
- [class OrderTicket()](#class-OrderTicket)
  - [async def create\_order()](#async-def-create\_order)
  - [async def get\_token()](#async-def-get\_token)
- [class Session()](#class-Session)
- [class Ticket()](#class-Ticket)
- [async def get\_all\_buyer\_info()](#async-def-get\_all\_buyer\_info)
- [async def get\_all\_buyer\_info\_obj()](#async-def-get\_all\_buyer\_info\_obj)
- [async def get\_available\_sessions()](#async-def-get\_available\_sessions)
- [async def get\_project\_info()](#async-def-get\_project\_info)

---

**@dataclasses.dataclass** 

## class BuyerInfo()

购买人信息

id (int): 信息序号

uid (int): 用户 ID

account_channel (str): 默认为空

personal_id (str): 身份证号

name (str): 姓名

id_card_front (str): 未知

id_card_back (str): 未知

is_default (bool): 是否为默认信息

tel (str): 电话号码

error_code (str): 错误代码

id_type (int): 默认 0

verify_status (int): 认证状态

accountId (int): 用户 ID

isBuyerInfoVerified (bool): 默认为 True

isBuyerValid (bool): 默认为 True




---

**@dataclasses.dataclass** 

## class OrderTicket()

购票类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | Credential 对象 |
| `target_buyer` | `BuyerInfo` | 购票人 |
| `project_id` | `int` | 展出id |
| `session` | `Session` | Session 对象 |
| `ticket` | `Ticket` | Ticket 对象 |


### async def create_order()

创建购买订单



**Returns:** `dict`:  调用 API 返回的结果




### async def get_token()

获取购票Token



**Returns:** `dict`:  调用 API 返回的结果




---

**@dataclasses.dataclass** 

## class Session()

场次对象

id (int): 场次id

start_time (int): 场次开始时间戳

formatted_time (str): 格式化start_time后的时间格式: YYYY-MM-DD dddd

ticket_list (list[Ticket]): 存放Ticket对象的list




---

**@dataclasses.dataclass** 

## class Ticket()

票对象

id (int): 场次id

price (float): 价格(RMB)

desc (str): 描述

sale_start (str): 开售开始时间

sale_end (str): 开售结束时间




---

## async def get_all_buyer_info()

返回账号的全部身份信息


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 登录凭证 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_all_buyer_info_obj()

以BuyerInfo对象返回账号的全部身份信息


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 登录凭证 |

**Returns:** `list[BuyerInfo]`:  BuyerInfo对象列表




---

## async def get_available_sessions()

返回该项目的所有可用场次


| name | type | description |
| - | - | - |
| `project_id` | `int` | 项目id |

**Returns:** `list[Session]`:  存放场次对象的list




---

## async def get_project_info()

返回项目全部信息


| name | type | description |
| - | - | - |
| `project_id` | `int` | 项目id |

**Returns:** `dict`:  调用 API 返回的结果




