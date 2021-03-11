r"""
模块：channel
功能：频道相关
项目GitHub地址：https://github.com/Passkou/bilibili_api
   _____                _____    _____   _  __   ____    _    _
 |  __ \      /\      / ____|  / ____| | |/ /  / __ \  | |  | |
 | |__) |    /  \    | (___   | (___   | ' /  | |  | | | |  | |
 |  ___/    / /\ \    \___ \   \___ \  |  <   | |  | | | |  | |
 | |       / ____ \   ____) |  ____) | | . \  | |__| | | |__| |
 |_|      /_/    \_\ |_____/  |_____/  |_|\_\  \____/   \____/4
"""

import json
import os
from .exceptions import ArgsException
from .utils.utils import get_api
from .utils.network import request

API = get_api("channel")


class Channel:
    """
    频道类，各种对频道的操作均在里面。
    """

    def __init__(self, tid: int = None, name: str = None):
        """
        Args:
            tid (int, optional):               tid. tid 和 name 必须提供其中之一。
            name (str, optional):                name. tid 和 name 必须提供其中之一。
        """

        # 用于存储频道信息
        self.__info = None

        # ID 检查
        if tid is not None:
            self.set_tid(tid)
        elif name is not None:
            self.set_name(name)
        else:
            # tid和name均未提供
            raise ArgsException("请至少提供 tid 和 name 中的其中一个参数。")

    def set_tid(self, tid: int):
        """
        设置 tid
        Args:
            tid (int):   要设置的 tid。
        """
        with open(os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8") as f:
            channel = json.loads(f.read())

        for main_ch in channel:
            if "tid" not in main_ch:
                continue
            if tid == int(main_ch["tid"]):
                self.__tid = tid
                self.__name = main_ch["name"]
                self.__info = main_ch
                return
            for sub_ch in main_ch["sub"]:
                if "tid" not in sub_ch:
                    continue
                if tid == int(sub_ch["tid"]):
                    self.__tid = tid
                    self.__name = sub_ch["name"]
                    self.__info = sub_ch
                    return
        else:
            raise ArgsException("请输入正确的tid。")

    def set_name(self, name: str):
        """
        设置 频道名
        Args:
            name (str):   要设置的 name。
        """
        with open(os.path.join(os.path.dirname(__file__), "data/channel.json"), encoding="utf8") as f:
            channel = json.loads(f.read())

        for main_ch in channel:
            if "name" not in main_ch:
                continue
            if name == main_ch["name"]:
                self.__tid = main_ch["tid"]
                self.__name = name
                self.__info = main_ch
                return
            for sub_ch in main_ch["sub"]:
                if "name" not in sub_ch:
                    continue
                if name == sub_ch["name"]:
                    self.__tid = sub_ch["tid"]
                    self.__name = name
                    self.__info = sub_ch
                    return
        else:
            raise ArgsException("请输入正确的频道名。")

    def get_tid(self):
        """
        获取 tid。

        Returns:
            tid。
        """
        return self.__tid

    def get_name(self):
        """
        获取 name。

        Returns:
            name。
        """
        return self.__name

    def get_info(self):
        """
        获取分区信息（不再返回上级分区信息）。

        Returns:
            info。
        """
        return self.__info

    async def get_top10(self, day: int = 7):
        """
        获取分区前十排行榜
        :param tid: 0为主页
        :param day: 3天或7天排行榜
        :return:
        """
        if day not in (3, 7):
            raise ArgsException("day只能是3，7")

        url = API["ranking"]["get_top10"]["url"]
        params = {
            "rid": self.__tid,
            "day": day
        }
        resp = await request("GET", url, params=params)
        return resp
