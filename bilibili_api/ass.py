"""
bilibili_api.ass

有关 ASS 文件的操作
"""
import os
from tempfile import gettempdir
from typing import Union, Optional

from .video import Video
from .bangumi import Episode
from .cheese import CheeseVideo
from .utils.srt2ass import srt2ass
from .utils.json2srt import json2srt
from .utils.credential import Credential
from .utils.danmaku2ass import Danmaku2ASS
from .utils.network import get_session
from .exceptions.ArgsException import ArgsException


def export_ass_from_xml(
    file_local,
    output_local,
    stage_size,
    font_name,
    font_size,
    alpha,
    fly_time,
    static_time,
) -> None:
    """
    以一个 XML 文件创建 ASS

    一定看清楚 Arguments!

    Args:
        file_local   (str)       : 文件输入
        output_local (str)       : 文件输出
        stage_size   (tuple(int)): 视频大小
        font_name    (str)       : 字体
        font_size    (float)     : 字体大小
        alpha        (float)     : 透明度(0-1)
        fly_time     (float)     : 滚动弹幕持续时间
        static_time  (float)     : 静态弹幕持续时间
    """
    Danmaku2ASS(
        input_files=file_local,
        input_format="Bilibili",
        output_file=output_local,
        stage_width=stage_size[0],
        stage_height=stage_size[1],
        reserve_blank=0,
        font_face=font_name,
        font_size=font_size,
        text_opacity=alpha,
        duration_marquee=fly_time,
        duration_still=static_time,
    )


def export_ass_from_srt(file_local, output_local) -> None:
    """
    转换 srt 至 ass

    Args:
        file_local   (str): 文件位置

        output_local (str): 输出位置
    """
    srt2ass(file_local, output_local, "movie")


def export_ass_from_json(file_local, output_local) -> None:
    """
    转换 json 至 ass

    Args:
        file_local   (str): 文件位置

        output_local (str): 输出位置
    """
    json2srt(file_local, output_local.replace(".ass", ".srt"))
    srt2ass(output_local.replace(".ass", ".srt"), output_local, "movie")
    os.remove(output_local.replace(".ass", ".srt"))


async def make_ass_file_subtitle(
    obj: Union[Video, Episode],
    page_index: Optional[int] = 0,
    cid: Optional[int] = None,
    out: Optional[str] = "test.ass",
    lan_name: Optional[str] = "中文（自动生成）",
    lan_code: Optional[str] = "ai-zh",
    credential: Credential = Credential(),
) -> None:
    """
    生成视频字幕文件

    Args:
        obj        (Union[Video,Episode]): 对象

        page_index (int, optional)       : 分 P 索引

        cid        (int, optional)       : cid

        out        (str, optional)       : 输出位置. Defaults to "test.ass".

        lan_name   (str, optional)       : 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）".

        lan_code   (str, optional)       : 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh"

        credential (Credential)          : Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处
    """
    # 目测必须得有 Credential 才能获取字幕
    if credential.has_sessdata():
        obj.credential = credential
    elif not obj.credential.has_sessdata():
        raise credential.raise_for_no_sessdata()

    if isinstance(obj, Episode):
        info = await obj.get_player_info(cid=await obj.get_cid(), epid=obj.get_epid())
    else:
        if cid == None:
            if page_index == None:
                raise ArgsException("page_index 和 cid 至少提供一个。")
            cid = await obj.get_cid(page_index=page_index)
        info = await obj.get_player_info(cid=cid)
    json_files = info["subtitle"]["subtitles"]
    for subtitle in json_files:
        if subtitle["lan_doc"] == lan_name or subtitle["lan"] == lan_code:
            url = subtitle["subtitle_url"]
            if isinstance(obj, Episode) or "https:" not in url:
                url = "https:" + url
            req = await get_session().request("GET", url)
            file_dir = gettempdir() + "/" + "subtitle.json"
            with open(file_dir, "wb") as f:
                f.write(req.content)
            export_ass_from_json(file_dir, out)
            return
    raise ValueError("没有找到指定字幕")


