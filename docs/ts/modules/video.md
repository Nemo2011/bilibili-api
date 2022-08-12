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

| name | type | description |
| ---- | ---- | ----------- |
| aid  | number  | AV 号。     |

设置视频 aid

**Returns:** None

#### function get_bvid()

获取视频 bvid

**Returns:** bvid

#### function set_bvid()

| name | type | description |
| ---- | ---- | ----------- |
| bvid  | string  | BV 号。     |

设置视频 bvid

**Returns:** None

#### async function get_info()

获取视频详细信息

**Returns:** 调用 API 返回的结果

#### async function get_stat()

获取视频统计数据（播放量，点赞数等）。

**Returns:** API 调用返回结果。

#### async function get_tags()

获取视频标签。

**Returns:** API 调用返回结果。

#### async function get_chargers()

获取视频充电用户。

**Returns:** API 调用返回结果。

#### async function get_pages()

获取分 P 信息。

**Returns:** API 调用返回结果。

#### async function get_download_url()

| name       | type          | description                          |
| ---------- | ------------- | ------------------------------------ |
| page_index | int, optional | 分 P 号，从 0 开始。defaults to null |
| cid        | int, optional | 分 P 的 ID。defaults to null    |
| html5      | bool, optional | 是否以 html5 平台访问，这样子能直接在网页中播放，但是链接少。 |

获取视频下载信息。

**Returns:** API 调用返回结果。

#### async function get_related()

获取相关视频信息。

**Returns:** API 调用返回结果。

#### async function has_liked()

视频是否点赞过。

**Returns:** bool: 视频是否点赞过。

#### async function get_pay_coins()

获取视频已投币数量。

**Returns:** int: 视频已投币数量。

#### async function has_favoured()

是否已收藏。

**Returns:** bool: 视频是否已收藏。

#### async function get_media_list()

获取收藏夹列表信息，用于收藏操作，含各收藏夹对该视频的收藏状态。

**Returns:** API 调用返回结果。

#### async function get_pbp()

| name | type | description |
| page_index | int | 分 P 号 |
| cid | int | 分 P 编码 |

获取高能进度条

**Returns:** Object: 调用 API 返回的结果

#### async function like()

| name | type | description |
| - | - | - |
| status | boolean | 点赞状态。Defaults to True. |

点赞视频。

**Returns:** null: 调用 API 返回的结果。

#### async function pay_coin()

| name | type | description |
| - | - | - |
| num | number | 投币数量（1 ~ 2), defaults to 1 |
| like | boolean | 是否同时点赞, defaults to false |

投币

**Returns:** null: 调用 API 返回的结果。
