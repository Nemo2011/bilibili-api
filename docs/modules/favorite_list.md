# Module favorite_list.py

```python
from bilibili_api import favorite_list
```

收藏夹操作。

## class FavoriteListContentOrder

**Extends:** enum.Enum

收藏夹列表内容排序方式枚举。

+ MTIME  : 最近收藏
+ VIEW   : 最多播放
+ PUBTIME: 最新投稿


## class FavoriteListType

**Extends:** enum.Enum

收藏夹类型枚举

+ VIDEO  : 视频收藏夹
+ ARTICLE: 专栏收藏夹
+ CHEESE : 课程收藏夹
---

## class SearchFavoriteListMode

**Extends:** enum.Enum

收藏夹搜索模式枚举

+ ONLY : 仅当前收藏夹
+ ALL  : 该用户所有收藏夹

---
## class FavoriteList

收藏夹类

### Attributes

| name | type | description |
| ---- | ---- | ----------- |
| credential | Credential | 凭据 |

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| media_id   | int \| None                                | 收藏夹 ID                                             |
| credential | Credential \| None, optional               | 凭据. Defaults to None.                               |

---

#### def is_video_favorite_list()

收藏夹是否为视频收藏夹

**Returns:** bool: 是否为视频收藏夹

---

#### def get_favorite_list_type()

获取收藏夹类型

**Returns:** FavoriteListType: 收藏夹类型

---

#### def get_media_id()

获取收藏夹 id

**Returns:** int: 收藏夹 id

---
#### def get_info()

获取收藏夹信息

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_content_video()

| name       | type                               | description                                           |
| ---------- | ---------------------------------- | :---------------------------------------------------- |
| page       | int, optional                      | 页码. Defaults to 1.                                  |
| keyword    | str \| None, optional                      | 搜索关键词. Defaults to None.                         |
| order      | FavoriteListContentOrder, optional | 排序方式. Defaults to FavoriteListContentOrder.MTIME. |
| tid        | int, optional                      | 分区 ID. Defaults to 0.                               |

获取视频收藏夹内容。

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_content()

| name       | type                               | description                                           |
| ---------- | ---------------------------------- | :---------------------------------------------------- |
| page       | int, optional                      | 页码. Defaults to 1.                                  |

获取收藏夹内容。

**Returns:** dict: 调用 API 返回的结果

---

#### async def get_content_ids_info()

获取收藏夹所有内容的 ID。

**Returns:** dict: 收藏夹所有内容的 ID 信息

---

## async def get_video_favorite_list()

| name       | type                 | description                                                  |
| ---------- | -------------------- | ------------------------------------------------------------ |
| uid        | int                  | 用户 UID                                                     |
| video      | video.Video \| None, optional          | 视频类。若提供该参数则结果会附带该收藏夹是否存在该视频。Defaults to None. |
| credential | Credential \| None, optional | 凭据. Defaults to None.                                      |

获取视频收藏夹列表。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_video_favorite_list_content()

| name       | type                               | description                                           |
| ---------- | ---------------------------------- | :---------------------------------------------------- |
| media_id   | int                                | 收藏夹 ID                                              |
| page       | int, optional                      | 页码. Defaults to 1.                                   |
| keyword    | str \| None, optional              | 搜索关键词. Defaults to None.                           |
| order      | FavoriteListContentOrder, optional | 排序方式. Defaults to FavoriteListContentOrder.MTIME.  |
| tid        | int, optional                      | 分区 ID. Defaults to 0.                               |
| mode       | SearchFavoriteListMode, optional   | 搜索模式，默认仅当前收藏夹.                               |
| credential | Credential \| None, optional        | 凭据. Defaults to None.                              |

获取视频收藏夹列表内容，也可用于搜索收藏夹内容。

mode 参数见 SearchFavoriteListMode 枚举。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_topic_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| page       | int, optional        | 页码. Defaults to 1.    |
| credential | Credential \| None, optional | 凭据. Defaults to None. |

获取自己的话题收藏夹内容。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_article_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| page       | int, optional        | 页码. Defaults to 1.    |
| credential | Credential \| None, optional | 凭据. Defaults to None. |

获取自己的专栏收藏夹内容。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_album_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| page       | int, optional        | 页码. Defaults to 1.    |
| credential | Credential \| None, optional | 凭据. Defaults to None. |

获取自己的相簿收藏夹内容。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_course_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| page       | int, optional        | 页码. Defaults to 1.    |
| credential | Credential \| None, optional | 凭据. Defaults to None. |

获取自己的课程收藏夹内容。

**Returns:** dict: 调用 API 返回的结果

---

## async def get_note_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| page       | int, optional        | 页码. Defaults to 1.    |
| credential | Credential \| None, optional | 凭据. Defaults to None. |

获取自己的笔记收藏夹内容。

**Returns:** dict: 调用 API 返回的结果

---

## async def create_video_favorite_list()

| name         | type                 | description                    |
| ------------ | -------------------- | :----------------------------- |
| title        | str                  | 收藏夹名                       |
| introduction | str, optional        | 收藏夹简介. Defaults to ''.    |
| private      | bool, optional       | 是否为私有. Defaults to False. |
| credential   | Credential \| None, optional | 凭据. Defaults to None.        |

新建视频收藏夹列表。

**Returns:** dict: 调用 API 返回的结果

## async def modify_video_favorite_list()

| name         | type                 | description                    |
| ------------ | -------------------- | :----------------------------- |
| media_id     | int                  | 收藏夹 ID.                     |
| title        | str                  | 收藏夹名                       |
| introduction | str, optional        | 收藏夹简介. Defaults to ''.    |
| private      | bool, optional       | 是否为私有. Defaults to False. |
| credential   | Credential \| None, optional | 凭据. Defaults to None.        |

修改视频收藏夹信息。

**Returns:** dict: 调用 API 返回的结果

## async def delete_video_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| media_ids  | List[int]            | 收藏夹 ID 列表。        |
| credential | Credential, optional | 凭据. Defaults to None. |

删除视频收藏夹，可批量删除。

**Returns:** dict: 调用 API 返回的结果

## async def copy_video_favorite_list_content()

| name          | type       | description            |
| ------------- | ---------- | :--------------------- |
| media_id_from | int        | 要复制的源收藏夹 ID。  |
| media_id_to   | int        | 目标收藏夹 ID。        |
| aids          | List[int]  | 被复制的视频 ID 列表。 |
| credential    | Credential | 凭据                   |

复制视频收藏夹内容

**Returns:** dict: 调用 API 返回的结果

## async def move_video_favorite_list_content()

| name          | type       | description            |
| ------------- | ---------- | :--------------------- |
| media_id_from | int        | 要移动的源收藏夹 ID。  |
| media_id_to   | int        | 目标收藏夹 ID。        |
| aids          | List[int]  | 被移动的视频 ID 列表。 |
| credential    | Credential | 凭据                   |

移动视频收藏夹内容

**Returns:** dict: 调用 API 返回的结果

## async def delete_video_favorite_list_content()

| name       | type       | description            |
| ---------- | ---------- | :--------------------- |
| media_id   | int        | 收藏夹 ID。            |
| aids       | List[int]  | 被删除的视频 ID 列表。 |
| credential | Credential | 凭据                   |

删除视频收藏夹内容

**Returns:** dict: 调用 API 返回的结果

## async def clean_video_favorite_list_content()

| name       | type       | description |
| ---------- | ---------- | :---------- |
| media_id   | int        | 收藏夹 ID。 |
| credential | Credential | 凭据        |

清除视频收藏夹失效内容

**Returns:** dict: 调用 API 返回的结果
