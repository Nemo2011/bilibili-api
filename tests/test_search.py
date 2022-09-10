# bilibili_api.search

from bilibili_api import search


async def test_a_search():
    return await search.search("云社_")


async def test_b_search_by_type():
    return await search.search_by_type("丸子叨叨叨", search.SearchObjectType.USER)


async def test_c_get_hot_search_keywords():
    return await search.get_hot_search_keywords()


async def test_d_get_default_search_keyword():
    return await search.get_default_search_keyword()


async def test_e_get_suggest_keywords():
    return await search.get_suggest_keywords("gswdm")
