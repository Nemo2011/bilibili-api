# Module login_v2.py


bilibili_api.login_v2

登录


``` python
from bilibili_api import login_v2
```

- [class LoginCheck()](#class-LoginCheck)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def complete\_check()](#async-def-complete\_check)
  - [async def fetch\_info()](#async-def-fetch\_info)
  - [async def send\_sms()](#async-def-send\_sms)
- [class PhoneNumber()](#class-PhoneNumber)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
- [class QrCodeLogin()](#class-QrCodeLogin)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def check\_state()](#async-def-check\_state)
  - [async def generate\_qrcode()](#async-def-generate\_qrcode)
  - [def get\_credential()](#def-get\_credential)
  - [def get\_qrcode\_picture()](#def-get\_qrcode\_picture)
  - [def get\_qrcode\_terminal()](#def-get\_qrcode\_terminal)
  - [def has\_done()](#def-has\_done)
  - [def has\_qrcode()](#def-has\_qrcode)
- [class QrCodeLoginChannel()](#class-QrCodeLoginChannel)
- [class QrCodeLoginEvents()](#class-QrCodeLoginEvents)
- [def get\_code\_by\_country()](#def-get\_code\_by\_country)
- [def get\_countries\_list()](#def-get\_countries\_list)
- [def get\_id\_by\_code()](#def-get\_id\_by\_code)
- [def have\_code()](#def-have\_code)
- [def have\_country()](#def-have\_country)
- [async def login\_with\_password()](#async-def-login\_with\_password)
- [async def login\_with\_sms()](#async-def-login\_with\_sms)
- [def search\_countries()](#def-search\_countries)
- [async def send\_sms()](#async-def-send\_sms)

---

## class LoginCheck()

验证类，如果密码登录需要验证会返回此类




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `check_url` | `str` | 验证链接 |


### async def complete_check()

完成验证


| name | type | description |
| - | - | - |
| `code` | `str` | 验证码 |

**Returns:** `Credential`:  凭据类




### async def fetch_info()

获取验证信息



**Returns:** `dict`:  调用 API 返回的结果




### async def send_sms()

发送验证码


| name | type | description |
| - | - | - |
| `geetest` | `Geetest` | 极验验证码实例，须完成。验证码类型应为 `GeetestType.VERIFY` |




---

## class PhoneNumber()

手机号类




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `number` | `str` | 手机号 |
| `country` | `str` | 地区/地区码，如 +86 |


---

## class QrCodeLogin()

二维码登陆类

支持网页端/TV端




### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `platform` | `QrCodeLoginChannel, optional` | 平台. (web/tv) Defaults to QrCodeLoginChannel.WEB. |


### async def check_state()

检查二维码登录状态



**Returns:** `QrCodeLoginEvents`:  二维码登录状态




### async def generate_qrcode()

生成二维码






### def get_credential()

获取登录成功后得到的凭据



**Returns:** `Credential`:  凭据




### def get_qrcode_picture()

获取二维码的 Picture 类



**Returns:** `Picture`:  二维码




### def get_qrcode_terminal()

获取二维码的终端字符串



**Returns:** `str`:  二维码的终端字符串




### def has_done()

是否已经成功登录



**Returns:** `bool`:  是否已经成功登录




### def has_qrcode()

是否已有已生成的二维码



**Returns:** `bool`:  是否已有二维码




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
| `country` | `str` | 地区名 |

**Returns:** `int`:  对应的代码，没有返回 -1




---

## def get_countries_list()

获取国际地区代码列表



**Returns:** `List[dict]`:  地区列表




---

## def get_id_by_code()

获取地区码对应的地区 id


| name | type | description |
| - | - | - |
| `code` | `int` | 地区吗 |

**Returns:** `int`:  对应的代码，没有返回 -1




---

## def have_code()

是否存在地区代码


| name | type | description |
| - | - | - |
| `code` | `Union[str, int]` | 代码 |

**Returns:** `bool`:  是否存在




---

## def have_country()

是否有地区


| name | type | description |
| - | - | - |
| `keyword` | `str` | 关键词 |

**Returns:** `bool`:  是否存在




---

## async def login_with_password()

密码登录。


| name | type | description |
| - | - | - |
| `username` | `str` | 用户手机号、邮箱 |
| `password` | `str` | 密码 |
| `geetest` | `Geetest` | 极验验证码实例，须完成。验证码类型应为 `GeetestType.LOGIN` |

**Returns:** `Union[Credential, LoginCheck]`:  如果需要验证，会返回 `LoginCheck` 类，否则返回 `Credential` 类。




---

## async def login_with_sms()

验证码登录


| name | type | description |
| - | - | - |
| `phonenumber` | `str` | 手机号类 |
| `code` | `str` | 验证码 |
| `captcha_id` | `str` | captcha_id，为 `send_sms` 调用返回结果 |

**Returns:** `Union[Credential, LoginCheck]`:  如果需要验证，会返回 `LoginCheck` 类，否则返回 `Credential` 类。




---

## def search_countries()

搜索一个地区及其国际地区代码


| name | type | description |
| - | - | - |
| `keyword` | `str` | 关键词 |

**Returns:** `List[dict]`:  地区列表




---

## async def send_sms()

发送验证码


| name | type | description |
| - | - | - |
| `phonenumber` | `PhoneNumber` | 手机号类 |
| `geetest` | `Geetest` | 极验验证码实例，须完成。验证码类型应为 `GeetestType.LOGIN` |

**Returns:** `str`:  captcha_id，需传入 `login_with_sms`




