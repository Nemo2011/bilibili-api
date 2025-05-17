# 示例：获取一个合集中的所有视频

````
import asyncio
from bilibili_api import channel_series, Credential


#定义合集或列表id。例如一个网址为https://space.bilibili.com/111/lists/222?type=series的合集，其id为222。
series_id=0

async def main():
	#实例化credential 如果只是获取视频，只需给予sessdata即可
	credential=Credential(sessdata='')
	#实例化series
    series = channel_series.ChannelSeries(id_=series_id, credential=cre)
    #获取合集中所有的视频信息
    video_list = await series.get_videos()
	

asyncio.run(main())
```
````