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

---

## class VideoFavoriteList

一个简单的视频收藏夹类。

### Functions

#### def \_\_init\_\_()

| name | type | description |
| - | - | - |
| media_id   | int                                | 收藏夹 ID                                             |
| credential | Credential, optional               | 凭据. Defaults to None.                               |

#### _async_ def get_meta()

| name       | type                               | description                                           |
| ---------- | ---------------------------------- | :---------------------------------------------------- |
| page       | int, optional                      | 页码. Defaults to 1.                                  |
| keyword    | str, optional                      | 搜索关键词. Defaults to None.                         |
| order      | FavoriteListContentOrder, optional | 排序方式. Defaults to FavoriteListContentOrder.MTIME. |
| tid        | int, optional                      | 分区 ID. Defaults to 0.                               |

获取视频收藏夹列表元数据。

**Returns:** API 调用返回结果

---

## _async_ def get_video_favorite_list()

| name       | type                 | description                                                  |
| ---------- | -------------------- | ------------------------------------------------------------ |
| uid        | int                  | 用户 UID                                                     |
| video      | video.Video          | 视频类。若提供该参数则结果会附带该收藏夹是否存在该视频。Defaults to None. |
| credential | Credential, optional | 凭据. Defaults to None.                                      |

获取视频收藏夹列表。

**Returns:** API 调用返回结果

---

## _async_ def get_video_favorite_list_content()

| name       | type                               | description                                           |
| ---------- | ---------------------------------- | :---------------------------------------------------- |
| media_id   | int                                | 收藏夹 ID                                             |
| page       | int, optional                      | 页码. Defaults to 1.                                  |
| keyword    | str, optional                      | 搜索关键词. Defaults to None.                         |
| order      | FavoriteListContentOrder, optional | 排序方式. Defaults to FavoriteListContentOrder.MTIME. |
| tid        | int, optional                      | 分区 ID. Defaults to 0.                               |
| credential | Credential, optional               | 凭据. Defaults to None.                               |

获取视频收藏夹列表内容。

**Returns:** API 调用返回结果

---

## _async_ def get_topic_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| page       | int, optional        | 页码. Defaults to 1.    |
| credential | Credential, optional | 凭据. Defaults to None. |

获取自己的话题收藏夹内容。

**Returns:** API 调用返回结果

---

## _async_ def get_article_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| page       | int, optional        | 页码. Defaults to 1.    |
| credential | Credential, optional | 凭据. Defaults to None. |

获取自己的专栏收藏夹内容。

**Returns:** API 调用返回结果

---

## _async_ def get_album_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| page       | int, optional        | 页码. Defaults to 1.    |
| credential | Credential, optional | 凭据. Defaults to None. |

获取自己的相簿收藏夹内容。

**Returns:** API 调用返回结果

---

## _async_ def get_course_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| page       | int, optional        | 页码. Defaults to 1.    |
| credential | Credential, optional | 凭据. Defaults to None. |

获取自己的课程收藏夹内容。

**Returns:** API 调用返回结果

---

## _async_ def get_note_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| page       | int, optional        | 页码. Defaults to 1.    |
| credential | Credential, optional | 凭据. Defaults to None. |

获取自己的笔记收藏夹内容。

**Returns:** API 调用返回结果

---

## _async_ def create_video_favorite_list()

| name         | type                 | description                    |
| ------------ | -------------------- | :----------------------------- |
| title        | str                  | 收藏夹名                       |
| introduction | str, optional        | 收藏夹简介. Defaults to ''.    |
| private      | bool, optional       | 是否为私有. Defaults to False. |
| credential   | Credential, optional | 凭据. Defaults to None.        |

新建视频收藏夹列表。

**Returns:** API 调用返回结果

## _async_ def modify_video_favorite_list()

| name         | type                 | description                    |
| ------------ | -------------------- | :----------------------------- |
| media_id     | int                  | 收藏夹 ID.                     |
| title        | str                  | 收藏夹名                       |
| introduction | str, optional        | 收藏夹简介. Defaults to ''.    |
| private      | bool, optional       | 是否为私有. Defaults to False. |
| credential   | Credential, optional | 凭据. Defaults to None.        |

修改视频收藏夹信息。

**Returns:** API 调用返回结果

## _async_ def delete_video_favorite_list()

| name       | type                 | description             |
| ---------- | -------------------- | :---------------------- |
| media_ids  | List[int]            | 收藏夹 ID 列表。        |
| credential | Credential, optional | 凭据. Defaults to None. |

删除视频收藏夹，可批量删除。

**Returns:** API 调用返回结果

## _async_ def copy_video_favorite_list_content()

| name          | type       | description            |
| ------------- | ---------- | :--------------------- |
| media_id_from | int        | 要复制的源收藏夹 ID。  |
| media_id_to   | int        | 目标收藏夹 ID。        |
| aids          | List[int]  | 被复制的视频 ID 列表。 |
| credential    | Credential | 凭据                   |

复制视频收藏夹内容

**Returns:** API 调用返回结果

## _async_ def move_video_favorite_list_content()

| name          | type       | description            |
| ------------- | ---------- | :--------------------- |
| media_id_from | int        | 要移动的源收藏夹 ID。  |
| media_id_to   | int        | 目标收藏夹 ID。        |
| aids          | List[int]  | 被移动的视频 ID 列表。 |
| credential    | Credential | 凭据                   |

移动视频收藏夹内容

**Returns:** API 调用返回结果

## _async_ def delete_video_favorite_list_content()

| name       | type       | description            |
| ---------- | ---------- | :--------------------- |
| media_id   | int        | 收藏夹 ID。            |
| aids       | List[int]  | 被删除的视频 ID 列表。 |
| credential | Credential | 凭据                   |

删除视频收藏夹内容

**Returns:** API 调用返回结果

## _async_ def clean_video_favorite_list_content()

| name       | type       | description |
| ---------- | ---------- | :---------- |
| media_id   | int        | 收藏夹 ID。 |
| credential | Credential | 凭据        |

清除视频收藏夹失效内容

**Returns:** API 调用返回结果