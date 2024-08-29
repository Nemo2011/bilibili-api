# Module login.py


bilibili_api.login

登录

**虽然可能有其他函数，但是请忽略他们，这些并不重要**

**login_with_qrcode 用到了 tkinter，linux 的小伙伴请注意安装**


``` python
from bilibili_api import login
```

--

## class Check()

验证类，如果密码登录需要验证会返回此类


| name | type | description |
| - | - | - |
| check_url | str | 验证 url |
| tmp_token | str | 验证 token |


### def fetch_info()

获取验证信息



**Returns:** dict: 调用 API 返回的结果




--

## class PhoneNumber()

手机号类




--

## def get_code_by_country()

获取地区对应代码


| name | type | description |
| - | - | - |
| country | str | 地区名 |

**Returns:** int: 对应的代码，没有返回 -1




--

## def get_countries_list()

获取国际地区代码列表



**Returns:** List[dict]: 地区列表




--

## def get_id_by_code()

获取地区码对应的地区 id


| name | type | description |
| - | - | - |
| code | int | 地区吗 |

**Returns:** int: 对应的代码，没有返回 -1




--

## def have_code()

是否存在地区代码


| name | type | description |
| - | - | - |
| code | Union[str, int] | 代码 |

**Returns:** bool: 是否存在




--

## def have_country()

是否有地区


| name | type | description |
| - | - | - |
| keyword | str | 关键词 |

**Returns:** bool: 是否存在




--

## def login_with_password()

密码登录。


| name | type | description |
| - | - | - |
| username | str | 用户手机号、邮箱 |
| password | str | 密码 |

**Returns:** Union[Credential, Check]: 如果需要验证，会返回 `Check` 类，否则返回 `Credential` 类。




--

## def login_with_qrcode()

扫描二维码登录


| name | type | description |
| - | - | - |
| root | Union[tkinter.Tk, None] | 根窗口，默认为 tkinter.Tk()，如果有需要可以换成 tkinter.Toplevel(). Defaults to None. |

**Returns:** Credential: 凭据




--

## def login_with_qrcode_term()

终端扫描二维码登录



**Returns:** Credential: 凭据




--

## def login_with_sms()

验证码登录


| name | type | description |
| - | - | - |
| phonenumber | str | 手机号类 |
| code | str | 验证码 |

**Returns:** Credential: 凭据类




--

## def login_with_tv_qrcode_term()

终端扫描 TV 二维码登录



**Returns:** Credential: 凭据




--

## def search_countries()

搜索一个地区及其国际地区代码


| name | type | description |
| - | - | - |
| keyword | str | 关键词 |

**Returns:** List[dict]: 地区列表




--

## def send_sms()

发送验证码


| name | type | description |
| - | - | - |
| phonenumber | PhoneNumber | 手机号类 |

**Returns:** None



