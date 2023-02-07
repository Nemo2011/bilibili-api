# bilibili_api.rank

from bilibili_api import rank
from bilibili_api.rank import RankType, RankDayType, VIPRankType, MangeRankType


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
