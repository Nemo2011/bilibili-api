# Module emoji.py


bilibili_api.emoji

表情包相关


``` python
from bilibili_api import emoji
```

---

## async def get_all_emoji()

获取所有表情包


| name | type | description |
| - | - | - |
| business | str | 使用场景, reply / dynamic |
| credential | Credential | 登录凭证. Defaults to None. |

**Returns:** dict: 调用 API 返回的结果




---

## def get_all_emote_list()

获取所有表情包 id <-> 对应文字



**Returns:** dict: 模块存储的数据 (`last_update` 字段为最后更新时间)


如果数据更新时间过早，可能会遗漏新的表情包。此时可用 `get_all_emoji` + `get_emoji_detail` 查询相关信息，或前往 Github 催促更新。



---

## async def get_emoji_detail()

获取表情包详情


| name | type | description |
| - | - | - |
| id | Union[int, List[int]] | 表情包 id，可通过 `get_emoji_list` 或 `get_all_emoji` 查询。 |
| business | str | 使用场景, reply / dynamic |

**Returns:** dict: 调用 API 返回的结果




---

## async def get_emoji_list()

获取表情包列表


| name | type | description |
| - | - | - |
| business | str | 使用场景, reply / dynamic |
| credential | Credential | 登录凭证. Defaults to None. |

**Returns:** dict: 调用 API 返回的结果




