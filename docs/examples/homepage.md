# 示例：获取主页视频

``` python
from bilibili_api import homepage, sync

print(sync(homepage.get_videos()))
```