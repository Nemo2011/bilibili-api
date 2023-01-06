# Module login.py

登录。

``` python
from bilibili_api import login
```

---
**注意：**

用 `linux` 的小伙伴在使用 `login_with_qrcode` 时先装一下 `python3-tk` 吧。

``` bash
$ sudo apt-get install python3-tk
```

如果想将登录功能嵌入你自己的应用，可以参考[这里](/modules/login_func.md)。
---

## def get_contries_list()

获取国家（地区）列表

**Returns:** List[dict]: 包含国家及地区的列表。

举个例子：下面是 `津巴布韦` 对应的字典

``` python
{
    'name': '津巴布韦', # 就像 `中国大陆`
    'id': 98, # 貌似是 B 站自己的 id
    'code': 263 # 对应的代码，就像中国大陆的 +86
}
```

## def search_countries()

| name | type | description |
| - | - | - |
| keyword | str | 关键词 |

搜索一个地区及其国际地区代码

**Returns:** List[dict]: 地区列表

## def have_country()

| name | type | description |
| - | - | - |
| keyword | str | 关键词 |

是否有地区

**Returns:** bool: 是否存在

## def have_code()

| name | type | description |
| - | - | - |
| code | Union[str, int]) | 代码 |

是否存在地区代码

**Returns:** bool: 是否存在

## class PhoneNumber()

手机号类

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| number | str | 号码 |
| country | Union[str, int] | 地区（代码）如 `中国大陆` 或 `+86` |

---

## def login_with_qrcode()

| name | type | description |
| - | - | - |
| root | Union[tkinter.Tk(), tkinter.Toplevel()] | 窗口 |

**注意：** 这里自定义窗口是因为有的时候写 `tkinter` 程序不能出现两个主窗口 `tkinter.Tk`(如使用 `ImageTK`)，所以特地设置了窗口参数，大家可以设置成 `tkinter.Toplevel`

扫描二维码登录。

**Returns:** Credential 凭据类。

## def login_with_password()

| name | type | description |
| - | - | - |
| username | str | 手机号、邮箱 |
| password | str | 密码 |

密码登录。

**Returns:** Union[Credential, Check]: 如果需要验证，会返回 [`Check`](#check) 类，否则返回 `Credential` 类。

## def send_sms()

**需要经过极验验证**

| name | type | description |
| - | - | - |
| phonenumber | PhoneNumber | 手机号类 |

发送验证码。

**Returns:** None

## def login_with_sms()

| name | type | description |
| - | - | - |
| phonenumber | PhoneNumber | 手机号类 |
| code | str | 验证码 |

验证码登录

**Returns:** Credential 凭据类

**如果返回错误：验证码错误，请尝试再次完成极验验证码（极验验证码结果一个只能用一次）**

---

## <span id="check"> class Check </span>

验证类，如果密码登录需要验证会返回此类

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| check_url | str | 验证网址 |

#### def fetch_info()

获取验证信息

**Returns:** dict: 调用 API 返回的结果

#### def send_sms()

**需要经过极验验证**

发送验证码

#### def complete_check()

完成验证

| name | type | description |
| - | - | - |
| code | str | 验证码 |

**Returns:** Credential: 凭据类

---
