# 示例：查找分区

``` python
from bilibili_api import live_area, sync

# 因为直播分区容易出现变动，故不像视频分区一样直接使用文件保存，而是每次查询时先抓取一遍。
sync(live_area.fetch_live_area_data())

print(live_area.get_area_info_by_name("互动玩法")[0]) # 此分区为主分区
```
