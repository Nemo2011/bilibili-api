# Module manga.py


bilibili_api.manga

漫画相关操作


``` python
from bilibili_api import manga
```

- [class Manga()](#class-Manga)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def get\_manga\_id()](#def-get\_manga\_id)
- [class MangaIndexFilter()](#class-MangaIndexFilter)
  - [class Area()](#class-Area)
  - [class Order()](#class-Order)
  - [class Payment()](#class-Payment)
  - [class Status()](#class-Status)
  - [class Style()](#class-Style)
- [class MangaOrderType()](#class-MangaOrderType)
- [async def get\_followed\_manga()](#async-def-get\_followed\_manga)
- [async def get\_manga\_home\_recommend()](#async-def-get\_manga\_home\_recommend)
- [async def get\_manga\_update()](#async-def-get\_manga\_update)
- [async def set\_follow\_manga()](#async-def-set\_follow\_manga)

---

## class Manga()

漫画类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类。 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `manga_id` | `int` | 漫画 id |
| `credential` | `Credential \| None` | 凭据类. Defaults to None. |


### def get_manga_id()

获取漫画的 id



**Returns:** `int`:  漫画的 id




---

## class MangaIndexFilter()

漫画索引筛选器类。




### class Area()

**Extend: enum.Enum**

漫画索引筛选器的地区枚举类。

- ALL: 全部
- CHINA: 大陆
- JAPAN: 日本
- SOUTHKOREA: 韩国
- OTHER: 其他




### class Order()

**Extend: enum.Enum**

漫画索引筛选器的排序枚举类。

- HOT: 人气推荐
- UPDATE: 更新时间
- RELEASE_DATE: 上架时间




### class Payment()

**Extend: enum.Enum**

漫画索引筛选器的付费枚举类。

- ALL: 全部
- FREE: 免费
- PAID: 付费
- WILL_BE_FREE: 等就免费




### class Status()

**Extend: enum.Enum**

漫画索引筛选器的状态枚举类。

- ALL: 全部
- FINISHED: 完结
- UNFINISHED: 连载




### class Style()

**Extend: enum.Enum**

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




---

## class MangaOrderType()

**Extend: enum.Enum**

漫画排序方式

- FOLLOW: 追漫顺序
- UPDATE: 更新时间
- READING: 最近阅读
- FREE: 等免




---

## async def get_followed_manga()

获取追漫列表


| name | type | description |
| - | - | - |
| `pn` | `int` | 页码。Defaults to 1. |
| `ps` | `int` | 每页数量。Defaults to 18. |
| `order` | `MangaOrderType` | 排序方式。Defaults to MangaOrderType.FOLLOW. |
| `credential` | `Credential` | 凭据类. |

**Returns:** `List[Manga]`:  追漫列表




---

## async def get_manga_home_recommend()

获取首页推荐的漫画


| name | type | description |
| - | - | - |
| `pn` | `int` | 页码。Defaults to 1. |
| `seed` | `Optional, str` | Unknown param，无需传入. |
| `credential` | `Credential` | 凭据类. Defaults to None. |

**Returns:** `List[Manga]`:  漫画列表




---

## async def get_manga_update()

获取更新推荐的漫画


| name | type | description |
| - | - | - |
| `date` | `Union[str, datetime.datetime]` | 日期，默认为今日。 |
| `pn` | `int` | 页码。Defaults to 1. |
| `ps` | `int` | 每页数量。Defaults to 8. |
| `credential` | `Credential` | 凭据类. Defaults to None. |

**Returns:** `List[Manga]`:  漫画列表




---

## async def set_follow_manga()

设置追漫


| name | type | description |
| - | - | - |
| `manga` | `Manga` | 漫画类。 |
| `status` | `bool` | 设置是否追漫。是为 True，否为 False。Defaults to True. |
| `credential` | `Credential` | 凭据类。 |




