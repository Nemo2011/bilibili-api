# Module manga.py

```python
from bilibili_api import manga
```

## class Manga

漫画类

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据类 |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| ---- | ---- | ----------- |
| manga_id | int | 漫画 id   |
| credential | Credential \| None | 凭据类. Defaults to None. |

#### async def get_info()

获取漫画信息

**Returns:** dict: 调用 API 返回的结果

#### async def get_episode_info()

获取某一话的详细信息

| name | type | description |
| ---- | ---- | ----------- |
| episode_count | int \| float \| None | 第几话. |
| episode_id    | int \| None          | 对应的话的 id. 可以通过 `get_episode_id` 获取。 |

**注意：episode_count 和 episode_id 中必须提供一个参数。**

**Returns:** dict: 对应的话的详细信息

#### async def get_episode_id()

获取某一话的 id

| name | type | description |
| ---- | ---- | ----------- |
| episode_count | int \| float \| None | 第几话. |

**Returns:** int: 对应的话的 id

#### async def get_images_url()

获取某一话的图片链接。(未经过处理，所有的链接无法直接访问)

获取的图片 url 请传入 `manga.manga_image_turn_to_Picture` 函数以转换为 `Picture` 类。

| name | type | description |
| ---- | ---- | ----------- |
| episode_count | int \| float \| None | 第几话. |
| episode_id    | int \| None          | 对应的话的 id. 可以通过 `get_episode_id` 获取。 |

**注意：episode_count 和 episode_id 中必须提供一个参数。**

**Returns:** dict: 调用 API 返回的结果

#### async def get_images()

获取某一话的所有图片

| name | type | description |
| ---- | ---- | ----------- |
| episode_count | int \| float \| None | 第几话. |
| episode_id    | int \| None          | 对应的话的 id. 可以通过 `get_episode_id` 获取。 |

**注意：episode_count 和 episode_id 中必须提供一个参数。**

**Returns:** List[Dict]: 返回一个列表，每一项为字典，字典有三个键值：`picture: Picture`, `x: int`, `y: int`

---

## async def manga_image_turn_to_Picture()

将 Manga.get_images_url 函数获得的图片 url 转换为 Picture 类。

| name | type | description |
| ---- | ---- | ----------- |
| url  | str  | 未经处理的漫画图片链接。 |
| credential | Credential \| None | 凭据类. Defaults to None. |

**Returns:** Picture: 图片类。
