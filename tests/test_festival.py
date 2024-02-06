from bilibili_api import festival

fes = festival.Festival("genshin2023")

async def test_a_Festival_get_info():
    return await fes.get_info()
