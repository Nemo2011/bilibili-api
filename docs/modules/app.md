# Module app.py

```python
from bilibili_api import app
```

手机 APP 相关

## async def get_loading_images()

| name       | type                 | description               |
| ---------- | -------------------- | ------------------------- |
| build      | int, optional        | 客户端内部版本号          |
| mobi_app   | str, optional        | android / iphone / ipad   |
| platform   | str, optional        | android / ios  / ios      |
| height     | int, optional        | 屏幕高度                  |
| width      | int, optional        | 屏幕宽度                  |
| birth      | str, optional        | 生日日期(四位数，例 0101) |
| credential | Credential \| None, optional | 凭据                      |

获取开屏启动画面

**Returns:** API 调用返回结果

---

## async def get_loading_images_special()

| name       | type                 | description             |
| ---------- | -------------------- | ----------------------- |
| mobi_app   | str, optional        | android / iphone / ipad |
| platform   | str, optional        | android / ios  / ios    |
| height     | int, optional        | 屏幕高度                |
| width      | int, optional        | 屏幕宽度                |
| credential | Credential \| None, optional | 凭据                    |

获取特殊开屏启动画面

**Returns:** API 调用返回结果

---

