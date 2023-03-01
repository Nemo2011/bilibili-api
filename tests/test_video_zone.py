from bilibili_api import video_zone


async def test_a_get_zone_info_by_tid():
    return video_zone.get_zone_info_by_tid(0)


async def test_b_get_zone_info_by_name():
    return video_zone.get_zone_info_by_name("鬼畜")


async def test_c_get_zone_top10():
    return await video_zone.get_zone_top10(tid=3)


async def test_d_get_zone_new_videos():
    return await video_zone.get_zone_new_videos(tid=3)


async def test_e_get_zone_new_videos_count():
    return await video_zone.get_zone_videos_count_today()


async def test_f_get_zone_list():
    return video_zone.get_zone_list()


async def test_g_get_zone_list_sub():
    return video_zone.get_zone_list_sub()


async def test_g_get_zone_hot_tags():
    return await video_zone.get_zone_hot_tags(tid=33)
