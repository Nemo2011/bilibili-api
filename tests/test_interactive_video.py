import asyncio
import time
from bilibili_api.utils.Danmaku import Danmaku
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException
from bilibili_api import interactive_video as video_m, exceptions
from .common import get_credential
import datetime

BVID = "BV1pK4y197mm"
AID = 931111241

video = video_m.IVideo(BVID, credential=get_credential())

async def test_get_pages():
    pages = await video.get_pages()
    return pages


async def test_get_download_url():
    pages = await video.get_download_url(1)
    return pages

