"""
bilibili_api.opus

图文相关
"""

import enum
import yaml
from typing import Optional
from . import article
from . import dynamic
from . import note
from .utils.credential import Credential
from .utils.network import Api
from .utils.utils import get_api, raise_for_statement
from .utils import cache_pool


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
        self.__is_note = False
        self.__info = None
        self.credential: Credential = credential if credential else Credential()

        if cache_pool.opus_type.get(self.__id):
            self.__is_note = cache_pool.opus_is_note[self.__id]
            self.__type = OpusType(cache_pool.opus_type[self.__id])
        else:
            api = API["info"]["detail"]
            params = {"timezone_offset": -480, "id": self.__id}
            self.__info = (
                Api(**api, credential=self.credential)
                .update_params(**params)
                .result_sync
            )["item"]
            self.__type = OpusType(self.__info["type"])
            self.__is_note = bool(self.__info["modules"][0].get("module_top"))
            cache_pool.opus_is_note[self.__id] = self.__is_note
            cache_pool.opus_type[self.__id] = self.__type.value

    def get_opus_id(self) -> int:
        """
        获取图文 id

        Returns:
            int: 图文 idd
        """
        return self.__id

    def get_type(self):
        """
        获取图文类型(专栏/动态)

        Returns:
            OpusType: 图文类型
        """
        return self.__type

    def turn_to_article(self) -> "article.Article":
        """
        对专栏图文，转换为专栏
        """
        raise_for_statement(self.__type == OpusType.ARTICLE, "仅支持专栏图文")
        if self.__info:
            cvid = int(self.__info["basic"]["rid_str"])
        else:
            cvid = cache_pool.opus_cvid[self.__id]
        cache_pool.article_is_opus[cvid] = 1
        cache_pool.article_dyn_id[cvid] = self.__id
        cache_pool.article_is_note[cvid] = self.is_note()
        return article.Article(cvid=cvid, credential=self.credential)

    def turn_to_dynamic(self) -> "dynamic.Dynamic":
        """
        转为动态
        """
        cache_pool.dynamic_is_opus[self.__id] = 1
        return dynamic.Dynamic(dynamic_id=self.__id, credential=self.credential)

    def is_note(self) -> bool:
        """
        是否为笔记
        """
        return self.__is_note

    def turn_to_note(self) -> "note.Note":
        """
        转为笔记
        """
        raise_for_statement(self.is_note(), "仅支持笔记")
        if self.__info:
            cvid = int(self.__info["basic"]["rid_str"])
        else:
            cvid = cache_pool.opus_cvid[self.__id]
        cache_pool.article_is_opus[cvid] = 1
        cache_pool.article_dyn_id[cvid] = self.__id
        cache_pool.article_is_note[cvid] = self.is_note()
        return note.Note(cvid=cvid, credential=self.credential)

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
        if self.is_note():
            top, title, author, content = self.__info["modules"][:4]
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
