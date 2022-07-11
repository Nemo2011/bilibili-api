# Module login.py

登录。

``` python
from bilibili_api import login
```

---
**注意：**
用 `linux` 的小伙伴先装一下 `python3-tk` 吧。

``` bash
$ sudo apt-get install python3-tk
```

---
>如果您的系统是 `MacOS`，请务必保证您的 `python` 是官网下载的 `python`，千万别用 `xcode-select` 中的 `python`! 作者测过，可能 `tcl/tk` 版本会不支持，然后就黑屏了！
>当然如果您没出现错误，也不用硬着头皮重装。这里仅供参考。
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
| keyword | string | 关键词 |

搜索一个地区及其国际地区代码

**Returns:** List[dict]: 地区列表

## def have_country()

| name | type | description |
| - | - | - |
| keyword | string | 关键词 |

是否有地区

**Returns:** bool: 是否存在

## def have_code()

| name | type | description |
| - | - | - |
| code | Union[str, int]) | 代码 |

是否存在地区代码

**Returns:** bool: 是否存在

## class PhoneNumber()

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| number | string | 号码 |
| country | Union[string, int] | 地区（代码）如 `中国大陆` 或 `+86` |

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
| username | string | 手机号、邮箱 |
| password | string | 密码 |

密码登录。

**Returns:** Union[Credential, Check]: 如果需要验证，会返回 [`Check`](#check) 类，否则返回 `Credential` 类。

## def send_sms()

| name | type | description |
| - | - | - |
| phonenumber | PhoneNumber | 手机号类 |

发送验证码。

**Returns:** None

## def login_with_sms()

| name | type | description |
| - | - | - |
| phonenumber | PhoneNumber | 手机号类 |
| code | string | 验证码 |

验证码登录

**Returns:** Credential 凭据类

---

## <span id="check"> class Check </span>

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| check_url | string | 验证网址 |

#### def set_phone()

设置手机号

| name | type | description |
| - | - | - |
| phonenumber | PhoneNumber | 手机号类 |

**Returns:** None

#### def send_code()

发送验证码

**Returns:** None

#### def login()

| name | type | description |
| - | - | - |
| code | string | 验证码 |

登录

**Returns:** Credential 凭据类

---
