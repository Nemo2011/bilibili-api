# 登录函数

`bilibili_api 10.2.0` 新增了登录函数，封装了登录用的脚本，可以快速获取 `Credential` 类。
有了登录函数后，收集 `Credential` 类就无需打开浏览器翻 `cookies` 啦！

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
