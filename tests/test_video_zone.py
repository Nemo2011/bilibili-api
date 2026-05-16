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


async def test_h_get_sub_zone_by_main_tid_v2():
    return video_zone.get_sub_zone_by_main_tid_v2(tid_v2 = 1005)


async def test_i_get_zone_info_by_tid_v2():
    return video_zone.get_zone_info_by_tid_v2(tid_v2 = 1005)


async def test_j_get_zone_name_by_tid_v2():
    return video_zone.get_zone_name_by_tid_v2(tid_v2 = 1005)


async def test_k_get_zone_url_by_tid_v2():
    return video_zone.get_zone_url_by_tid_v2(tid_v2 = 1005)


async def test_l_get_tid_v2_by_zone_name():
    return video_zone.get_tid_v2_by_zone_name(name = "动画")
