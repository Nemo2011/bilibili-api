# Module album.py

``` python
from bilibili_api import album
```

## class AlbumCategory 

**Extends: enum.Enum**

相簿分区枚举。

- ALL: 全部
- PAINTS: 画友
- PHOTOS: 摄影

---

## class AlbumOrder

**Extends: enum.Enum**

相簿排序顺序枚举。

- RECOMMEND: 推荐
- HOT: 最火（并非所有函数的所有分区均对此项支持）
- NEW: 最新（并非所有函数的所有分区均对此项支持）

---

## class Album

### Attributes

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| doc_id | int | 相簿 ID。如 https://h.bilibili.com/1919 的 doc_id 为 1919 |
| credential | Credential | 凭据类 |

#### def get_doc_id()

获取相簿 ID

**Returns:** int: 相簿 id

#### async def get_info()

获取相簿完整信息

**Returns:** dict: 相簿信息

#### async def get_author()

获取相簿作者信息

**Returns:** dict: 相簿作者信息

#### async def get_pictures()

获取相簿中的图片

**Returns:** List[Picture]: 相簿中的图片

---

## async def get_homepage_albums_list()

| name | type | description |
| - | - | - |
| category | AlbumCategory | 分区. Defaults to AlbumCategory.ALL |
| order | AlbumOrder | 排序方式. Defaults to AlbumOrder.RECOMMEND |
| page_num | int | 第几页. Defaults to 1. |
| page_size | int | 每一页的数据大小. Defaults to 45. |
| credential | Optional[Credential] | 凭据类. Defaults to None. |

获取相簿列表。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_homepage_recommend_uppers()

| name | type | description |
| - | - | - |
| category | AlbumCategory | 分区. Defaults to AlbumCategory.ALL |
| numbers | int | 获取数据的大小. Defaults to 6. (分区为全部时此参数必须为偶数。) |
| credential | Optional[Credential] | 凭据类. Defaults to None. |

获取首页推荐相簿 up 主。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_user_albums()

| name | type | description |
| - | - | - |
| uid | int | 用户 uid |
| category | AlbumCategory | 分区. Defaults to AlbumCategory.ALL |
| page_num | int | 第几页. Defaults to 1. |
| page_size | int | 每一页的数据大小. Defaults to 45. |
| credential | Optional[Credential] | 凭据类. Defaults to None. |

获取指定用户的相簿列表。

**Returns:** dict: 调用 API 返回的结果
