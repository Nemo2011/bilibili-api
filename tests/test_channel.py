from bilibili_api import channel


async def test_a_get_channel_info_by_tid():
    main_ch, sub_ch = channel.get_channel_info_by_tid(1)
    assert main_ch["name"] == "动画", "主分区测试，tid=1 时，应当返回 动画 分区内容。"

    main_ch, sub_ch = channel.get_channel_info_by_tid(24)
    assert sub_ch["name"] == "MAD·AMV", "主分区测试，tid=24 时，应当返回 MAD·AMV。"

    return main_ch, sub_ch


async def test_b_get_channel_info_by_name():
    main_ch, sub_ch = channel.get_channel_info_by_name("动画")
    assert main_ch["tid"] == 1, "子分区测试，name=动画 时，应当返回 tid=1。"

    main_ch, sub_ch = channel.get_channel_info_by_name("MAD·AMV")
    assert sub_ch["tid"] == 24, "子分区测试，name=MAD·AMV 时，应当返回 tid=24。"

    return main_ch, sub_ch


async def test_c_get_top10():
    data = await channel.get_top10(1)
    return data
