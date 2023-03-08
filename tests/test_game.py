from bilibili_api import game
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException

g = game.Game(105667)


async def test_a_Game_get_info():
    return await g.get_info()


async def test_b_Game_get_up_info():
    return await g.get_up_info()


async def test_c_Game_get_detail():
    return await g.get_detail()


async def test_d_Game_get_wiki():
    try:
        return await g.get_wiki()
    except ResponseCodeException as e:
        if e.code == -703:
            # 数据为空
            return e.raw
        else:
            raise e


async def test_e_Game_get_videos():
    return await g.get_videos()


async def test_f_Game_get_score():
    return await g.get_score()
