# bilibili_api.ass

from bilibili_api import ass, video
from .common import get_credential

v = video.Video("BV1or4y1u7fk")


async def test_a_ass_danmakus_protobuf():
    return await ass.make_ass_file_danmakus_protobuf(
        v, page=0, out="danmakus_protobuf.ass"
    )


async def test_b_ass_danmakus_xml():
    return await ass.make_ass_file_danmakus_xml(v, page=0, out="danmakus_xml.ass")


async def test_c_ass_subtitle():
    return await ass.make_ass_file_subtitle(v, lan_name="中文（中国）", out="subtitle.ass", credential=get_credential())
