"""
bilibili_api.opus

图文相关
"""

import enum
import yaml
from typing import Optional
from . import article
from . import dynamic
from .utils.credential import Credential
from .utils.network import Api
from .utils.utils import get_api, raise_for_statement


API = get_api("opus")


class OpusType(enum.Enum):
    """
    图文类型

    + ARTICLE: 专栏
    + DYNAMIC: 动态
    """

    ARTICLE = 1
    DYNAMIC = 0


class Opus:
    """
    图文类。

    Attributes:
        credential (Credential): 凭据类
    """

    def __init__(self, opus_id: int, credential: Optional[Credential] = None):
        self.__id = opus_id
        self.credential = credential if credential else Credential()

        api = API["info"]["detail"]
        params = {"timezone_offset": -480, "id": self.__id}
        self.__info = (
            Api(**api, credential=self.credential).update_params(**params).result_sync
        )["item"]
        self.__type = OpusType(self.__info["type"])

    def get_opus_id(self):
        return self.__id

    def get_type(self):
        """
        获取图文类型(专栏/动态)

        Returns:
            OpusType: 图文类型
        """
        return self.__type

    async def get_info(self):
        """
        获取图文基本信息

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["detail"]
        params = {"timezone_offset": -480, "id": self.__id}
        return (
            await Api(**api, credential=self.credential).update_params(**params).result
        )

    def markdown(self) -> str:
        """
        将图文转为 markdown

        Returns:
            str: markdown 内容
        """
        title, author, content = self.__info["modules"][:3]

        markdown = f'# {title["module_title"]["text"]}\n\n'

        for para in content["module_content"]["paragraphs"]:
            para_raw = ""
            if para["para_type"] == 1:
                for node in para["text"]["nodes"]:
                    raw = node["word"]["words"]
                    if node["word"].get("style"):
                        if node["word"]["style"].get("bold"):
                            if node["word"]["style"]["bold"]:
                                raw = f" **{raw}**"
                    para_raw += raw
            else:
                for pic in para["pic"]["pics"]:
                    para_raw += f'![]({pic["url"]})\n'
            markdown += f"{para_raw}\n\n"

        meta_yaml = yaml.safe_dump(self.__info, allow_unicode=True)
        content = f"---\n{meta_yaml}\n---\n\n{markdown}"
        return content
