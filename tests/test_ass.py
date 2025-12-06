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


async def test_base_ass_json_data():
    a = await ass.request_subtitle_languages(v, credential=get_credential())
    print(await a.request_ass_data_str())
    print(a.to_srt())
    print(a.to_ass())
    print(a.to_lrc())
    print(a.to_simple_json())
    print(a.to_simple_json_str())
    return


async def test_c_ass_subtitle():
    return await ass.make_ass_file_subtitle(v, lan_name="中文（中国）", out="subtitle.ass", credential=get_credential())


async def test_c_srt_subtitle():
    return await ass.make_srt_file_subtitle(v, lan_name="中文（中国）", out="subtitle.srt", credential=get_credential())


async def test_c_lrc_subtitle():
    return await ass.make_lrc_file_subtitle(v, lan_name="中文（中国）", out="subtitle.lrc", credential=get_credential())


async def test_c_json_subtitle():
    return await ass.make_simple_json_file_subtitle(v, lan_name="中文（中国）", out="subtitle.json", credential=get_credential())
