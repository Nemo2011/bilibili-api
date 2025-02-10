# Module app.py


bilibili_api.app

手机 APP 相关


``` python
from bilibili_api import app
```

- [async def get\_loading\_images()](#async-def-get\_loading\_images)
- [async def get\_loading\_images\_special()](#async-def-get\_loading\_images\_special)

---

## async def get_loading_images()

获取开屏启动画面


| name | type | description |
| - | - | - |
| `build` | `int, optional` | 客户端内部版本号 |
| `mobi_app` | `str, optional` | android / iphone / ipad |
| `platform` | `str, optional` | android / ios/ ios |
| `height` | `int, optional` | 屏幕高度 |
| `width` | `int, optional` | 屏幕宽度 |
| `birth` | `str, optional` | 生日日期(四位数，例 0101) |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_loading_images_special()

获取特殊开屏启动画面


| name | type | description |
| - | - | - |
| `mobi_app` | `str, optional` | android / iphone / ipad |
| `platform` | `str, optional` | android / ios/ ios |
| `height` | `str, optional` | 屏幕高度 |
| `width` | `str, optional` | 屏幕宽度 |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




