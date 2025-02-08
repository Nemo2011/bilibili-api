# 示例：获取视频信息并点赞

```python
import asyncio
from bilibili_api import video, Credential

SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""

async def main():
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 Video 类
    v = video.Video(bvid="BVxxxxxxxx", credential=credential)
    # 获取视频信息
    info = await v.get_info()
    # 打印视频信息
    print(info)
    # 给视频点赞
    await v.like(True)

if __name__ == '__main__':
    # 主入口
    asyncio.run(main())
```

**以下两个方式接口不同，数据略有偏差**

# 示例：视频在线人数监测 WebSocket

```python
from bilibili_api import video
import asyncio

# 实例化
v = video.VideoOnlineMonitor(bvid="BV1AV411x7Gs")

@v.on('ONLINE')
async def on_online_update(event):
    """
    在线人数更新
    """
    print(event)


@v.on('DANMAKU')
async def on_danmaku(event):
    """
    收到实时弹幕
    """
    print(event)

if __name__ == '__main__':
    # 主入口，v.connect() 为连接服务器
    asyncio.get_event_loop().run_until_complete(v.connect())
```

# 示例：获取视频在线人数 HTTP

```python
from bilibili_api import video
import asyncio

# 实例化
v = video.Video(bvid="BV1AV411x7Gs")

async def main():
    # 获取在线人数
    online = await v.get_online()
    print(f'总共 {online["total"]} 人在观看，其中 {online["count"]} 人在网页端观看')

if __name__ == '__main__':
    asyncio.run(main())
```

# 示例：获取视频弹幕

```python
from bilibili_api import video, sync, Credential

v = video.Video(bvid='BV1AV411x7Gs')

dms = sync(v.get_danmakus(0))

for dm in dms:
    print(dm)
```

# 示例：下载视频

```python
import asyncio

from bilibili_api import video, Credential, HEADERS, get_client
import os

SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""

# FFMPEG 路径，查看：http://ffmpeg.org/
FFMPEG_PATH = "ffmpeg"


async def download(url: str, out: str, intro: str):
    dwn_id = await get_client().download_create(url, HEADERS)
    bts = 0
    tot = get_client().download_content_length(dwn_id)
    with open(out, "wb") as file:
        while True:
            bts += file.write(await get_client().download_chunk(dwn_id))
            print(f"{intro} - {out} [{bts} / {tot}]", end="\r")
            if bts == tot:
                break
    print()


async def main():
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 Video 类
    v = video.Video(bvid="BV1AV411x7Gs", credential=credential)
    # 获取视频下载链接
    download_url_data = await v.get_download_url(0)
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    streams = detecter.detect_best_streams()
    # 有 MP4 流 / FLV 流两种可能
    if detecter.check_flv_mp4_stream() == True:
        # FLV 流下载
        await download(streams[0].url, "flv_temp.flv", "下载 FLV 音视频流")
        # 转换文件格式
        os.system(f"{FFMPEG_PATH} -i flv_temp.flv video.mp4")
        # 删除临时文件
        os.remove("flv_temp.flv")
    else:
        # MP4 流下载
        await download(streams[0].url, "video_temp.m4s", "下载视频流")
        await download(streams[1].url, "audio_temp.m4s", "下载音频流")
        # 混流
        os.system(
            f"{FFMPEG_PATH} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy video.mp4"
        )
        # 删除临时文件
        os.remove("video_temp.m4s")
        os.remove("audio_temp.m4s")

    print("已下载为：video.mp4")


if __name__ == "__main__":
    # 主入口
    asyncio.run(main())
```

