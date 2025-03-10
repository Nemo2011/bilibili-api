# Module favorite_list.py


bilibili_api.favorite_list

收藏夹操作。


``` python
from bilibili_api import favorite_list
```

- [class FavoriteList()](#class-FavoriteList)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_content()](#async-def-get\_content)
  - [async def get\_content\_ids\_info()](#async-def-get\_content\_ids\_info)
  - [async def get\_content\_video()](#async-def-get\_content\_video)
  - [def get\_favorite\_list\_type()](#def-get\_favorite\_list\_type)
  - [async def get\_info()](#async-def-get\_info)
  - [def get\_media\_id()](#def-get\_media\_id)
  - [def is\_video\_favorite\_list()](#def-is\_video\_favorite\_list)
- [class FavoriteListContentOrder()](#class-FavoriteListContentOrder)
- [class FavoriteListType()](#class-FavoriteListType)
- [class SearchFavoriteListMode()](#class-SearchFavoriteListMode)
- [async def clean\_video\_favorite\_list\_content()](#async-def-clean\_video\_favorite\_list\_content)
- [async def copy\_video\_favorite\_list\_content()](#async-def-copy\_video\_favorite\_list\_content)
- [async def create\_video\_favorite\_list()](#async-def-create\_video\_favorite\_list)
- [async def delete\_video\_favorite\_list()](#async-def-delete\_video\_favorite\_list)
- [async def delete\_video\_favorite\_list\_content()](#async-def-delete\_video\_favorite\_list\_content)
- [async def get\_article\_favorite\_list()](#async-def-get\_article\_favorite\_list)
- [async def get\_course\_favorite\_list()](#async-def-get\_course\_favorite\_list)
- [async def get\_favorite\_collected()](#async-def-get\_favorite\_collected)
- [async def get\_note\_favorite\_list()](#async-def-get\_note\_favorite\_list)
- [async def get\_topic\_favorite\_list()](#async-def-get\_topic\_favorite\_list)
- [async def get\_video\_favorite\_list()](#async-def-get\_video\_favorite\_list)
- [async def get\_video\_favorite\_list\_content()](#async-def-get\_video\_favorite\_list\_content)
- [async def modify\_video\_favorite\_list()](#async-def-modify\_video\_favorite\_list)
- [async def move\_video\_favorite\_list\_content()](#async-def-move\_video\_favorite\_list\_content)

---

## class FavoriteList()

收藏夹类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `type_` | `FavoriteListType, optional` | 收藏夹类型. Defaults to FavoriteListType.VIDEO. |
| `media_id` | `int, optional` | 收藏夹号（仅为视频收藏夹时提供）. Defaults to None. |
| `credential` | `Credential, optional` | 凭据类. Defaults to Credential(). |


### async def get_content()

获取收藏夹内容。


| name | type | description |
| - | - | - |
| `page` | `int, optional` | 页码. Defaults to 1. |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_content_ids_info()

获取收藏夹所有内容的 ID。

**注意：接口针对番剧剧集视频返回的 id / bvid 实际上对应的是其 epid**



**Returns:** `dict`:  调用 API 返回的结果




### async def get_content_video()

获取视频收藏夹内容。


| name | type | description |
| - | - | - |
| `page` | `int, optional` | 页码. Defaults to 1. |
| `keyword` | `str \| None, optional` | 搜索关键词. Defaults to None. |
| `order` | `FavoriteListContentOrder, optional` | 排序方式. Defaults to FavoriteListContentOrder.MTIME. |
| `mode` | `SearchFavoriteListMode, optional` | 搜索模式，默认仅当前收藏夹. |
| `tid` | `int, optional` | 分区 ID. Defaults to 0. |

**Returns:** `dict`:  调用 API 返回的结果




### def get_favorite_list_type()

获取收藏夹类型



**Returns:** `FavoriteListType`:  收藏夹类型




### async def get_info()

获取收藏夹信息。



**Returns:** `dict`:  调用 API 返回的结果




### def get_media_id()

获取收藏夹 media_id，仅视频收藏夹存在此属性



**Returns:** `Union[int, None]`:  media_id




### def is_video_favorite_list()

收藏夹是否为视频收藏夹



**Returns:** `bool`:  是否为视频收藏夹




---

## class FavoriteListContentOrder()

**Extend: enum.Enum**

收藏夹列表内容排序方式枚举。

+ MTIME  : 最近收藏
+ VIEW   : 最多播放
+ PUBTIME: 最新投稿




---

## class FavoriteListType()

**Extend: enum.Enum**

收藏夹类型枚举

+ VIDEO  : 视频收藏夹
+ ARTICLE: 专栏收藏夹
+ CHEESE : 课程收藏夹




---

## class SearchFavoriteListMode()

**Extend: enum.Enum**

收藏夹搜索模式枚举

+ ONLY : 仅当前收藏夹
+ ALL  : 该用户所有收藏夹




---

## async def clean_video_favorite_list_content()

清除视频收藏夹失效内容


| name | type | description |
| - | - | - |
| `media_id` | `int` | 收藏夹 ID |
| `credential` | `Credential` | 凭据 |

**Returns:** `dict`:  API 调用结果。




---

## async def copy_video_favorite_list_content()

复制视频收藏夹内容


| name | type | description |
| - | - | - |
| `media_id_from` | `int` | 要复制的源收藏夹 ID。 |
| `media_id_to` | `int` | 目标收藏夹 ID。 |
| `aids` | `List[int]` | 被复制的视频 ID 列表。 |
| `credential` | `Credential` | 凭据 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def create_video_favorite_list()

新建视频收藏夹列表。


| name | type | description |
| - | - | - |
| `title` | `str` | 收藏夹名。 |
| `introduction` | `str, optional` | 收藏夹简介. Defaults to ''. |
| `private` | `bool, optional` | 是否为私有. Defaults to False. |
| `credential` | `Credential, optional` | 凭据. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def delete_video_favorite_list()

删除视频收藏夹，可批量删除。


| name | type | description |
| - | - | - |
| `media_ids` | `List[int]` | 收藏夹 ID 列表。 |
| `credential` | `Credential` | Credential. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def delete_video_favorite_list_content()

删除视频收藏夹内容


| name | type | description |
| - | - | - |
| `media_id` | `int` | 收藏夹 ID。 |
| `aids` | `List[int]` | 被删除的视频 ID 列表。 |
| `credential` | `Credential` | 凭据 |

**Returns:** `dict`:  API 调用结果。




---

## async def get_article_favorite_list()

获取自己的专栏收藏夹内容。


| name | type | description |
| - | - | - |
| `page` | `int, optional` | 页码. Defaults to 1. |
| `credential` | `Credential \| None, optional` | Credential. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_course_favorite_list()

获取自己的课程收藏夹内容。


| name | type | description |
| - | - | - |
| `page` | `int, optional` | 页码. Defaults to 1. |
| `credential` | `Credential \| None, optional` | Credential. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_favorite_collected()

获取收藏合集列表


| name | type | description |
| - | - | - |
| `uid` | `int` | 用户 UID。 |
| `pn` | `int, optional` | 页码. Defaults to 1. |
| `ps` | `int, optional` | 每页数据大小. Defaults to 20. |
| `credential` | `Credential \| None, optional` | Credential. Defaults to None. |




---

## async def get_note_favorite_list()

获取自己的笔记收藏夹内容。


| name | type | description |
| - | - | - |
| `page` | `int, optional` | 页码. Defaults to 1. |
| `credential` | `Credential \| None, optional` | Credential. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_topic_favorite_list()

获取自己的话题收藏夹内容。


| name | type | description |
| - | - | - |
| `page` | `int, optional` | 页码. Defaults to 1. |
| `credential` | `Credential \| None, optional` | Credential |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_video_favorite_list()

获取视频收藏夹列表。


| name | type | description |
| - | - | - |
| `uid` | `int` | 用户 UID。 |
| `video` | `Video \| None, optional` | 视频类。若提供该参数则结果会附带该收藏夹是否存在该视频。Defaults to None. |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_video_favorite_list_content()

获取视频收藏夹列表内容，也可用于搜索收藏夹内容。

mode 参数见 SearchFavoriteListMode 枚举。


| name | type | description |
| - | - | - |
| `media_id` | `int` | 收藏夹 ID。 |
| `page` | `int, optional` | 页码. Defaults to 1. |
| `keyword` | `str, optional` | 搜索关键词. Defaults to None. |
| `order` | `FavoriteListContentOrder, optional` | 排序方式. Defaults to FavoriteListContentOrder.MTIME. |
| `tid` | `int, optional` | 分区 ID. Defaults to 0. |
| `mode` | `SearchFavoriteListMode, optional` | 搜索模式，默认仅当前收藏夹. |
| `credential` | `Credential, optional` | Credential. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def modify_video_favorite_list()

修改视频收藏夹信息。


| name | type | description |
| - | - | - |
| `media_id` | `int` | 收藏夹 ID. |
| `title` | `str` | 收藏夹名。 |
| `introduction` | `str, optional` | 收藏夹简介. Defaults to ''. |
| `private` | `bool, optional` | 是否为私有. Defaults to False. |
| `credential` | `Credential, optional` | Credential. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def move_video_favorite_list_content()

移动视频收藏夹内容


| name | type | description |
| - | - | - |
| `media_id_from` | `int` | 要移动的源收藏夹 ID。 |
| `media_id_to` | `int` | 目标收藏夹 ID。 |
| `aids` | `List[int]` | 被移动的视频 ID 列表。 |
| `credential` | `Credential` | 凭据 |

**Returns:** `dict`:  调用 API 返回的结果




