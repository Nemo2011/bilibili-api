# Module video.ts(video.js)

``` typescript
import {} from "bilibili-api-ts/video";
```

## class Video

### Functions

#### _constructor_ ()

| name | type | description |
| - | - | - |
| bvid | string | 视频 bvid |
| aid | int | 视频 aid |
| credential | Credential | 凭据类 |

#### function get_aid()

获取视频 aid

**Returns:** aid

#### function set_aid()

设置视频 aid

**Returns:** None

#### function get_bvid()

获取视频 bvid

**Returns:** bvid

#### function set_bvid()

设置视频 bvid

**Returns:** None

#### _async_ function get_info()

获取视频详细信息

**Returns:** 调用 API 返回的结果

#### _async_ function get_stat()

获取视频统计数据（播放量，点赞数等）。

**Returns:** API 调用返回结果。

#### _async_ function get_tags()

获取视频标签。

**Returns:** API 调用返回结果。

#### _async_ function get_chargers()

获取视频充电用户。

**Returns:** API 调用返回结果。

#### _async_ function get_pages()

获取分 P 信息。

**Returns:** API 调用返回结果。

#### _async_ function get_download_url()

| name       | type          | description                          |
| ---------- | ------------- | ------------------------------------ |
| page_index | int, optional | 分 P 号，从 0 开始。defaults to null |
| cid        | int, optional | 分 P 的 ID。defaults to null    |
| html5      | bool, optional | 是否以 html5 平台访问，这样子能直接在网页中播放，但是链接少。 |

获取视频下载信息。

**Returns:** API 调用返回结果。
