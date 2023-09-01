from bilibili_api import channel


async def test_a_get_channel_categories():
    return await channel.get_channel_categories()


async def test_b_get_channel_category_detail():
    return await channel.get_channel_category_detail(category_id=4)


async def test_c_get_channels_in_category():
    return await channel.get_channels_in_category(category_id=4)


ch = channel.Channel(channel_id=68)


# async def test_d_get_channel_info():
#     return await ch.get_info()


# async def test_e_get_related_channels():
#     return await ch.get_related_channels()


async def test_f_get_channel_videos():
    return await ch.get_list()


async def test_g_get_channel_videos_by_filter():
    return await ch.get_featured_list(filter=channel.ChannelVideosFilter.YEAR_2023)

# 海外一测就掉，暂时不测试
# async def test_h_get_channel_videos_by_order():
#     return await ch.get_list(order=channel.ChannelVideosOrder.VIEW)
