"""
ivitools.download

下载互动视频
"""
import os

from colorama import Fore
from bilibili_api import interactive_video, sync
import tqdm
import requests


async def download_file(url: str, out: str):
    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"},
        stream=True,
    )
    headers = resp.headers
    CHUNK_SIZE = 1024
    parts = int(headers["Content-Length"]) // CHUNK_SIZE
    if int(headers["Content-Length"]) % CHUNK_SIZE != 0:
        parts += 1
    fp = open(out, "wb")
    bar = tqdm.tqdm(range(parts))
    bar.set_description("DOWNLOADING...")
    bar.display()
    for chunk in resp.iter_content(CHUNK_SIZE):
        fp.write(chunk)
        bar.update(1)


def download_interactive_video(bvid: str, out: str):
    ivideo = interactive_video.InteractiveVideo(bvid)
    downloader = interactive_video.InteractiveVideoDownloader(
        ivideo, out, download_file
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
        print("Almost!!! It's packaging your interactive video now! ")

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
