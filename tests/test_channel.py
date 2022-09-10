# bilibili_api.channel

from bilibili_api import channel


async def test_a_get_channel_info_by_tid():
    return channel.get_channel_info_by_tid(3)


async def test_b_get_channel_info_by_name():
    return channel.get_channel_info_by_name("喵星人")


async def test_c_get_top10():
    return await channel.get_top10(3)


async def test_d_get_channel_list():
    return channel.get_channel_list()


async def test_e_get_channel_list_sub():
    return channel.get_channel_list_sub()
