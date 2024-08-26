# Module login_func.py


bilibili_api.login_func

登录功能相关


``` python
from bilibili_api import login_func
```

## class QrCodeLoginEvents

**Extend: enum.Enum**

二维码登录状态枚举

+ SCAN: 未扫描二维码
+ CONF: 未确认登录
+ TIMEOUT: 二维码过期
+ DONE: 成功




## def check_qrcode_events()

检查登录状态。（建议频率 1s，这个 API 也有风控！）


| name | type | description |
| - | - | - |
| login_key | str | 登录密钥（get_qrcode 的返回值第二项) |

**Returns:** Tuple[QrCodeLoginEvents, str|Credential]: 状态(第一项）和信息（第二项）（如果成功登录信息为凭据类）




## def check_tv_qrcode_events()

检查登录状态。


| name | type | description |
| - | - | - |
| auth_code | str | 登录密钥 |

**Returns:** Tuple[QrCodeLoginEvents, str|Credential]: 状态(第一项）和信息（第二项）（如果成功登录信息为凭据类）




## def close_geetest_server()

关闭极验验证服务（打开极验验证服务后务必关闭掉它，否则会卡住）



**Returns:** None



## def done_geetest()

检查是否完成了极验验证。

如果没有完成极验验证码就开始短信登录发送短信，那么可能会让你的项目卡住。



**Returns:** bool: 是否完成极验验证




## def get_qrcode()

获取二维码及登录密钥（后面有用）



**Returns:** Tuple[Picture, str]: 第一项是二维码图片地址（本地缓存）和登录密钥。登录密钥需要保存。




## def get_tv_qrcode()

获取 TV 端登录二维码及登录密钥（后面有用）



**Returns:** Tuple[Picture, str]: 第一项是二维码图片地址（本地缓存）和登录密钥。登录密钥需要保存。




## def safecenter_close_geetest_server()

登录验证专用函数：关闭极验验证服务（打开极验验证服务后务必关闭掉它，否则会卡住）



**Returns:** None



## def safecenter_done_geetest()

登录验证专用函数：检查是否完成了极验验证。

如果没有完成极验验证码就开始短信登录发送短信，那么可能会让你的项目卡住。



**Returns:** bool: 是否完成极验验证




## def safecenter_start_geetest_server()

登录验证专用函数：验证码服务打开服务器



**Returns:** ServerThread: 服务进程，将自动开启


返回值内函数及属性:
(继承：threading.Thread)
- url   (str) : 验证码服务地址
- start (Callable): 开启进程
- stop  (Callable): 结束进程

``` python
print(start_geetest_server().url)
```



## def start_geetest_server()

验证码服务打开服务器



**Returns:** ServerThread: 服务进程，将自动开启


返回值内函数及属性:
(继承：threading.Thread)
- url   (str) : 验证码服务地址
- start (Callable): 开启进程
- stop  (Callable): 结束进程

``` python
print(start_geetest_server().url)
```



