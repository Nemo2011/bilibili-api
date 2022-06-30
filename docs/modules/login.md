# Module login.py

登录。

``` python
from bilibili_api import login
```

**虽然可以用 `dir` 捕获其他函数，但是请忽略他们，这些并不重要。**

---

**先唠叨几句：** 所有的登录函数返回的结果都是 `Credential` 类。<br>
**再唠叨几句：** 有界面的登录函数我都是用 `tkinter` 写的，别问为啥，问就是跨平台性能不好。`tkinter` 好歹是官方用的，要是不跨平台那么 `IDLE` 不就是打脸吗？<br>
**最后提个醒：** 用 `linux` 的小伙伴先装一下 `python3-tk` 吧。

``` bash
$ sudo apt-get install python3-tk
```

**好了唠叨完了。请大家注意以上两点。**

---

## def login_with_qrcode()

| name | type | description |
| - | - | - |
| root | Union[tkinter.Tk(), tkinter.Toplevel()] | 窗口 |

**注意：** 这里自定义窗口是因为有的时候写 `tkinter` 程序不能出现两个主窗口 `tkinter.Tk`(如 `ImageTK`)，所以特地设置了窗口参数，大家可以设置成 `tkinter.Toplevel`

扫描二维码登录。

**Returns:** Credential 凭据类。
