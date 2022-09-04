"""
bilibili_api.interactive_video

互动视频相关操作
"""

import copy
import enum
from lib2to3.pytree import Node
from typing import List
from .utils.Credential import Credential
from .utils.utils import get_api
from .utils.network_httpx import request, get_session
from .video import Video
from urllib import parse

API = get_api("interactive_video")


class InteractiveVideo(Video):
    async def get_graph_version(self):
        pass

    async def get_edge_info(self, edge_id: int):
        pass


class InteractiveNode:
    pass


class InteractiveButtonAlign(enum.Enum):
    """
    按钮的文字的位置


    ``` text
    -----
    |xxx|----o (TEXT_LEFT)
    -----

         -----
    o----|xxx| (TEXT_RIGHT)
         -----

    ----------
    |XXXXXXXX| (DEFAULT)
    ----------
    ```

    - DEFAULT
    - TEXT_UP
    - TEXT_RIGHT
    - TEXT_DOWN
    - TEXT_LEFT
    """

    DEFAULT = 0
    TEXT_UP = 1
    TEXT_RIGHT = 2
    TEXT_DOWN = 3
    TEXT_LEFT = 4


class InteractiveNodeJumpingType(enum.Enum):
    """
    对下一节点的跳转的方式

    - ASK    : 选择
    - DEFAULT: 跳转到默认节点
    - READY  : 选择(只有一个选择)
    """

    READY = 1
    DEFAULT = 0
    ASK = 2


class InteractiveVariable:
    def __init__(self, name, var_id, var_value, show: bool = False):
        self.__var_id = var_id
        self.__var_value = var_value
        self.__name = name
        self.__is_show = show

    def get_id(self):
        return self.__var_id

    def get_value(self):
        return self.__var_value

    def is_show(self):
        return self.__is_show

    def get_name(self):
        return self.__name

    def __str__(self):
        return f"{self.__name} {self.__var_value}"


class InteractiveButton:
    def __init__(
        self, text, x, y, align: InteractiveButtonAlign = InteractiveButtonAlign.DEFAULT
    ):
        self.__text = text
        self.__pos = (x, y)
        self.__align = align

    def get_text(self):
        return self.__text

    def get_align(self):
        return self.__align

    def get_pos(self):
        return self.__pos

    def __str__(self):
        return f"{self.__text} {self.__pos}"


class InteractiveJumpingCondition:
    def __init__(self, var: List[InteractiveVariable] = [], command: str = "True"):
        self.__vars = var
        self.__command = command

    def get_result(self):
        if self.__command == "":
            return True
        command = copy.copy(self.__command)
        for var in self.__vars:
            var_name = var.get_id()
            var_value = var.get_value()
            command = command.replace(var_name, str(var_value))
        command = command.replace("&&", " and ")
        command = command.replace("||", " or ")
        command = command.replace("!", " not ")
        command = command.replace("===", "==")
        command = command.replace("!==", "!=")
        command = command.replace("true", "True")
        command = command.replace("false", "False")
        return eval(command)

    def __str__(self):
        return f"{self.__command}"


class InteractiveNode:
    def __init__(
        self,
        video: InteractiveVideo,
        node_id: int,
        cid: int,
        button: InteractiveButton = None,
        command: InteractiveJumpingCondition = InteractiveJumpingCondition(),
        is_default: bool = False
    ):  
        self.__parent = video
        self.__id = node_id
        self.__cid = cid
        self.__button = button
        self.__jumping_command = command
        self.__is_default = is_default

    async def get_vars(self) -> List[InteractiveVariable]:
        edge_info = await self.__parent.get_edge_info(self.__id)
        node_vars = edge_info["hidden_vars"]
        var_list = []
        for var in node_vars:
            var_value = var["value"]
            var_name = var["name"]
            var_show = var["is_show"]
            var_id = var["id_v2"]
            var_list.append(InteractiveVariable(
                var_name, 
                var_id, 
                var_value, 
                var_show
            ))

    async def get_children(self) -> List[InteractiveNode]:
        edge_info = await self.__parent.get_edge_info(self.__id)
        nodes = []
        for node in edge_info["edges"]["questions"][0]["choices"]:
            node_id = node["id"]
            node_cid = node["cid"]
            if "text_align" in node.keys():
                text_align = node["text_align"]
            else:
                text_align = 0
            if "option" in node.keys():
                node_button = InteractiveButton(
                    node["option"], 
                    node.get("x"), 
                    node.get("y"), 
                    text_align
                )
            else:
                node_button = None
            node_condition = InteractiveJumpingCondition(
                await self.get_vars(), 
                node["condition"]
            )
            if "is_default" in node.keys():
                node_is_default = node["is_default"]
            else:
                node_is_default = False
            nodes.append(InteractiveNode(
                self.__parent, 
                node_id, 
                node_cid, 
                node_button, 
                node_condition, 
                node_is_default
            ))
        return nodes

    def is_default(self):
        return self.__is_default

    async def get_jumping_type(self) -> List[InteractiveNodeJumpingType]:
        edge_info = await self.__parent.get_edge_info(self.__id)
        return edge_info["edges"]["questions"][0]["type"]

    def get_node_id(self):
        return self.__id

    def get_cid(self):
        return self.__cid

    def get_self_button(self):
        if self.__button == None:
            return InteractiveButton("", -1, -1)
        return self.__button

    def get_jumping_command(self):
        return self.__jumping_command
    
    def get_video(self):
        return self.__parent

    async def get_info(self):
        return await self.__parent.get_edge_info(self.__id)

    def __str__(self):
        return f"{self.get_node_id()} {self.get_cid()} {self.get_self_button().get_text()}"


