# bilibili_api.video_uploader

from bilibili_api import video_uploader


async def test_a_get_missions():
    return await video_uploader.get_missions()
