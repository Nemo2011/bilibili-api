# bilibili_api.rank

from bilibili_api import rank
from bilibili_api.rank import RankType, RankDayType, VIPRankType, MangeRankType
from .common import get_credential


async def test_a_get_rank():
    rank_types = [RankType.All,
                  RankType.Original,
                  RankType.Rookie,
                  RankType.Bangumi,
                  RankType.GuochuangAnime,
                  RankType.Guochuang,
                  RankType.Documentary,
                  RankType.Douga,
                  RankType.Music,
                  RankType.Dance,
                  RankType.Game,
                  RankType.Knowledge,
                  RankType.Technology,
                  RankType.Sports,
                  RankType.Car,
                  RankType.Life,
                  RankType.Food,
                  RankType.Animal,
                  RankType.Fashion,
                  RankType.Ent,
                  RankType.Cinephile,
                  RankType.Movie,
                  RankType.TV,
                  RankType.Variety,
                  RankType.Original
                  ]
    return [await rank.get_rank(rank_type, RankDayType.WEEK) for rank_type in rank_types]


async def test_f_music_rank_weakly_list():
    return await rank.get_music_rank_list()


async def test_g_music_rank_weakly_details():
    return await rank.get_music_rank_weakly_detail(1)


async def test_h_music_rank_weakly_contents():
    return await rank.get_music_rank_weakly_musics(1)


async def test_i_get_vip_rank():
    need_test_ranks = [VIPRankType.VIP,
                       VIPRankType.MOVIE,
                       VIPRankType.TV,
                       VIPRankType.VARIETY,
                       VIPRankType.BANGUMI,
                       VIPRankType.GUOCHUANG,
                       VIPRankType.DOCUMENTARY
                       ]
    return [await rank.get_vip_rank(rank_type) for rank_type in need_test_ranks]

async def test_j_get_manga_rank():
    return [await rank.get_manga_rank(rank_type) for rank_type in MangeRankType]

async def test_k_get_live_sailing_rank():
    return await rank.get_live_sailing_rank()

async def test_l_get_live_hot_rank():
    return await rank.get_live_hot_rank()

async def test_m_get_live_energy_user_rank():
    return await rank.get_live_energy_user_rank()

async def test_n_get_live_rank():
    return await rank.get_live_rank()

async def test_o_get_live_user_medal_rank():
    return await rank.get_live_user_medal_rank()

async def test_p_subscribe_music_rank():
    return await rank.subscribe_music_rank(status=True, credential=get_credential())
