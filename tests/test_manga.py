# bilibili_api.manga

from .common import get_credential
from bilibili_api import manga

comic = manga.Manga(manga_id=30023, credential=get_credential())

async def test_a_Manga_get_info():
    return await comic.get_info()


async def test_b_Manga_get_images_url():
    return await comic.get_images_url(1)


async def test_c_Manga_get_images():
    return await comic.get_images(1)


async def test_d_set_follow_manga():
    print()
    print("正在设置追漫...")
    await manga.set_follow_manga(manga=comic, status=True)
    print("正在取消追漫...")
    await manga.set_follow_manga(manga=comic, status=False)


async def test_e_get_manga_index():
    return await manga.get_manga_index()