class InteractiveGraph:
    def __init__(self, video: InteractiveVideo, skin: dict, root_cid: int):
        self.__parent = video
        self.__skin = skin
        self.__node = InteractiveNode(self.__parent, 1, root_cid)
    
    def get_video(self):
        return self.__parent

    def get_skin(self):
        return self.__skin

    def get_root_node(self):
        return self.__node

    async def get_children(self):
        return await self.__node.get_children()

    async def get_all_nodes(self):
        pass


class InteractiveVideo(Video):
    def __init__(self, bvid=None, aid=None, credential=None):
        super().__init__(bvid, aid, credential)

    async def up_get_ivideo_pages(self):
        """
        获取交互视频的分 P 信息。up 主需要拥有视频所有权。
        Args:
            bvid       (str)       : BV 号.
            credential (Credential): Credential 类.

        Returns:
        dict: 调用 API 返回结果
        """
        credential = self.credential if self.credential else Credential()
        url = API["info"]["videolist"]["url"]
        params = {"bvid": self.get_bvid()}
        return await request("GET", url=url, params=params, credential=credential)

    async def up_submit_story_tree(self, story_tree: str):
        """
        上传交互视频的情节树。up 主需要拥有视频所有权。

        Args:
        story_tree  (str): 情节树的描述，参考 bilibili_storytree.StoryGraph, 需要 Serialize 这个结构

        Returns:
        dict: 调用 API 返回结果
        """
        credential = self.credential if self.credential else Credential()
        url = API["operate"]["savestory"]["url"]
        form_data = {"preview": "0", "data": story_tree, "csrf": credential.bili_jct}
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://member.bilibili.com",
            "Content-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/plain, */*",
        }
        data = parse.urlencode(form_data)
        return await request(
            "POST",
            url=url,
            data=data,
            headers=headers,
            no_csrf=True,
            credential=credential,
        )

    async def get_graph_version(self):
        """
        获取剧情图版本号，仅供 `get_edge_info()` 使用。

        Args:
            bvid (str): bvid
            credential (Credential, optional): [description]. Defaults to None.

        Returns:
            int: 剧情图版本号
        """
        # 取得初始顶点 cid
        bvid = self.get_bvid()
        credential = self.credential if self.credential else Credential()
        v = Video(bvid=bvid, credential=credential)
        page_list = await v.get_pages()
        cid = page_list[0]["cid"]

        # 获取剧情图版本号
        api = "https://api.bilibili.com/x/player/v2"
        params = {"bvid": bvid, "cid": cid}

        resp = await request("GET", api, params, credential=credential)
        return resp["interaction"]["graph_version"]

    async def get_edge_info(self, edge_id: int = None):
        """
        获取剧情图节点信息

        Args:
            bvid          (str)                 : BV 号
            graph_version (int)                 : 剧情图版本号，可使用 get_graph_version() 获取
            edge_id       (int, optional)       : 节点 ID，为 None 时获取根节点信息. Defaults to None.
            credential    (Credential, optional): 凭据. Defaults to None.
        """
        bvid = self.get_bvid()
        credential = self.credential if self.credential is not None else Credential()

        url = API["info"]["edge_info"]["url"]
        params = {"bvid": bvid, "graph_version": (await self.get_graph_version())}

        if edge_id is not None:
            params["edge_id"] = edge_id

        return await request("GET", url, params, credential=credential)

    async def get_cid(self):
        return await super().get_cid(0)

    async def get_pbp(self, cid: int):
        return await super().get_pbp(cid = cid)

    async def get_danmaku_snapshot(self):
        return await super().get_danmaku_snapshot()

    async def get_danmaku_view(self, cid: int = None):
        return await super().get_danmaku_view(cid = cid)

    async def get_danmaku_xml(self, cid: int = None):
        return await super().get_danmaku_xml(cid = cid)

    async def get_danmakus(self, cid: int = None):
        return await super().get_danmakus(cid = cid)

    async def get_graph(self):
        edge_info = await self.get_edge_info(1)
        cid = await self.get_cid()
        return InteractiveGraph(self, edge_info["edges"]["skin"], cid)
