# bilibili_api.session

from bilibili_api import ResponseCodeException, session

from .common import get_credential


async def test_a_fetch_session_msgs():
    return await session.fetch_session_msgs(12076317, get_credential())


async def test_b_get_sessions():
    return await session.get_sessions(get_credential())

async def test_c_get_new_sessions():
    return await session.new_sessions(get_credential())


async def test_d_send_msg():
    try:
        return await session.send_msg(
            get_credential(), 1666311555, session.EventType.TEXT, "THIS IS A TEST MSG. "
        )
        # 660303135 表示有意见[doge]
    except ResponseCodeException as e:
        if e.code == 21026:
            return e.raw
        else:
            raise e


async def test_e_get_likes():
    return await session.get_likes(get_credential())


async def test_f_get_replies():
    return await session.get_replies(get_credential())


async def test_g_get_system_messages():
    return await session.get_system_messages(get_credential())


async def test_h_get_unread_messages():
    return await session.get_unread_messages(get_credential())


async def test_i_get_session_configs():
    return await session.get_session_settings(get_credential())

async def test_j_get_session_detail():
    return await session.get_session_detail(get_credential(), 12076317, 1)
