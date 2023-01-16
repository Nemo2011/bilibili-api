# Module bilibili_api.black_room

```python
from bilibili_api import black_room
```

## const dict BLACK_TYPE

违规类型代码

## class BlackFrom

**Extends: enum.Enum**

违规来源

- SYSTEM: 系统封禁
- ADMIN: 风纪仲裁
- ALL: 全部

## async def get_blocked_list()

获取小黑屋名单

| name | type | description |
| - | - | - |
| from_ | BlackFrom | 违规来源. Defaults to BlackFrom.ALL. |
| type_ | int | 违规类型. 查看 black_room.BLACK_TYPE。Defaults to 0 (ALL). |
| pn | int | 页数. Defaults to 1. |
| credential | Credential \| None | 凭据, Defaults to None. |

## class BlackRoom()

### Attributes

| name | type | description |
| - | - | - |
| credential | Credential \| None | 凭据类 ｜

### Functions

## def \_\_init\_\_()

| name | type | description |
| - | - | - |
| black_room_id | int | 小黑屋 id |
| credential | Credential \| None | 凭据类. Defaults to None. |

## async def get_details()

获取小黑屋详细信息
