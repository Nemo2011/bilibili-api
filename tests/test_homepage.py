# bilibili_api.homepage

from bilibili_api import homepage
from .common import get_credential

async def test_get_top_photo():
    return await homepage.get_top_photo()

async def test_get_links():
    return await homepage.get_links(get_credential())

async def test_get_popularize():
    return await homepage.get_popularize(get_credential())

async def test_get_videos():
    return await homepage.get_popularize(get_credential())
