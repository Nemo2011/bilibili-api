# bilibili_api.homepage

from bilibili_api import homepage

from .common import get_credential


async def test_a_get_top_photo():
    return await homepage.get_top_photo()


async def test_b_get_links():
    return await homepage.get_links(get_credential())


async def test_c_get_popularize():
    return await homepage.get_popularize(get_credential())


async def test_d_get_videos():
    return await homepage.get_popularize(get_credential())
