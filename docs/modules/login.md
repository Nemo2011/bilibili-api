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

## def login_with_qrcode()

| name | type | description |
| - | - | - |
| root | Union[tkinter.Tk(), tkinter.Toplevel()] | 窗口 |

**注意：** 这里自定义窗口是因为有的时候写 `tkinter` 程序不能出现两个主窗口 `tkinter.Tk`(如 `ImageTK`)，所以特地设置了窗口参数，大家可以设置成 `tkinter.Toplevel`

扫描二维码登录。

**Returns:** Credential 凭据类。
