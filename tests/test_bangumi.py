# bilibili_api.bangumi

from bilibili_api import bangumi

# from .common import get_credential

b = bangumi.Bangumi(28231846)
ep = bangumi.Episode(374717)

# 港澳台 ep 测试 START
r = bangumi.Bangumi(epid=675686)  # 港澳台番剧
e = bangumi.Bangumi(epid=674709)  # 内地番剧
from bilibili_api import sync
async def test_gangaotai_get_list():
    return e.get_ep_list()
async def test_gangaotai_get_item():
    return e.get_ep_info()
info1 = sync(test_gangaotai_get_list())
info2 = sync(test_gangaotai_get_item())
print(info1)
print(info2)
# 港澳台 ep 测试 END

async def test_a_Bangumi_get_meta():
    return await b.get_meta()


async def test_b_Bangumi_get_short_comment_list():
    return await b.get_short_comment_list()


async def test_c_Bangumi_get_long_comment_list():
    return await b.get_long_comment_list()


async def test_d_Bangumi_get_episode_list():
    return await b.get_episode_list()


async def test_e_Bangumi_get_stat():
    return await b.get_stat()


async def test_f_Episode_get_episode_info():
    return await ep.get_episode_info()


async def test_g_Bangumi_get_overview():
    return await b.get_overview()
