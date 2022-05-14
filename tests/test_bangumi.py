from bilibili_api import bangumi
from .common import get_credential

media_id = 28231846
epid = 374717
season_id = None
credential = get_credential()

async def test_a_get_meta():
    data = await bangumi.get_meta(media_id, credential)
    global season_id
    season_id = data['media']['season_id']
    return data

async def test_b_get_short_comment_list():
    return await bangumi.get_short_comment_list(media_id, credential=credential)

async def test_c_get_long_comment_list():
    return await bangumi.get_long_comment_list(media_id, credential=credential)

async def test_d_get_episodes_list():
    return await bangumi.get_episode_list(season_id, credential)

async def test_e_get_stat():
    return await bangumi.get_stat(season_id, credential)

async def test_f_get_episode_info():
    return await bangumi.get_episode_info(epid, credential)

async def test_g_get_overview():
    return await bangumi.get_overview(season_id, credential)

async def test_h_set_follow():
    return await bangumi.set_follow(season_id, credential=credential)
