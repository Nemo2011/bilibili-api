"""
bilibili_api.ass

有关 ASS 文件的操作
"""

import os
import json
from tempfile import gettempdir
from typing import List, Tuple, Union, Optional

from .video import Video
from .bangumi import Episode
from .cheese import CheeseVideo
from .utils.srt2ass import srt2ass_cover_by_str
from .utils.danmaku2ass import Danmaku2ASS
from .utils.network import Api, Credential
from .exceptions.ArgsException import ArgsException

class AssSubtitleObject:
    def __init__(self, json_lan_list:json, obj:Union[Video, Episode], lan_set:str =None):
        """
        获取远程字幕

        Args:
            json_lan_list        (json)                : 字幕可选语言

            obj                  (Union[Video,Episode]): 对象

            lan_set              (str)              : 设置默认字幕语言，如果为None，则自动获取可获取语言
        """
        self.__json_lan_list = json_lan_list
        self.__json_subtitle_data = None
        self.__obj = obj
        self.__lan_set = lan_set
        self.__data_string = None
        
    def get_lan_list(self) -> Tuple[List[str], List[Optional[str]]]:
        """
        获取字幕语言列表
        
        Returns:
            Tuple[List[str], List[Optional[str]]]: 字幕名,字幕语言代码
        """
        ret_lan_code = []
        ret_lan_doc = []
        for lan in self.__json_lan_list:
            if lan.get("lan"):
                ret_lan_code.append(lan["lan"])
                ret_lan_doc.append(lan.get("lan_doc"))
        return ret_lan_code, ret_lan_doc
        
    async def request_ass_data_json(self, lan_set:str = None) -> json:
        """
        获取对应语言的字幕
        
        Args:
            lan_set     (str)   : 如果为None，则获取默认字幕语言
        
        Returns:
            json: 字幕数据
        """
        if lan_set:
            self.__lan_set = lan_set
        elif self.__lan_set is None:
            ret_lan_code, _ = self.get_lan_list()
            if ret_lan_code:
                self.__lan_set = ret_lan_code[0]
            else:
                self.__lan_set = None
        
        for subtitle in self.__json_lan_list:
            if subtitle["lan"] == self.__lan_set or subtitle["lan_doc"] == self.__lan_set:
                url = subtitle["subtitle_url"]
                if isinstance(self.__obj, Episode) or "https:" not in url:
                    url = "https:" + url
                    
                self.__json_subtitle_data  = await Api(url=url, method="GET").request(raw=True)
                return self.__json_subtitle_data
        
        raise ArgsException("没有找到指定字幕")
    
    async def request_ass_data_str(self, lan_set:str = None) -> str:
        """
        获取对应语言的字幕
        
        Args:
            lan_set     (str)   : 如果为None，则获取默认字幕语言
        
        Returns:
            str: 字幕数据
        """
        if self.__data_string == None:
            if self.__json_subtitle_data:
                self.__data_string = json.dumps(self.__json_subtitle_data)
            else:
                self.__data_string = json.dumps(await self.request_ass_data_json(lan_set=lan_set))
            
        return self.__data_string
    
    def to_srt(self) -> str:
        """
        获取srt格式的字幕
        
        Returns:
            str: srt字幕
        """
        if self.__json_subtitle_data == None:
            raise ArgsException("未进行字幕数据请求")
            
        self.__data_string = ""
        for cnt, comment in enumerate(self.__json_subtitle_data["body"]):
            self.__data_string += (
                "{}\n{}:{}:{},{} --> {}:{}:{},{}\n{}\n\n".format(
                    cnt + 1,
                    str(int(comment["from"]) // 3600).zfill(2),
                    str(int(comment["from"]) // 60 % 60).zfill(2),
                    str(int(comment["from"]) % 60).zfill(2),
                    str(
                        int(round(comment["from"] - int(comment["from"]), 2) * 100)
                    ).zfill(2),
                    str(int(comment["to"] - 0.01) // 3600).zfill(2),
                    str(int(comment["to"] - 0.01) // 60 % 60).zfill(2),
                    str(int(comment["to"] - 0.01) % 60).zfill(2),
                    str(
                        int(
                            round(comment["to"] - 0.01 - int(comment["to"] - 0.01), 2)
                            * 100
                        )
                    ).zfill(2),
                    comment["content"],
                )
            )
        
        return self.__data_string
    
    def to_ass(self) -> str:
        """
        获取ass格式的字幕
        
        Returns:
            str: ass字幕
        """
        srt_string = self.to_srt()
        self.__data_string = srt2ass_cover_by_str(srt_string)
        return self.__data_string
    
    def to_lrc(self) -> str:
        """
        获取lrc格式的字幕
        
        Returns:
            str: lrc字幕
        """
        if self.__json_subtitle_data == None:
            raise ArgsException("未进行字幕数据请求")
        
        self.__data_string = ""
         
        for _, comment in enumerate(self.__json_subtitle_data["body"]):
            self.__data_string += ("[{}:{}:{}]{}\n[{}:{}:{}]\n".format(
                    str(int(comment["from"]) // 3600).zfill(2),
                    str(int(comment["from"]) // 60 % 60).zfill(2),
                    str(int(comment["from"]) % 60).zfill(2),
                    comment["content"],
                    str(int(comment["to"] - 0.01) // 3600).zfill(2),
                    str(int(comment["to"] - 0.01) // 60 % 60).zfill(2),
                    str(int(comment["to"] - 0.01) % 60).zfill(2),
                )
            )
            
        return self.__data_string
    
    def to_simple_json(self) -> json:
        """
        获取简化后的JSON数据

        Returns:
            json: 字幕数据
        """
        if self.__json_subtitle_data == None:
            raise ArgsException("未进行字幕数据请求")
            
        jsonResult = []
        for cnt, comment in enumerate(self.__json_subtitle_data["body"]):
            jsonResult.append({
                "cnt": cnt + 1,
                "start_time": float(comment["from"]),
                "content": comment["content"],
                "end_time": float(comment["to"] - 0.01)
            })
            
        return jsonResult
    
    def to_simple_json_str(self) -> str:
        """
        获取简化后的JSON字符串
        
        Returns:
            str: 获取简化后的JSON字符串
        """
        self.__data_string = json.dumps(self.to_simple_json())
        return self.__data_string
    
    def __str__(self):
        if self.__data_string == None:
            if self.__json_subtitle_data:
                self.__data_string = json.dumps(self.__json_subtitle_data)
            else:
                raise ArgsException("未进行字幕数据请求")
                
        return self.__data_string
        
async def request_subtitle_lan_list(
    obj: Union[Video, Episode],
    page_index: Optional[int] = 0,
    cid: Optional[int] = None,
    credential: Optional[Credential] = None,
) -> AssSubtitleObject:
    """
    获取远程字幕支持JSON数据

    Args:
        obj        (Union[Video,Episode]): 对象

        page_index (int, optional)       : 分 P 索引

        cid        (int, optional)       : cid

        credential (Credential, optional): Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处
        
    Returns:
            AssSubtitleObject: 字幕对象
    """
    # 目测必须得有 Credential 才能获取字幕
    credential = credential if credential else Credential()
    if credential.has_sessdata():
        obj.credential = credential
    elif not obj.credential.has_sessdata():
        credential.raise_for_no_sessdata()

    if isinstance(obj, Episode):
        info = await obj.get_player_info(cid=await obj.get_cid(), epid=obj.get_epid())
    else:
        if cid == None:
            if page_index == None:
                raise ArgsException("page_index 和 cid 至少提供一个。")
            cid = await obj.get_cid(page_index=page_index)
        info = await obj.get_player_info(cid=cid)
    json_data = info["subtitle"]["subtitles"]
    
    return AssSubtitleObject(json_lan_list=json_data, obj=obj)

async def request_subtitle(
    obj: Union[Video, Episode],
    page_index: Optional[int] = 0,
    cid: Optional[int] = None,
    lan_name: Optional[str] = None,
    lan_code: Optional[str] = None,
    credential: Optional[Credential] = None,
) -> AssSubtitleObject:
    """
    获取远程字幕

    Args:
        obj        (Union[Video,Episode]): 对象

        page_index (int, optional)       : 分 P 索引

        cid        (int, optional)       : cid
        
        lan_name   (str, optional)       : 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）" 默认None 则自动获取可用歌词.

        lan_code   (str, optional)       : 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh" 默认None 则自动获取可用歌词

        credential (Credential, optional): Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处
        
    Returns:
            AssSubtitleObject: 字幕对象
    """
    subtitle_data_obj = await request_subtitle_lan_list(obj=obj, page_index=page_index, cid=cid, credential=credential)
    
    try:
        await subtitle_data_obj.request_ass_data_json(lan_set=lan_code)
    except:
        await subtitle_data_obj.request_ass_data_json(lan_set=lan_name)
        
    return subtitle_data_obj
    

async def make_ass_file_subtitle(
    obj: Union[Video, Episode],
    page_index: Optional[int] = 0,
    cid: Optional[int] = None,
    out: Optional[str] = "test.ass",
    lan_name: Optional[str] = "中文（自动生成）",
    lan_code: Optional[str] = "ai-zh",
    credential: Optional[Credential] = None,
) -> None:
    """
    生成视频字幕文件

    编码默认采用 utf-8

    Args:
        obj        (Union[Video,Episode]): 对象

        page_index (int, optional)       : 分 P 索引

        cid        (int, optional)       : cid

        out        (str, optional)       : 输出位置. Defaults to "test.ass".

        lan_name   (str, optional)       : 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）".

        lan_code   (str, optional)       : 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh"

        credential (Credential, optional): Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处
    """
    # 目测必须得有 Credential 才能获取字幕
    subtitle_data_obj = await request_subtitle(obj=obj, page_index=page_index, cid=cid, lan_name=lan_name, lan_code=lan_code, credential=credential)
        
    subtitle_ass_str = subtitle_data_obj.to_ass()
    
    with open(out, "w+", encoding="utf-8") as file:
        file.write(subtitle_ass_str)
        
async def make_srt_file_subtitle(
    obj: Union[Video, Episode],
    page_index: Optional[int] = 0,
    cid: Optional[int] = None,
    out: Optional[str] = "test.srt",
    lan_name: Optional[str] = "中文（自动生成）",
    lan_code: Optional[str] = "ai-zh",
    credential: Optional[Credential] = None,
) -> None:
    """
    生成视频字幕文件

    编码默认采用 utf-8

    Args:
        obj        (Union[Video,Episode]): 对象

        page_index (int, optional)       : 分 P 索引

        cid        (int, optional)       : cid

        out        (str, optional)       : 输出位置. Defaults to "test.ass".

        lan_name   (str, optional)       : 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）".

        lan_code   (str, optional)       : 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh"

        credential (Credential, optional): Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处
    """
    # 目测必须得有 Credential 才能获取字幕
    subtitle_data_obj = await request_subtitle(obj=obj, page_index=page_index, cid=cid, lan_name=lan_name, lan_code=lan_code, credential=credential)
        
    subtitle_ass_str = subtitle_data_obj.to_srt()
    
    with open(out, "w+", encoding="utf-8") as file:
        file.write(subtitle_ass_str)
        
async def make_lrc_file_subtitle(
    obj: Union[Video, Episode],
    page_index: Optional[int] = 0,
    cid: Optional[int] = None,
    out: Optional[str] = "test.lrc",
    lan_name: Optional[str] = "中文（自动生成）",
    lan_code: Optional[str] = "ai-zh",
    credential: Optional[Credential] = None,
) -> None:
    """
    生成视频字幕文件

    编码默认采用 utf-8

    Args:
        obj        (Union[Video,Episode]): 对象

        page_index (int, optional)       : 分 P 索引

        cid        (int, optional)       : cid

        out        (str, optional)       : 输出位置. Defaults to "test.ass".

        lan_name   (str, optional)       : 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）".

        lan_code   (str, optional)       : 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh"

        credential (Credential, optional): Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处
    """
    # 目测必须得有 Credential 才能获取字幕
    subtitle_data_obj = await request_subtitle(obj=obj, page_index=page_index, cid=cid, lan_name=lan_name, lan_code=lan_code, credential=credential)

    subtitle_ass_str = subtitle_data_obj.to_lrc()
    
    with open(out, "w+", encoding="utf-8") as file:
        file.write(subtitle_ass_str)
        
async def make_simpleJson_file_subtitle(
    obj: Union[Video, Episode],
    page_index: Optional[int] = 0,
    cid: Optional[int] = None,
    out: Optional[str] = "test.json",
    lan_name: Optional[str] = "中文（自动生成）",
    lan_code: Optional[str] = "ai-zh",
    credential: Optional[Credential] = None,
) -> None:
    """
    生成视频字幕文件

    编码默认采用 utf-8

    Args:
        obj        (Union[Video,Episode]): 对象

        page_index (int, optional)       : 分 P 索引

        cid        (int, optional)       : cid

        out        (str, optional)       : 输出位置. Defaults to "test.ass".

        lan_name   (str, optional)       : 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）".

        lan_code   (str, optional)       : 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh"

        credential (Credential, optional): Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处
    """
    # 目测必须得有 Credential 才能获取字幕
    subtitle_data_obj = await request_subtitle(obj=obj, page_index=page_index, cid=cid, lan_name=lan_name, lan_code=lan_code, credential=credential)
        
    subtitle_ass_str = subtitle_data_obj.to_simple_json_str()
    
    with open(out, "w+", encoding="utf-8") as file:
        file.write(subtitle_ass_str)
    
# 下面是弹幕处理

def _export_ass_from_xml(
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

async def make_ass_file_danmakus_protobuf(
    obj: Union[Video, Episode, CheeseVideo],
    page: int = 0,
    out="test.ass",
    cid: Union[int, None] = None,
    date=None,
    font_name="Simsun",
    font_size=25.0,
    alpha=1,
    fly_time=7,
    static_time=5,
) -> None:
    """
    生成视频弹幕文件

    弹幕数据来源于 protobuf 接口

    编码默认采用 utf-8

    Args:
        obj         (Union[Video,Episode,CheeseVideo])       : 对象

        page        (int, optional)                          : 分 P 号. Defaults to 0.

        out         (str, optional)                          : 输出文件. Defaults to "test.ass"

        cid         (int | None, optional)                   : cid. Defaults to None.

        date        (datetime.date, optional)                : 获取时间. Defaults to None.

        font_name   (str, optional)                          : 字体. Defaults to "Simsun".

        font_size   (float, optional)                        : 字体大小. Defaults to 25.0.

        alpha       (float, optional)                        : 透明度(0-1). Defaults to 1.

        fly_time    (float, optional)                        : 滚动弹幕持续时间. Defaults to 7.

        static_time (float, optional)                        : 静态弹幕持续时间. Defaults to 5.
    """
    if isinstance(obj, Video):
        v = obj
        if isinstance(obj, Episode):
            cid = 0
        else:
            if cid is None:
                if page is None:
                    raise ArgsException("page_index 和 cid 至少提供一个。")
                # type: ignore
                cid = await v._Video__get_cid_by_index(page)
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
        raise ArgsException("请传入 Video/Episode/CheeseVideo 类！")
    with open(gettempdir() + "/danmaku_temp.xml", "w+", encoding="utf-8") as file:
        file.write("<i>")
        for d in danmakus:
            file.write(d.to_xml())
        file.write("</i>")
    _export_ass_from_xml(
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

    弹幕数据来源于 xml 接口

    编码默认采用 utf-8

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
                cid = await v._Video__get_cid_by_index(page)  # type: ignore
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
        raise ArgsException("请传入 Video/Episode/CheeseVideo 类！")
    with open(gettempdir() + "/danmaku_temp.xml", "w+", encoding="utf-8") as file:
        file.write(xml_content)
    _export_ass_from_xml(
        gettempdir() + "/danmaku_temp.xml",
        out,
        stage_size,
        font_name,
        font_size,
        alpha,
        fly_time,
        static_time,
    )
