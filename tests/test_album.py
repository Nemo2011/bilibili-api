# bilibili_api.album

from bilibili_api import album

al = album.Album(123348276)


# async def test_a_Album_get_info():
#     return await al.get_info()


# async def test_b_Album_get_pictures():
#     return await al.get_pictures()


async def test_c_get_homepage_albums():
    return await album.get_homepage_albums_list()


async def test_d_get_recommend_uppers():
    return await album.get_homepage_recommend_uppers()


# async def test_e_get_user_albums():
#     return await album.get_user_albums(53456)
