# 示例：获取番剧剧集 BV 号

番剧剧集也是视频，只不过是特殊的视频，也有 BV 号。

若想下载，首先得获取到 BV 号。

```python
from bilibili_api import bangumi, sync


async def main():
    ep = bangumi.Episode(374717)
    # 打印 bv 号
    print(await ep.get_bvid())

sync(main())
```

# 示例：获取番剧所有长评

```python
from bilibili_api import bangumi, sync

async def main():
    b = bangumi.Bangumi(28231846)
    next = None
    cmts = []
    while next != 0:
        cm = await b.get_long_comment_list(next=next)
        cmts.extend(cm['list'])
        next = cm['next']

    for cmt in cmts:
        print(cmt)

sync(main())
```

# 示例：获取番剧索引

```python
from bilibili_api import bangumi, sync
from bilibili_api.bangumi import IndexFilter as IF
async def main():
    filters = bangumi.IndexFilterMeta.Anime(area=IF.Area.JAPAN,
        year=IF.make_time_filter(start=2019, end=2022, include_end=True),
        season=IF.Season.SPRING,
        style=IF.Style.Anime.NOVEL)
    index = await bangumi.get_index_info(filters=filters, order=IF.Order.SCORE, sort=IF.Sort.DESC, pn=2, ps=20)
    print(index)

sync(main())

```

# 示例：下载番剧

``` python
import asyncio

from bilibili_api import bangumi, video, Credential, HEADERS, get_client
import os

SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""

# FFMPEG 路径，查看：http://ffmpeg.org/
FFMPEG_PATH = "ffmpeg"

MEDIA_ID = 23679586


async def main():
    if not os.path.exists(str(MEDIA_ID)):
        os.mkdir(str(MEDIA_ID))
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 Bangumi 类
    b = bangumi.Bangumi(media_id=MEDIA_ID, credential=credential)
    # 获取所有剧集
    for idx, ep in enumerate(await b.get_episodes()):
        await download_episode(ep, f"{MEDIA_ID}/{idx + 1}.mp4")


async def download_episode(ep: bangumi.Episode, out: str):
    print(f"########## {await ep.get_bvid()} ##########")
    # 获取视频下载链接
    download_url_data = await ep.get_download_url()
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    streams = detecter.detect_best_streams(
        video_max_quality=video.VideoQuality._1080P,
        audio_max_quality=video.AudioQuality._192K,
        no_dolby_audio=True,
        no_dolby_video=True,
        no_hdr=True,
        no_hires=True
    )
    # 有 MP4 流 / FLV 流两种可能
    if detecter.check_video_and_audio_stream():
        # MP4 流下载
        await get_client().download(streams[0].url, HEADERS, "video_temp.m4s", "视频流")
        await get_client().download(streams[1].url, HEADERS, "audio_temp.m4s", "音频流")
        # 混流
        os.system(
            f"{FFMPEG_PATH} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy {out}"
        )
        # 删除临时文件
        os.remove("video_temp.m4s")
        os.remove("audio_temp.m4s")
    else:
        # FLV 流下载
        await get_client().download(streams[0].url, HEADERS, "flv_temp.flv", "FLV 音视频流")
        # 转换文件格式
        os.system(f"{FFMPEG_PATH} -i flv_temp.flv {out}")
        # 删除临时文件
        os.remove("flv_temp.flv")

    print(f"已下载为：{out}")


if __name__ == "__main__":
    # 主入口
    asyncio.run(main())
```
