# 示例：获取鬼畜频道最新的视频

``` python
from bilibili_api import channel, sync
kichiku = channel.Channel(68)
print(
    sync(
        kichiku.get_list(
            order_or_filter=channel.ChannelVideosOrder.NEW
        )
    )
)
```
