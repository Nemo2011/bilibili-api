# Module show.py

bilibili会员购展出相关

```py
from bilibili_api import show
```

## 定义

* 项目id:
  * 在URL https://show.bilibili.com/platform/detail.html?id=75650 中项目id为`75650`

## def get_project_info()

| name       | type | description |
|------------|------|-------------|
| project_id | int  | 项目id        |

返回项目全部信息

**Returns:** dict: 调用 API 返回的结果

## def get_available_sessions()

| name       | type | description |
|------------|------|-------------|
| project_id | int  | 项目id        |

返回该项目的所有可用场次

**Returns:** list[Session]: 存放场次对象的list

## def get_all_buyer_info()

返回账号的全部身份信息

| 属性名          | 类型         | 表述   |
|--------------|------------|------|
| credential   | Credential | 登录凭证 |

**Returns:** dict: 调用 API 返回的结果

## def get_all_buyer_info_obj()

以`BuyerInfo`对象返回账号的全部身份信息

| 属性名          | 类型         | 表述   |
|--------------|------------|------|
| credential   | Credential | 登录凭证 |

**Returns:** list[BuyerInfo]: BuyerInfo对象列表

## generate_clickPosition():

生成虚假的点击事件

**Returns:** dict: 点击坐标和时间

## class OrderTicket

### def _\_init\_\_()

| 属性名          | 类型         | 表述         |
|--------------|------------|------------|
| credential   | Credential | 登录凭证       |
| target_buyer | BuyerInfo  | 购票人        |
| project_id   | int        | 展出id       |
| session      | Session    | Session 对象 |
| ticket       | Ticket     | Ticket 对象  |

### def get_token()

获取购票Token

**Returns:** dict: 调用 API 返回的结果

#### 注意

* 由于某些原因，如 场次、票类型 不可用等原因会导致`token`不会出现，并且`code`返回`0`

### def create_order()

创建购买订单

**Returns:** dict: 调用 API 返回的结果

#### 注意

* 提交成功的回显为:

```json
{
  "token": "xxx"
}
```

* 失败可能为: `{}`等其他情况

---

* 可能有时候需要滑动验证，注意`shield`键中的键值

```json
{
  "shield": {
    "open": 0,
    "verifyMethod": "",
    "verifyType": 0,
    "verifyRelation": "",
    "business": "",
    "customerId": 0,
    "voucher": "",
    "type": 0,
    "h5Url": "",
    "pcUrl": "",
    "msg": "",
    "naUrl": ""
  },
  "token": "xxx"
}
```

---

* 目前create_order只支持一单一票，对于一单多票目前还未实现

## class Ticket

| 属性名        | 类型  | 描述           |
|------------|-----|--------------|
| id         | int | 场次id         |
| price      | int | 原价格(RMB)*100 |
| desc       | str | 描述           |
| sale_start | str | 开售开始时间       |
| sale_end   | str | 开售结束时间       |

### 注意

* price属性的值为`(原价格*100)`
  * 如原价格为`233.33`元, price值则为`23333`

## class Session

场次对象

| 属性名            | 类型           | 描述                                   |
|----------------|--------------|--------------------------------------|
| id             | int          | 场次id                                 |
| start_time     | int          | 场次开始时间戳                              |
| formatted_time | str          | 格式化start_time后的时间格式: YYYY-MM-DD dddd |
| ticket_list    | list[Ticket] | 存放Ticket对象的list                      |

## class BuyerInfo

购买人信息

| 属性名                 | 类型   | 表述       |
|---------------------|------|----------|
| id                  | int  | 信息序号     |
| uid                 | int  | 用户 ID    |
| account_channel     | str  | 默认为空     |
| personal_id         | str  | 身份证号     |
| name                | str  | 姓名       |
| id_card_front       | str  | 未知       |
| id_card_back        | str  | 未知       |
| is_default          | bool | 是否为默认信息  |
| tel                 | str  | 电话号码     |
| error_code          | str  | 错误代码     |
| id_type             | int  | 默认 0     |
| verify_status       | int  | 认证状态     |
| accountId           | int  | 用户 ID    |
| isBuyerInfoVerified | bool | 默认为 True |
| isBuyerValid        | bool | 默认为 True |
