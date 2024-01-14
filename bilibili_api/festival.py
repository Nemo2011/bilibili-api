"""
bilibili_api.festival

节日专门页相关
"""

from typing import Optional
from .utils.credential import Credential
from .utils.initial_state import get_initial_state
from .video import Video

class Festival:
    """
    节日专门页

    Attributes:
        fes_id     (str)       : 节日专门页编号
        credential (Credential): 凭证类
    """
    def __init__(self, fes_id: str, credential: Optional[Credential] = None) -> None:
        """
        Args:
            fes_id (str): 节日专门页编号
            credential (Credential, optional): 凭据类. Defaults to None.
        """
        self.fes_id = fes_id
        self.credential = credential if credential else Credential()

    async def get_info(self) -> dict:
        """
        获取节日信息

        Returns:
            dict: 调用 API 返回的结果
        """
        return (await get_initial_state(
            f"https://www.bilibili.com/festival/{self.fes_id}",
            credential=self.credential
        ))[0]
