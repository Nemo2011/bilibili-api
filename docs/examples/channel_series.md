# 示例：获取一个合集中的所有视频

``` python
import asyncio
from bilibili_api import channel_series, Credential

# 定义合集或列表 id。例如 https://space.bilibili.com/517327498/lists/3993361?type=season

season_id = 3993361


async def main():
    # 实例化 credential 如果只是获取视频，只需给予 sessdata 即可
    credential = Credential(sessdata="")
    # 实例化 series
    series = channel_series.ChannelSeries(
        id_=season_id,
        type_=channel_series.ChannelSeriesType.SEASON,
        credential=credential,
    )
    # 获取合集中所有的视频信息
    video_list = await series.get_videos()
    for v in video_list["archives"]:
        print(v["bvid"], v["title"])


asyncio.run(main())
```
