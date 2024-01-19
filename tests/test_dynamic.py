# bilibili_api.dynamic

from time import time, sleep
from datetime import datetime

from bilibili_api import Picture, ResponseCodeException, user, dynamic

from . import common

credential = common.get_credential()

dy: dynamic.Dynamic = dynamic.Dynamic(761008818532384867, credential=credential)

draft_ids = []


# async def test_a_send_dynamic():
#     # 测试发送动态
#     print("测试立即发送纯文本动态")
#     text_dynamic_build = (
#         dynamic.BuildDynmaic()
#         .add_text("测试立即发送纯文本动态")
#         .add_image(
#             Picture.from_file("./design/logo.png").upload_file_sync(
#                 credential=credential
#             )
#         )
#     )
#     global dy
#     dy = dynamic.Dynamic(
#         (await dynamic.send_dynamic(text_dynamic_build, credential=credential))[
#             "dyn_id"
#         ],
#         credential=credential,
#     )
#     print(dy.get_dynamic_id())
# 见L61


async def test_b_get_schedules_list():
    return await dynamic.get_schedules_list(credential=credential)


async def test_e_Dynamic_get_info():
    global dy
    return await dy.get_info()  # type: ignore


async def test_f_Dynamic_get_reposts():
    global dy
    return await dy.get_reposts()  # type: ignore


async def test_g_Dynamic_set_like():
    try:
        await dy.set_like()
    except ResponseCodeException as e:
        if e.code == 65006:
            return "ok"
        raise


# async def test_i_Dynamic_delete():
#     global dy
#     return await dy.delete()  # type: ignore
# FIXME: 不知道为什么每一次自动删除都会出问题。单独跑一遍删除不会出问题。
# 暂时停止动态发送、删除相关操作


async def test_j_get_new_dynamic_users():
    return await dynamic.get_new_dynamic_users(common.get_credential())


async def test_k_get_live_users():
    return await dynamic.get_live_users(credential=common.get_credential())


async def test_l_get_dynamic_page_UPs_info():
    return await dynamic.get_dynamic_page_UPs_info(credential=common.get_credential())


async def test_m_get_dynamic_page_info_by_type():
    return await dynamic.get_dynamic_page_info(
        credential=common.get_credential(), _type=dynamic.DynamicType.ALL
    )


async def test_m_get_dynamic_page_info_by_mid():
    return await dynamic.get_dynamic_page_info(
        credential=common.get_credential(), host_mid=12434430
    )
