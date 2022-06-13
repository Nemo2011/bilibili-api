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
    asyncio.get_event_loop().run_until_complete(main())
```

# 示例：视频在线人数监测

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
from bilibili_api import video, Credential, HEADERS
import aiohttp
import os

SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""

# FFMPEG 路径，查看：http://ffmpeg.org/
FFMPEG_PATH = "ffmpeg"

async def main():
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 Video 类
    v = video.Video(bvid="BV1AV411x7Gs", credential=credential)
    # 获取视频下载链接
    url = await v.get_download_url(0)
    # 视频轨链接
    video_url = url["dash"]["video"][0]['baseUrl']
    # 音频轨链接
    audio_url = url["dash"]["audio"][0]['baseUrl']
    async with aiohttp.ClientSession() as sess:
        # 下载视频流
        async with sess.get(video_url, headers=HEADERS) as resp:
            length = resp.headers.get('content-length')
            with open('video_temp.m4s', 'wb') as f:
                process = 0
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break

                    process += len(chunk)
                    print(f'下载视频流 {process} / {length}')
                    f.write(chunk)

        # 下载音频流
        async with sess.get(audio_url, headers=HEADERS) as resp:
            length = resp.headers.get('content-length')
            with open('audio_temp.m4s', 'wb') as f:
                process = 0
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break

                    process += len(chunk)
                    print(f'下载音频流 {process} / {length}')
                    f.write(chunk)

        # 混流
        print('混流中')
        os.system(f'{FFMPEG_PATH} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy video.mp4')

        # 删除临时文件
        os.remove("video_temp.m4s")
        os.remove("audio_temp.m4s")

        print('已下载为：video.mp4')

if __name__ == '__main__':
    # 主入口
    asyncio.get_event_loop().run_until_complete(main())
```

