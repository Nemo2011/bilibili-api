"""
ivitools.download

下载互动视频
"""
import os

import tqdm
import httpx
from colorama import Fore

from bilibili_api import sync, interactive_video, video

def download_interactive_video(bvid: str, out: str):
    ivideo = interactive_video.InteractiveVideo(bvid)
    downloader = interactive_video.InteractiveVideoDownloader(
        ivideo, out, stream_detecting_params={
            "codecs": [video.VideoCodecs.AVC]
        }
    )

    @downloader.on("START")
    async def on_start(data):
        print("Start downloading " + bvid + "...")

    @downloader.on("GET")
    async def on_get(data):
        print(f'Get node {data["title"]} (node_id: {data["node_id"]}). ')

    @downloader.on("PREPARE_DOWNLOAD")
    async def on_prepare_download(data):
        print(
            f'Start download the video for cid {data["cid"]}'
        )

    @downloader.on("PACKAGING")
    async def on_packaing(data):
        print("Packaging your file ...")

    @downloader.on("SUCCESS")
    async def on_success(data):
        print(
            Fore.GREEN
            + "Congratulations! Your IVI file is ready. Check it at "
            + os.path.abspath(out)
            + ". "
            + Fore.RESET
        )

    try:
        sync(downloader.start())
    except KeyboardInterrupt:
        sync(downloader.abort())
        print(Fore.YELLOW + "[WRN]: Aborted by user. " + Fore.RESET)
    except Exception as e:
        raise e
