# Module festival.py

```python
from bilibili_api import festival
```

节日专门页相关

> **Note:** 此处 `节日专门页` 指以下 `url`:

> - `https://www.bilibili.com/festival/*`

---

## class Festival

节日专门页

### Attributes

| name | type | description |
| - | - | - |
| fes_id | str | 节日专门页编号 |
| credential | Credential | 凭证类 |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| fes_id | str | 节日专门页编号 |
| credential | Credential | 凭证类 |

#### async def get_info()

获取节日信息

**Returns:** dict: 调用 API 返回的结果
