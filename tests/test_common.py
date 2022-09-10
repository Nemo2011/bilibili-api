# bilibili_api.__init__

from bilibili_api import parse_link, get_real_url


async def test_a_parse_link():
    return await parse_link("http://bilibili.com/video/av2")


async def test_b_get_real_url():
    return await get_real_url("https://b23.tv/mx00St")
