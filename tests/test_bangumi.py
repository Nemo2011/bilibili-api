# bilibili_api.bangumi

from bilibili_api import bangumi

# from .common import get_credential

b = bangumi.Bangumi(28231846)
ep = bangumi.Episode(374717)


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


from bilibili_api import sync

# print(sync(test_f_Episode_get_episode_info()))
# 港澳台 ep 测试 START
e = bangumi.Bangumi(epid=562695, oversea=True)  # 港澳台番剧


# e = bangumi.Bangumi(media_id=28338523, oversea=True)  # 港澳台番剧
# e = bangumi.Bangumi(epid=674709)  # 内地番剧

async def test_oversea_gangaotai_get_item():
    return e.get_episode_info()


async def test_oversea_gangaotai_get_bangumi():
    return await e.get_meta()


async def test_oversea_Bangumi_get_episode_list():
    return await e.get_episode_list()


async def test_oversea_Bangumi_get_stat():
    return await e.get_stat()

# 特性测试
# info2 = sync(test_oversea_gangaotai_get_item())
# print(info2)
# 兼容测试
# info3 = sync(test_oversea_gangaotai_get_bangumi())
# print(info3)
# 转换测试
# info4 = sync(test_oversea_Bangumi_get_episode_list())
# print(info4)
# 没有被限制的stat接口
# info5 = sync(test_oversea_Bangumi_get_stat())
# print(info5)
# 港澳台 ep 测试 END
