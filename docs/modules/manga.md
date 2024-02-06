# Module manga.py

```python
from bilibili_api import manga
```
## class MangaIndexFilter

漫画索引筛选器

### class Area

**Extends:** enum.Enum

漫画索引筛选器的地区枚举类。

- ALL: 全部
- CHINA: 大陆
- JAPAN: 日本
- SOUTHKOREA: 韩国
- OTHER: 其他

### class Order

**Extends:** enum.Enum

漫画索引筛选器的排序枚举类。

- HOT: 人气推荐
- UPDATE: 更新时间
- RELEASE_DATE: 上架时间

### class Status

**Extends:** enum.Enum

漫画索引筛选器的状态枚举类。

- ALL: 全部
- FINISHED: 完结
- UNFINISHED: 连载

### class Payment

**Extends:** enum.Enum

漫画索引筛选器的付费枚举类。

- ALL: 全部
- FREE: 免费
- PAID: 付费
- WILL_BE_FREE: 等就免费

### class Style

**Extends:** enum.Enum

漫画索引筛选器的风格枚举类。

- ALL: 全部
- WARM: 热血
- ANCIENT: 古风
- FANTASY: 玄幻
- IMAGING: 奇幻
- SUSPENSE: 悬疑
- CITY: 都市
- HISTORY: 历史
- WUXIA: 武侠仙侠
- GAME: 游戏竞技
- PARANORMAL: 悬疑灵异
- ALTERNATE: 架空
- YOUTH: 青春
- WEST_MAGIC: 西幻
- MORDEN: 现代
- POSITIVE: 正能量
- SCIENCE_FICTION: 科幻

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

#### def get_manga_id()

获取漫画 id

**Returns:** int: 漫画 id

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

获取的图片 url 请传入 `manga.manga_image_url_turn_to_Picture` 函数以转换为 `Picture` 类。

| name | type | description |
| ---- | ---- | ----------- |
| episode_count | int \| float \| None | 第几话. |
| episode_id    | int \| None          | 对应的话的 id. 可以通过 `get_episode_id` 获取。 |

**注意：episode_count 和 episode_id 中必须提供一个参数。**

**Returns:** dict: 调用 API 返回的结果

#### async def get_images()

获取某一话的所有图片 (速度根据漫画章节图片数量而定)

| name | type | description |
| ---- | ---- | ----------- |
| episode_count | int \| float \| None | 第几话. |
| episode_id    | int \| None          | 对应的话的 id. 可以通过 `get_episode_id` 获取。 |

**注意：episode_count 和 episode_id 中必须提供一个参数。**

**Returns:** List[Picture] 所有图片

---

## async def manga_image_url_turn_to_Picture()

将 Manga.get_images_url 函数获得的图片 url 转换为 Picture 类。

| name | type | description |
| ---- | ---- | ----------- |
| url  | str  | 未经处理的漫画图片链接。 |
| credential | Credential \| None | 凭据类. Defaults to None. |

**Returns:** Picture: 图片类。

---

## async def set_follow_manga()

设置追漫

| name | type | description |
| - | - | - |
| manga | Manga | 漫画类。 |
| status | bool | 设置是否追漫。是为 True，否为 False。Defaults to True. |
| credential | Credential | 凭据类。 |

**Returns:** dict: 调用 API 返回的结果

## async def get_raw_manga_index()

获取漫画索引原始数据

| name | type | description |
| - | - | - |
| area | MangaIndexFilter.Area | 地区。Defaults to MangaIndexFilter.Area.ALL. |
| status | MangaIndexFilter.Status | 状态。Defaults to MangaIndexFilter.Status.ALL. |
| payment | MangaIndexFilter.Payment | 付费。Defaults to MangaIndexFilter.Payment.ALL. |
| order | MangaIndexFilter.Order | 排序。Defaults to MangaIndexFilter.Order.HOT. |
| style | MangaIndexFilter.Style | 风格。Defaults to MangaIndexFilter.Style.ALL. |
| pn | int | 页数。Defaults to 1. |
| ps | int | 每页数量。Defaults to 18. |
| credential | Credential \| None | 凭据类. Defaults to None. |

**Returns:** dict: 调用 API 返回的结果

## async def get_manga_index()

获取漫画索引

| name | type | description |
| - | - | - |
| area | MangaIndexFilter.Area | 地区。Defaults to MangaIndexFilter.Area.ALL. |
| status | MangaIndexFilter.Status | 状态。Defaults to MangaIndexFilter.Status.ALL. |
| payment | MangaIndexFilter.Payment | 付费。Defaults to MangaIndexFilter.Payment.ALL. |
| order | MangaIndexFilter.Order | 排序。Defaults to MangaIndexFilter.Order.HOT. |
| style | MangaIndexFilter.Style | 风格。Defaults to MangaIndexFilter.Style.ALL. |
| pn | int | 页数。Defaults to 1. |
| ps | int | 每页数量。Defaults to 18. |
| credential | Credential \| None | 凭据类. Defaults to None. |

**Returns:** List[Manga]: 漫画索引

## async def get_manga_update()

获取漫画更新推荐

| name | type | description |
| - | - | - |
| date | str, datetime.datetime | 日期，默认为今日。|
| pn | int | 页数。Defaults to 1. |
| ps | int | 每页数量。Defaults to 8. |
| credential | Credential \| None | 凭据类. Defaults to None. |

**Returns:** dict: 调用 API 返回的结果

## async def get_manga_home_recommend()

获取漫画首页推荐

| name | type | description |
| - | - | - |
| pn | int | 页数。Defaults to 1. |
| seed | str, optional | Unknown param，无需传入 |
| credential | Credential \| None | 凭据类. Defaults to None. |