async def make_ass_file_danmakus_protobuf(
    obj: Union[Video, Episode, CheeseVideo],
    page: int = 0,
    out="test.ass",
    cid: Union[int, None] = None,
    credential: Union[Credential, None] = None,
    date=None,
    font_name="Simsun",
    font_size=25.0,
    alpha=1,
    fly_time=7,
    static_time=5,
) -> None:
    """
    生成视频弹幕文件

    来源：protobuf

    Args:
        obj         (Union[Video,Episode,CheeseVideo])       : 对象

        page        (int, optional)                          : 分 P 号. Defaults to 0.

        out         (str, optional)                          : 输出文件. Defaults to "test.ass"

        cid         (int | None, optional)                   : cid. Defaults to None.

        credential  (Credential | None, optional)            : 凭据. Defaults to None.

        date        (datetime.date, optional)                : 获取时间. Defaults to None.

        font_name   (str, optional)                          : 字体. Defaults to "Simsun".

        font_size   (float, optional)                        : 字体大小. Defaults to 25.0.

        alpha       (float, optional)                        : 透明度(0-1). Defaults to 1.

        fly_time    (float, optional)                        : 滚动弹幕持续时间. Defaults to 7.

        static_time (float, optional)                        : 静态弹幕持续时间. Defaults to 5.
    """
    credential = credential if credential else Credential()
    if date:
        credential.raise_for_no_sessdata()
    if isinstance(obj, Video):
        v = obj
        if isinstance(obj, Episode):
            cid = 0
        else:
            if cid is None:
                if page is None:
                    raise ArgsException("page_index 和 cid 至少提供一个。")
                # type: ignore
                cid = await v._Video__get_page_id_by_index(page)
        try:
            info = await v.get_info()
        except:
            info = {"dimension": {"width": 1440, "height": 1080}}
        width = info["dimension"]["width"]
        height = info["dimension"]["height"]
        if width == 0:
            width = 1440
        if height == 0:
            height = 1080
        stage_size = (width, height)
        if isinstance(obj, Episode):
            danmakus = await v.get_danmakus()
        else:
            danmakus = await v.get_danmakus(cid=cid, date=date)  # type: ignore
    elif isinstance(obj, CheeseVideo):
        stage_size = (1440, 1080)
        danmakus = await obj.get_danmakus()
    else:
        raise ValueError("请传入 Video/Episode/CheeseVideo 类！")
    with open(gettempdir() + "/danmaku_temp.xml", "w+", encoding="utf-8") as file:
        file.write("<i>")
        for d in danmakus:
            file.write(d.to_xml())
        file.write("</i>")
    export_ass_from_xml(
        gettempdir() + "/danmaku_temp.xml",
        out,
        stage_size,
        font_name,
        font_size,
        alpha,
        fly_time,
        static_time,
    )


async def make_ass_file_danmakus_xml(
    obj: Union[Video, Episode, CheeseVideo],
    page: int = 0,
    out="test.ass",
    cid: Union[int, None] = None,
    font_name="Simsun",
    font_size=25.0,
    alpha=1,
    fly_time=7,
    static_time=5,
) -> None:
    """
    生成视频弹幕文件

    来源：xml

    Args:
        obj         (Union[Video,Episode,Cheese]): 对象

        page        (int, optional)              : 分 P 号. Defaults to 0.

        out         (str, optional)              : 输出文件. Defaults to "test.ass".

        cid         (int | None, optional)       : cid. Defaults to None.

        font_name   (str, optional)              : 字体. Defaults to "Simsun".

        font_size   (float, optional)            : 字体大小. Defaults to 25.0.

        alpha       (float, optional)            : 透明度(0-1). Defaults to 1.

        fly_time    (float, optional)            : 滚动弹幕持续时间. Defaults to 7.

        static_time (float, optional)            : 静态弹幕持续时间. Defaults to 5.
    """
    if isinstance(obj, Video):
        v = obj
        if isinstance(obj, Episode):
            cid = 0
        else:
            if cid is None:
                if page is None:
                    raise ArgsException("page_index 和 cid 至少提供一个。")
                cid = await v._Video__get_page_id_by_index(page)  # type: ignore
        try:
            info = await v.get_info()
        except:
            info = {"dimension": {"width": 1440, "height": 1080}}
        width = info["dimension"]["width"]
        height = info["dimension"]["height"]
        if width == 0:
            width = 1440
        if height == 0:
            height = 1080
        stage_size = (width, height)
        if isinstance(obj, Episode):
            xml_content = await v.get_danmaku_xml()
        else:
            xml_content = await v.get_danmaku_xml(cid=cid)  # type: ignore
    elif isinstance(obj, CheeseVideo):
        stage_size = (1440, 1080)
        xml_content = await obj.get_danmaku_xml()
    else:
        raise ValueError("请传入 Video/Episode/CheeseVideo 类！")
    with open(gettempdir() + "/danmaku_temp.xml", "w+", encoding="utf-8") as file:
        file.write(xml_content)
    export_ass_from_xml(
        gettempdir() + "/danmaku_temp.xml",
        out,
        stage_size,
        font_name,
        font_size,
        alpha,
        fly_time,
        static_time,
    )
