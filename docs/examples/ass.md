# 示例：下载视频的弹幕

``` python
from bilibili_api import ass, sync
sync(ass.make_ass_file_danmakus("BV1fp4y1U747", 0, "out.ass"))
# 别问为什么选择这个视频，就是因为信息量大，可以用于 Debug
```
