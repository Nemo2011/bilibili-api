# 示例：获取视频标签下的视频

``` python
from bilibili_api import video_tag, sync
tag = video_tag.Tag(tag_name="空难")
print(sync(tag.get_cards()))
```
