# Module video.ts(video.js)

``` typescript
import {} from "bilibili-api-js/video";
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
