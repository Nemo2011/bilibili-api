# bilibili_api.comment

import random
import asyncio

from bilibili_api import comment
from bilibili_api.exceptions.ResponseCodeException import ResponseCodeException

from . import common

BVID = "BV1xx411c7Xg"
AID = 271
credential = common.get_credential()


async def test_a_get_comments():
    result = await comment.get_comments(
        oid=AID, type_=comment.CommentResourceType.VIDEO
    )
    return result


comment_id = None


async def test_b_send_comment():
    print()
    print("测试回复视频")
    result = await comment.send_comment(
        "测试" + str(random.random()),
        oid=AID,
        type_=comment.CommentResourceType.VIDEO,
        credential=credential,
    )
    global comment_id
    comment_id = result["rpid"]
    await asyncio.sleep(1)
    print("测试回复评论")
    result = await comment.send_comment(
        "测试回复评论" + str(random.random()),
        oid=AID,
        type_=comment.CommentResourceType.VIDEO,
        root=comment_id,
        credential=credential,
    )
    rpid = result["rpid"]
    await asyncio.sleep(1)
    print("测试回复评论的评论")
    result = await comment.send_comment(
        "测试回复评论的评论" + str(random.random()),
        oid=AID,
        type_=comment.CommentResourceType.VIDEO,
        root=comment_id,
        parent=rpid,
        credential=credential,
    )
    await asyncio.sleep(1)
    return result


async def test_c_like_comment():
    cmt = comment.Comment(
        oid=AID,
        type_=comment.CommentResourceType.VIDEO,
        rpid=comment_id,
        credential=credential,
    )
    return await cmt.like()


async def test_d_hate_comment():
    cmt = comment.Comment(
        oid=AID,
        type_=comment.CommentResourceType.VIDEO,
        rpid=comment_id,
        credential=credential,
    )
    return await cmt.hate()


# async def test_e_pin_comment():
#     cmt = comment.Comment(
#         oid=AID,
#         type_=comment.CommentResourceType.VIDEO,
#         rpid=comment_id,
#         credential=credential,
#     )
#     try:
#         info = await cmt.pin()
#         return info
#     except ResponseCodeException as e:
#         # -403  权限不足
#         if e.code not in (-403,):
#             raise e
#         return e.raw
# FIXME: 重试次数达到上限


async def test_f_get_sub_comments():
    cmt = comment.Comment(
        oid=AID,
        type_=comment.CommentResourceType.VIDEO,
        rpid=comment_id,
        credential=credential,
    )
    return await cmt.get_sub_comments()


async def test_g_delete_comment():
    cmt = comment.Comment(
        oid=AID,
        type_=comment.CommentResourceType.VIDEO,
        rpid=comment_id,
        credential=credential,
    )
    return await cmt.delete()
