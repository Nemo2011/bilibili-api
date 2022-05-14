from re import L
from bilibili_api import misc

async def test_a_get_search():
    return await misc.web_search("蹦蹦摸鱼")

async def test_b_get_search_by_type():
    tpe = misc.SearchObjectType.USER
    return await misc.web_search_by_type("蹦蹦摸鱼", tpe)
