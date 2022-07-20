# 登录函数

`bilibili_api 10.2.0` 新增了登录函数，封装了登录用的脚本，可以通过登录步骤获取 cookies 并生成 `Credential` 类。
有了登录函数后，收集 `Credential` 类就无需打开浏览器翻 `cookies` 啦！

---
**注意：**
用 `linux` 的小伙伴先装一下 `python3-tk` 吧。

``` bash
$ sudo apt-get install python3-tk
```

或者可以先安装 `idle`，众所周知，`idlelib` 是用 `tkinter` 写的。

---
>如果您的系统是 `MacOS`，请务必保证您的 `python` 是官网下载的 `python`，千万别用 `xcode-select` 中的 `python`! 这样可能 `tcl/tk` 版本会不支持，然后就黑屏了！
>当然如果您没出现错误，也不用硬着头皮重装。这里仅供参考。
---

## 举个简单的例子

**下面的程序会跳出一个二维码登录的窗口，登陆成功后会显示您的昵称**

<details>
<summary>展开</summary>

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
</details>
<br>

**当然，密码登录和验证码登录也可以！**

<details>
<summary>展开</summary>

``` python
from bilibili_api.login import login_with_password, login_with_sms, send_sms, PhoneNumber, Check
from bilibili_api.user import get_self_info
from bilibili_api import settings
from bilibili_api import sync

mode = int(input("""请选择登录方式：
1. 密码登录
2. 验证码登录
请输入 1/2
"""))

credential = None

# 关闭自动打开 geetest 验证窗口
settings.geetest_auto_open = False

if mode == 1:
    # 密码登录
    username = input("请输入手机号/邮箱：")
    password = input("请输入密码：")
    print("正在登录。")
    c = login_with_password(username, password)
    if isinstance(c, Check):
        # 还需验证
        phone = input("需要验证。请输入手机号：")
        c.set_phone(PhoneNumber(phone, country="+86")) # 默认设置地区为中国大陆
        c.send_code()
        print("已发送验证码。")
        code = input("请输入验证码：")
        credential = c.login(code)
        print("登录成功！")
    else:
        credential = c
elif mode == 2:
    # 验证码登录
    phone = input("请输入手机号：")
    print("正在登录。")
    send_sms(PhoneNumber(phone, country="+86")) # 默认设置地区为中国大陆
    code = input("请输入验证码：")
    c = login_with_sms(PhoneNumber(phone, country="+86"), code)
    credential = c
    print("登录成功")
else:
    print("请输入 1/2 ！")
    exit()

if credential != None:
    name = sync(get_self_info(credential))['name']
    print(f"欢迎，{name}!")
```

</details>

---

## **详细信息请参考[正文文档](/modules/login.md)**
