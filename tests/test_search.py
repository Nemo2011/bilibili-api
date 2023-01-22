# bilibili_api.search

from bilibili_api import search, channel


async def test_a_search():
    return await search.search("这是他的笑容发生的变化")


async def test_b_search_by_type():
    return await search.search_by_type("丸子叨叨叨", search.SearchObjectType.USER)


async def test_c_get_hot_search_keywords():
    return await search.get_hot_search_keywords()


async def test_d_get_default_search_keyword():
    return await search.get_default_search_keyword()


async def test_e_get_suggest_keywords():
    return await search.get_suggest_keywords("gswdm")


async def test_f_search_by_order():
    return await search.search_by_type(
        "小马宝莉",
        search_type = search.SearchObjectType.VIDEO,
        order_type = search.OrderVideo.SCORES,
        time_range = 10,
        topic_type = channel.ChannelTypes.DOUGA_MMD,
        page = 1,
        debug_param_func = print,
    )


async def test_g_search_game():
    return await search.search_games(
        "原神"
    )


async def test_h_search_manga():
    return await search.search_manga(
        "来自深渊"
    )


async def test_i_search_cheese():
    return await search.search_cheese(
        "Python"
    )
