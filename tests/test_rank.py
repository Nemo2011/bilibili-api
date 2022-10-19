# bilibili_api.rank

from bilibili_api import rank


async def test_a_get_rank():
    return await rank.get_rank()


async def test_b_get_hot_video():
    return await rank.get_hot_videos()


async def test_c_get_85_popular_video():
    return await rank.get_history_popular_videos()


async def test_d_get_weekly_hot_video_list():
    return await rank.get_weakly_hot_videos_list()


async def test_e_get_weekly_hot_video_content():
    return await rank.get_weakly_hot_videos(161)


async def test_f_music_rank_weakly_list():
    return await rank.get_music_rank_list()


async def test_g_music_rank_weakly_details():
    return await rank.get_music_rank_weakly_detail(1)


async def test_h_music_rank_weakly_contents():
    return await rank.get_music_rank_weakly_musics(1)
