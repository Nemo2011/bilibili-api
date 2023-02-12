from bilibili_api import creative_center
from . import common

credential = common.get_credential()

async def test_a_get_compare():
    return await creative_center.get_compare(credential)

async def test_b_get_graph():
    return await creative_center.get_graph(credential)

async def test_c_get_overview():
    return await creative_center.get_overview(credential)

async def test_d_get_video_survey():
    return await creative_center.get_video_survey(credential)

async def test_e_get_video_playanalysis():
    return await creative_center.get_video_playanalysis(credential)

async def test_f_get_video_source():
    return await creative_center.get_video_source(credential)

async def test_g_get_fan_overview():
    return await creative_center.get_fan_overview(credential)

async def test_h_get_fan_graph():
    return await creative_center.get_fan_graph(credential)

async def test_i_get_article_overview():
    return await creative_center.get_article_overview(credential)

async def test_j_get_article_graph():
    return await creative_center.get_article_graph(credential)

async def test_k_get_article_source():
    return await creative_center.get_article_source(credential)

async def test_l_get_article_rank():
    return await creative_center.get_article_rank(credential)