# 示例：获取分区排行榜前十视频

``` python
from bilibili_api import video_zone, sync

info = video_zone.get_zone_info_by_name("鬼畜")[0] # 此为主分区，信息位于返回的元组的第 0 项

print(sync(video_zone.get_zone_top10(info["tid"])))
```
