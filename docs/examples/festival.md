# 示例：下载拜年祭所有视频

``` python
import asyncio

from bilibili_api import festival, video, Credential, HEADERS, get_client
import os

SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""

# FFMPEG 路径，查看：http://ffmpeg.org/
FFMPEG_PATH = "ffmpeg"

FES_ID = "bnj2025"


async def download(url: str, out: str, intro: str):
    dwn_id = await get_client().download_create(url, HEADERS)
    bts = 0
    tot = get_client().download_content_length(dwn_id)
    with open(out, "wb") as file:
        while True:
            print(f"{intro} - {out} [{bts} / {tot}]", end="\r")
            bts += file.write(await get_client().download_chunk(dwn_id))
            if bts == tot:
                break
    print()


async def main():
    if not os.path.exists(FES_ID):
        os.mkdir(FES_ID)
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 2022 拜年祭：https://www.bilibili.com/festival/bnj2025
    # 实例化 Festival 类
    fes_2022 = festival.Festival(fes_id=FES_ID, credential=credential)
    video_sections = (await fes_2022.get_info())["videoSections"]
    for section in video_sections:  # 遍历所有“段落” (正片/单品/幕后花絮等等)
        for v in section["episodes"]:
            # 实例化每一个视频
            filename = v["title"]
            await download_video(
                video.Video(bvid=v["bvid"], credential=credential),
                f"{FES_ID}/{filename}.mp4",
            )


async def download_video(v: video.Video, out: str):
    print(f"########## {v.get_bvid()} ##########")
    # 获取视频下载链接
    download_url_data = await v.get_download_url(0)
    # 解析视频下载信息
    detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
    streams = detecter.detect_best_streams(
        video_max_quality=video.VideoQuality._1080P,
        audio_max_quality=video.AudioQuality._192K,
        no_dolby_audio=True,
        no_dolby_video=True,
        no_hdr=True,
        no_hires=True,
    )
    # 有 MP4 流 / FLV 流两种可能
    if detecter.check_video_and_audio_stream():
        # MP4 流下载
        await download(streams[0].url, "video_temp.m4s", "视频流")
        await download(streams[1].url, "audio_temp.m4s", "音频流")
        # 混流
        os.system(
            f"{FFMPEG_PATH} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy \"{out}\""
        )
        # 删除临时文件
        os.remove("video_temp.m4s")
        os.remove("audio_temp.m4s")
    else:
        # FLV 流下载
        await download(streams[0].url, "flv_temp.flv", "FLV 音视频流")
        # 转换文件格式
        os.system(f"{FFMPEG_PATH} -i flv_temp.flv \"{out}\"")
        # 删除临时文件
        os.remove("flv_temp.flv")

    print(f"已下载为：{out}")


if __name__ == "__main__":
    # 主入口
    asyncio.run(main())
```
