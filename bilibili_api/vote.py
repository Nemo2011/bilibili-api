"""
bilibili_api.vote

投票相关操作。

需要 vote_id,获取 vote_id: https://nemo2011.github.io/bilibili-api/#/vote_id
"""
from typing import Optional
from enum import Enum
from .utils.utils import get_api
from .utils.network_httpx import request
from .utils.Credential import Credential

API = get_api("vote")

class VoteType(Enum):
    """
    投票类型类

    + TEXT: 文字投票
    + IMAGE: 图片投票
    """
    TEXT = 0
    IMAGE = 1

class VoteChoices:
    """
    投票选项类
    """
    def __init__(self) -> None:
        self.choices = []
    
    def add_choice(self, desc: str, img_url: Optional[str] = None) -> "VoteChoices":
        """
        往 VoteChoices 添加选项

        Args:
            desc (str): 选项描述
            img_url (Optional[str], optional): 选项的图片链接，如果是图片投票. Defaults to None.
        """
        self.choices.append({"desc": desc, "img_url": img_url})
        return self

    def remove_choice(self, index: int) -> "VoteChoices":
        """
        从 VoteChoices 移除选项

        Args:
            index (int): 选项索引
        """
        self.choices.remove(index)
        return self

    def get_choices(self) -> dict:
        """
        获取 VoteChoices 的 choices

        Returns:
            dict: choices
        """
        results = {}
        for i in range(len(self.choices)):
            choice_key_name = f'info[options][{i}]'
            results[f'{choice_key_name}[desc]'] = self.choices[i]["desc"]
            results[f'{choice_key_name}[img_url]'] = self.choices[i]["img_url"]
        return results

class Vote:
    """
    投票类

    Attributes:
        vote_id (int): vote_id, 获取：https://nemo2011.github.io/bilibili-api/#/vote_id
        credential (Credential): 凭据类
    """
    def __init__(self, vote_id: int, credential: Credential = Credential()) -> None:
        """
        Args:
            vote_id (int): vote_id, 获取：https://nemo2011.github.io/bilibili-api/#/vote_id
            credential (Credential): 凭据类.
        """
        self.vote_id = vote_id
        self.credential = credential

    async def get_vote_info(self) -> dict:
        """
        获取投票详情

        Returns:
            dict: 调用 API 返回的结果
        """
        api = API["info"]["vote_info"]
        params = {"vote_id": self.vote_id}
        return await request("GET", api["url"], params=params)

    async def update_vote(self,
        title: str,
        _type: VoteType,
        choice_cnt: int,
        duration: int,
        choices: VoteChoices,
        desc: Optional[str] = None
    ) -> dict:
        """
        更新投票内容

        Args:
            vote_id (int): vote_id
            title (str): 投票标题
            _type (VoteType): 投票类型
            choice_cnt (int): 最多几项
            duration (int): 投票持续秒数 常用: 三天:259200 七天:604800 三十天:2592000
            choices (VoteChoices): 投票选项
            credential (Credential): Credential
            desc (Optional[str], optional): 投票描述. Defaults to None.

        Returns:
            dict: 调用 API 返回的结果
        """
        self.credential.raise_for_no_sessdata()
        api = API["operate"]["update"]
        data = {
            "info[title]": title,
            "info[desc]": desc,
            "info[type]": _type.value,
            "info[choice_cnt]": choice_cnt,
            "info[duration]": duration,
            "info[vote_id]": self.vote_id
        }
        data.update(choices.get_choices())
        if choice_cnt > len(choices.choices):
            raise ValueError("choice_cnt 大于 choices 选项数")
        return await request("POST", api["url"], data=data, credential=self.credential)


async def create_vote(
    title: str,
    _type: VoteType,
    choice_cnt: int,
    duration: int,
    choices: VoteChoices,
    credential: Credential,
    desc: Optional[str] = None
) -> Vote:
    """
    创建投票

    Args:
        title (str): 投票标题
        _type (VoteType): 投票类型
        choice_cnt (int): 最多几项
        duration (int): 投票持续秒数 常用: 三天:259200 七天:604800 三十天:2592000
        choices (VoteChoices): 投票选项
        credential (Credential): Credential
        desc (Optional[str], optional): 投票描述. Defaults to None.

    Returns:
        Vote: Vote 类
    """
    api = API["operate"]["create"]
    data = {"info[title]": title,
    "info[desc]": desc,
    "info[type]": _type.value,
    "info[choice_cnt]": choice_cnt,
    "info[duration]": duration
    }
    data.update(choices.get_choices())
    if choice_cnt > len(choices.choices):
        raise ValueError("choice_cnt 大于 choices 选项数")
    vote_id = (await request("POST", api["url"], data=data, credential=credential))["vote_id"]
    return Vote(vote_id=vote_id, credential=credential)
