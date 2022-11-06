# 示例：下载视频的弹幕

``` python
from bilibili_api import ass, sync, video
sync(ass.make_ass_file_danmakus_protobuf(video.Video("BV1AV411x7Gs"), 0, "out.ass"))
```
