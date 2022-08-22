# Module favorite_list.ts(favorite_list.js)

```typescript
import {} from "bilibili-api-ts/favorite_list";
```

收藏夹操作。

## enum FavoriteListContentOrder

收藏夹列表内容排序方式枚举。

+ MTIME  : 最近收藏
+ VIEW   : 最多播放
+ PUBTIME: 最新投稿


## async function get_video_favorite_list()

| name       | type                 | description                                                  |
| ---------- | -------------------- | ------------------------------------------------------------ |
| uid        | int                  | 用户 UID                                                     |
| video      | video.Video          | 视频类。若提供该参数则结果会附带该收藏夹是否存在该视频。Defaults to None. |
| credential | Credential, optional | 凭据. Defaults to None.                                      |

获取视频收藏夹列表。

**Returns:** API 调用返回结果

---

## async function get_video_favorite_list_content()

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
