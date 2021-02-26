"""
bilibili_api.video

视频相关操作
"""

from .utils.Credential import Credential
from .exceptions import VideoNoIdException, VideoInvalidIdException
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.utils import get_api
from .utils.network import request
import re

API = get_api("video")


class Video:
    """
    视频类，各种对视频的操作均在里面
    """
    def __init__(self, bvid: str = None, aid: int = None, credential: Credential = None):
        """
        :param bvid: BV号，以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）
        :param aid: AV号，大于 0 的整数（若已提供 bvid 则该参数无效）
        :param credential: Credential 类，用于一些操作的凭据认证
        """
        # ID 检查
        if bvid is not None:
            # 检查 bvid 是否有效
            if not re.search("^BV[a-zA-Z0-9]{10}$", bvid):
                raise VideoInvalidIdException("bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）")
            self.bvid = bvid
            # 计算并替换正确的 aid
            self.aid = bvid2aid(self.bvid)

        elif aid is not None:
            if aid <= 0:
                raise VideoInvalidIdException("aid 不能小于或等于 0")
            self.aid = aid
            # 计算并替换 BVID
            self.bvid = aid2bvid(aid)

        else:
            # 未提供任一 ID
            raise VideoNoIdException()

        # 未提供 credential 时初始化该类
        if credential is None:
            self.credential = Credential()

        # 用于存储视频信息，避免接口依赖视频信息时重复调用
        self.__info = None

    async def get_info(self):
        """
        获取视频信息
        """
        url = API["info"]["detail"]["url"]
        params = {
            "bvid": self.bvid
        }
        resp = await request("GET", url, params=params, credential=self.credential)
        # 存入 self.__info 中以备后续调用
        self.__info = resp
        return resp
