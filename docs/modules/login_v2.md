# Module login_v2.py


bilibili_api.login

登录


``` python
from bilibili_api import login_v2
```

---

## Overview

`login_v2` 是对登陆模块的一次彻底的重写，主要有以下改动：

- **将所有同步操作迁移至异步**
- 将 `login` 和 `login_func` 所有功能合并，即把 `login` 功能拆分，结合 `login_func` 进行编写。
- 将 Geetest 实例化，作为参数传入函数，生成、作答、检查、部署本地服务器过程全程由用户操作，取代了原先除作答外全模块操作。
- 同样将二维码登录过程实例化，用户操控生成、检查、获取数据的全流程。

（另一种表达方式：重构）

`login_v2` 相较于 `login` 也更加灵活，可以满足更多情况下的需求，虽然固定功能代码长度相较于原来有所上升，但是编写特定功能起来也更加游刃有余。

因为 `login` 和 `login_v2` 间的完全不兼容，`login` 和 `login_func` 将在之后的版本中暂时保留，甚至永久保留也有可能（懒得删）。

相关使用案例见 [Examples](/examples/login_v2.md)

---

## class PhoneNumber()

手机号类




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| number | str | 手机号 |
| country | str | 地区/地区码，如 +86 |


---

## class QrCodeLogin()

二维码登陆类

支持网页端/TV端




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| platform | Union[QrCodeLoginChannel, None] | 平台. (web/tv) Defaults to QrCodeLoginChannel.WEB. |


### async def check_state()

检查二维码登录状态



**Returns:** QrCodeLoginEvents: 二维码登录状态




### async def generate_qrcode()

生成二维码



**Returns:** None



### def get_credential()

获取登录成功后得到的凭据



**Returns:** Credential: 凭据




### def get_qrcode_picture()

获取二维码的 Picture 类



**Returns:** Picture: 二维码




### def get_qrcode_terminal()

获取二维码的终端字符串



**Returns:** str: 二维码的终端字符串




### def has_done()

是否已经成功登录



**Returns:** bool: 是否已经成功登录




### def has_qrcode()

是否已有已生成的二维码



**Returns:** bool: 是否已有二维码




---

## class QrCodeLoginChannel()

**Extend: enum.Enum**

二维码登陆渠道

- WEB: 网页端
- TV: TV




---

## class QrCodeLoginEvents()

**Extend: enum.Enum**

二维码登录状态枚举

+ SCAN: 未扫描二维码
+ CONF: 未确认登录
+ TIMEOUT: 二维码过期
+ DONE: 成功




---

## def get_code_by_country()

获取地区对应代码


| name | type | description |
| - | - | - |
| country | str | 地区名 |

**Returns:** int: 对应的代码，没有返回 -1




---

## def get_countries_list()

获取国际地区代码列表



**Returns:** List[dict]: 地区列表




---

## def get_id_by_code()

获取地区码对应的地区 id


| name | type | description |
| - | - | - |
| code | int | 地区吗 |

**Returns:** int: 对应的代码，没有返回 -1




---

## def have_code()

是否存在地区代码


| name | type | description |
| - | - | - |
| code | Union[str, int] | 代码 |

**Returns:** bool: 是否存在




---

## def have_country()

是否有地区


| name | type | description |
| - | - | - |
| keyword | str | 关键词 |

**Returns:** bool: 是否存在




---

## async def login_with_password()

密码登录。


| name | type | description |
| - | - | - |
| username | str | 用户手机号、邮箱 |
| password | str | 密码 |
| geetest | Geetest | 极验验证码实例，须完成 |

**Returns:** Union[Credential, Check]: 如果需要验证，会返回 `Check` 类，否则返回 `Credential` 类。




---

## async def login_with_sms()

验证码登录


| name | type | description |
| - | - | - |
| phonenumber | str | 手机号类 |
| code | str | 验证码 |
| captcha_id | str | captcha_id，为 `send_sms` 调用返回结果 |

**Returns:** Credential: 凭据类




---

## def search_countries()

搜索一个地区及其国际地区代码


| name | type | description |
| - | - | - |
| keyword | str | 关键词 |

**Returns:** List[dict]: 地区列表




---

## async def send_sms()

发送验证码


| name | type | description |
| - | - | - |
| phonenumber | PhoneNumber | 手机号类 |
| geetest | Geetest | 极验验证码实例，须完成 |

**Returns:** str: captcha_id，需传入 `login_with_sms`




