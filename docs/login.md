# 登录函数

`bilibili_api 10.2.0` 新增了登录函数，封装了登录用的脚本，可以快速获取 `Credential` 类。
有了登录函数后，收集 `Credential` 类就无需打开浏览器翻 `cookies` 啦！

## 举个简单的例子

**下面的程序会跳出一个二维码登录的窗口，登陆成功后会显示您的昵称**

``` python
from bilibili_api import login, user, sync
print("请登录：")
credential = login.login_with_qrcode()
try:
    credential.raise_for_no_bili_jct() # 判断是否成功
    credential.raise_for_no_sessdata() # 判断是否成功
except:
    print("登陆失败。。。")
    exit()
print("欢迎，", sync(user.get_self_info(credential))['name'], "!")
```
