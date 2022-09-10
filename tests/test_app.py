# bilibili_api.app

from bilibili_api import app
from .common import get_credential

credential = get_credential()


async def test_a_get_loading_images():
    return await app.get_loading_images(credential=credential)


async def test_b_get_loading_images_special():
    return await app.get_loading_images_special(credential=credential)
