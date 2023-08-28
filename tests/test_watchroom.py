from bilibili_api import watchroom

try:
    from . import common

    credential = common.get_credential()
except:
    credential = None
    print("导入凭据未成功")
    
season_id = 113
episode_id = 1678
room: watchroom.WatchRoom


async def test_a_match():
    return await watchroom.match(
        season_id=season_id,
        season_type=watchroom.SeasonType.ANIME,
        credential=credential,
    )


async def test_b_create():
    global room
    room = await watchroom.create(
        season_id=season_id, episode_id=episode_id, is_open=False, credential=credential
    )
    return room


async def test_c_join():
    return await room.join()


async def test_d_share():
    return await room.share()


async def test_e_progress():
    await room.progress(60, 0)
    return await room.progress(30, 1)


async def test_f_open_and_close():
    await room.close()
    return await room.open()


async def test_g_send():
    return await room.send(
        watchroom.Message("测试")
        + watchroom.Message("测试2")
        + watchroom.MessageSegment("测试3")
        + watchroom.MessageSegment("doge", True)
    )

