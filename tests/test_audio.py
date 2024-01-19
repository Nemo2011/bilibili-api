# bilibili_api.audio

from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException
from bilibili_api.audio import Audio, AudioList, get_user_stat, get_hot_song_list

from .common import get_credential

credential = get_credential()

audio = Audio(1033769, credential)

audio_list = AudioList(26241, credential)


async def test_a_Audio_get_info():
    return await audio.get_info()


async def test_b_Audio_get_tags():
    return await audio.get_tags()


async def test_c_get_user_stat():
    return await get_user_stat(660303135, credential)


async def test_d_Audio_get_download_url():
    return await audio.get_download_url()


async def test_e_Audio_add_coins():
    try:
        return await audio.add_coins()
    except ResponseCodeException as e:
        if e.code != 34005 and e.code != -104:
            raise e

        return e.raw


async def test_f_AudioList_get_info():
    return await audio_list.get_info()


async def test_g_AudioList_get_song_list():
    return await audio_list.get_song_list()


async def test_h_AudioList_get_tags():
    return await audio_list.get_tags()


async def test_j_get_hot_song_list():
    return await get_hot_song_list()
