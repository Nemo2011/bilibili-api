import asyncio
import time
from bilibili_api import interactive_video as video_m
from .common import get_credential
import datetime

BVID = "BV1pK4y197mm"
AID = 931111241

video = video_m.IVideo(BVID, credential=get_credential())

async def test_get_pages():
    pages = await video.get_pages()
    return pages


