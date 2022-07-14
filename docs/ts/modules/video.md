# 示例：获取视频信息

``` typescript
import { Video } from "bilibili-api-js/video";

export function test_video() {
    var v = new Video(null, 2);
    v.get_info().then(function ( value) {
        console.log(value);
    })
}

test_video();
```