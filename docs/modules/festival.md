# Module festival.py


bilibili_api.festival

节日专门页相关


``` python
from bilibili_api import festival
```

- [class Festival()](#class-Festival)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_info()](#async-def-get\_info)

---

## class Festival()

节日专门页


| name | type | description |
| - | - | - |
| `fes_id` | `str` | 节日专门页编号 |
| `credential` | `Credential` | 凭证类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `fes_id` | `str` | 节日专门页编号 |
| `credential` | `Credential, optional` | 凭据类. Defaults to None. |


### async def get_info()

获取节日信息



**Returns:** `dict`:  调用 API 返回的结果




