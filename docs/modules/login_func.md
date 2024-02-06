# Module login_func.py

登录功能。

``` python
from bilibili_api import login_func
```

这个库是专门为嵌入登录功能准备的。如果想要将登录功能嵌入你自己的 gui，那用 `login_func` 库就对了！

---

## const list COUNTRIES_LIST

国际地区代码列表

下面是 `津巴布韦` 对应的字典

``` python
{
    'name': '津巴布韦', # 就像 `中国大陆`
    'id': 98, # 貌似是 B 站自己的 id
    'code': 263 # 对应的国际地区代码，就像中国大陆的 +86
}
```

## 1. 二维码登录

二维码登录要展示二维码，并实时监视登录状态。

### class QrCodeLoginEvents()

#### Extends: enum.Enum

二维码登录状态枚举

+ SCAN: 未扫描二维码
+ CONF: 未确认登录
+ TIMEOUT: 二维码过期
+ DONE: 成功

### def get_qrcode()

获取二维码及登录密钥（后面有用）

**returns:** Tuple[Picture, str]: 第一项是二维码图片地址（本地缓存）和登录密钥。登录密钥需要保存。

### def check_qrcode_events()

| name | type | description |
| - | - | - |
| login_key | str | 登录密钥（get_qrcode 的返回值第二项) |

检查登录状态。（建议频率 1s，这个 API 也有风控！）

**returns:** Tuple[QrCodeLoginEvents, str|Credential]: 状态(第一项）和信息（第二项）（如果成功登录信息为凭据类）

### def get_tv_qrcode()

获取二维码及登录密钥（后面有用）

**returns:** Tuple[Picture, str]: 第一项是二维码图片地址（本地缓存）和登录密钥。登录密钥需要保存。

### def check_tv_qrcode_events()

| name | type | description |
| - | - | - |
| auth_code | str | 登录密钥（get_qrcode 的返回值第二项) |

检查登录状态。

**returns:** Tuple[QrCodeLoginEvents, str|Credential]: 状态(第一项）和信息（第二项）（如果成功登录信息为凭据类）

---

## 2. 极验验证码

短信登录需要完成极验验证。这些函数可以将极验验证嵌入你的 gui。

### def start_geetest_server()

开启极验验证服务

bilibili_api 完成极验验证的方式是新建一个 `http.server.HttpServer`。~~具体实现抄了 `pydoc`(Python 模块文档)~~

返回值内函数及属性: 
    (继承：threading.Thread)
    - url   (str)     : 验证码服务地址
    - start (Callable): 开启进程
    - stop  (Callable): 结束进程

``` python
print(start_geetest_server().url)
```

**Returns:** 极验验证码服务进程。

### def close_geetest_server()

关闭极验验证服务（打开极验验证服务后务必关闭掉它，否则会卡住）

### def done_geetest()

检查是否完成了极验验证。**如果没有完成极验验证码就开始短信登录发送短信，那么可能会让你的项目卡住。**

**Returns:** bool: 是否完成极验验证
