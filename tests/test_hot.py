# bilibili_api.hot

from bilibili_api import hot


async def test_b_get_hot_video():
    return await hot.get_hot_videos()


async def test_c_get_85_popular_video():
    return await hot.get_history_popular_videos()


async def test_d_get_weekly_hot_video_list():
    return await hot.get_weekly_hot_videos_list()


async def test_e_get_weekly_hot_video_content():
    return await hot.get_weekly_hot_videos(161)


async def test_f_get_hot_buzzwords():
    return await hot.get_hot_buzzwords()
