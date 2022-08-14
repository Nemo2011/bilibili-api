# Module user.ts(user.js)

```typescript
import {} from "bilibili-api-ts/user"
```

用户相关。

## enum VideoOrder

视频排序顺序。

+ PUBDATE : 上传日期倒序。
+ FAVORITE: 收藏量倒序。
+ VIEW  : 播放量倒序。

---

## class User

### Functions

#### _constructor_

| name       | type                 | description |
| ---------- | -------------------- | ----------- |
| uid        | int                  | 用户 UID    |
| credential | Credential | 凭据        |

#### async function get_user_info()

获取用户信息（昵称，性别，生日，签名，头像URL，空间横幅URL等）

**Returns:** 调用接口返回的内容。

#### async function get_relation_info()

获取用户关系信息（关注数，粉丝数，悄悄关注，黑名单数）

**Returns:** 调用接口返回的内容。

#### async function get_up_stat()

获取 UP 主数据信息（视频总播放量，文章总阅读量，总点赞数）

**Returns:** 调用接口返回的内容。

#### async function get_live_info()

获取用户直播间信息。

**Returns:** 调用接口返回的内容。

#### async function get_videos()

| name    | type                 | description                              |
| ------- | -------------------- | ---------------------------------------- |
| tid     | int, optional        | 分区 ID. Defaults to 0（全部）           |
| pn      | int, optional        | 页码，从 1 开始. Defaults to 1.          |
| ps      |(int, optional)       | 每一页的视频数. Defaults to 30. |
| keyword | str, optional        | 搜索关键词. Defaults to "".              |
| order   | VideoOrder, optional | 排序方式. Defaults to VideoOrder.PUBDATE |

获取用户投稿视频信息。

**Returns:** 调用接口返回的内容。

#### async function get_audios()

| name  | type                 | description                               |
| ----- | -------------------- | ----------------------------------------- |
| order | AudioOrder, optional | 排序方式. Defaults to AudioOrder.PUBDATE. |
| pn    | int, optional        | 页码，从 1 开始. Defaults to 1.           |
| ps     | (int, optional)       | 每一页的视频数. Defaults to 30. |

获取用户投稿音频。

**Returns:** 调用接口返回的内容。
