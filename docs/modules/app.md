# Module app.py


bilibili_api.app

手机 APP 相关


``` python
from bilibili_api import app
```

---

## async def get_loading_images()

获取开屏启动画面


| name | type | description |
| - | - | - |
| build | Union[int, None] | 客户端内部版本号 |
| mobi_app | Union[str, None] | android / iphone / ipad |
| platform | Union[str, None] | android / ios/ ios |
| height | Union[int, None] | 屏幕高度 |
| width | Union[int, None] | 屏幕宽度 |
| birth | Union[str, None] | 生日日期(四位数，例 0101) |
| credential | Union[Credential, None] | 凭据. Defaults to None. |

**Returns:** dict: 调用 API 返回的结果




---

## async def get_loading_images_special()

获取特殊开屏启动画面


| name | type | description |
| - | - | - |
| mobi_app | Union[str, None] | android / iphone / ipad |
| platform | Union[str, None] | android / ios/ ios |
| height | Union[str, None] | 屏幕高度 |
| width | Union[str, None] | 屏幕宽度 |
| credential | Union[Credential, None] | 凭据. Defaults to None. |

**Returns:** dict: 调用 API 返回的结果




