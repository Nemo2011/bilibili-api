# bilibili_api.audio

from bilibili_api.audio import Audio, AudioList, get_user_stat
from .common import get_credential
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException

credential = get_credential()

audio = Audio(11589, credential)

audio_list = AudioList(26241, credential)

async def test_a_au_get_info():
    return await audio.get_info()

async def test_b_au_get_tags():
    return await audio.get_tags()

async def test_c_get_user_stat():
    return await get_user_stat(660303135, credential)

async def test_d_au_get_download_url():
    return await audio.get_download_url()

async def test_e_au_add_coins():
    try:
        return await audio.add_coins()
    except ResponseCodeException as e:
        if e.code != 34005:
            raise e

        return e.raw

async def test_f_al_get_info():
    return await audio_list.get_info()

async def test_g_al_get_song_list():
    return await audio_list.get_song_list()

async def test_h_al_get_tags():
    return await audio_list.get_tags()
