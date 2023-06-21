"""
bilibili_api.article_category

专栏分类相关
"""
import os
from typing import List, Tuple, Optional
import copy
import json
from .utils.network_httpx import request
from .utils.utils import get_api
from enum import Enum


API = get_api("article-category")


class ArticleOrder(Enum):
    """
    专栏排序方式.

    + DEFAULT: 默认
    + TIME: 投稿时间排序
    + LIKE: 点赞数最多
    + COMMENTS: 评论数最多
    + FAVORITES: 收藏数最多
    """

    DEFAULT = 0
    TIME = 1
    LIKE = 2
    COMMENTS = 3
    FAVORITES = 4


def get_category_info_by_id(id: int) -> Tuple[Optional[dict], Optional[dict]]:
    """
    获取专栏分类信息

    Args:
        id (int): id

    Returns:
        Tuple[dict | None, dict | None]: 第一个是主分区，第二个是字分区。没有找到则为 (None, None)
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/article_category.json"),
        encoding="utf-8",
    ) as f:
        data = json.loads(f.read())

    for main_category in data:
        if main_category["id"] == id:
            return main_category, None
        for sub_category in main_category["children"]:
            if sub_category["id"] == id:
                return main_category, sub_category
    else:
        return None, None


def get_category_info_by_name(name: str) -> Tuple[Optional[dict], Optional[dict]]:
    """
    获取专栏分类信息

    Args:
        name (str): 分类名

    Returns:
        Tuple[dict | None, dict | None]: 第一个是主分区，第二个是字分区。没有找到则为 (None, None)
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/article_category.json"),
        encoding="utf-8",
    ) as f:
        data = json.loads(f.read())

    for main_category in data:
        if main_category["name"] == name:
            return main_category, None
        for sub_category in main_category["children"]:
            if sub_category["name"] == name:
                return main_category, sub_category
    else:
        return None, None


def get_categories_list() -> List[dict]:
    """
    获取所有的分类的数据

    Returns:
        List[dict]: 所有分区的数据
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/article_category.json"),
        encoding="utf-8",
    ) as f:
        data = json.loads(f.read())
    categories_list = []
    for main_category in data:
        main_category_copy = copy.copy(main_category)
        categories_list.append(main_category_copy)
        main_category_copy.pop("children")
        for sub_category in main_category["children"]:
            sub_category_copy = copy.copy(sub_category)
            sub_category_copy["father"] = main_category_copy
            categories_list.append(sub_category_copy)
    return categories_list


def get_categories_list_sub() -> dict:
    """
    获取所有分区的数据

    含父子关系（即一层次只有主分区）

    Returns:
        dict: 所有分区的数据
    """
    with open(
        os.path.join(os.path.dirname(__file__), "data/article_category.json"),
        encoding="utf-8",
    ) as f:
        return json.loads(f.read())


async def get_category_recommend_articles(
    category_id: int = 0,
    order: ArticleOrder = ArticleOrder.DEFAULT,
    page_num: int = 1,
    page_size: int = 20,
) -> dict:
    """
    获取指定分区的推荐文章

    Args:
        category_id (int)         : 专栏分类的 id, 0 为全部. Defaults to 0.

        order       (ArticleOrder): 排序方式. Defaults to ArticleOrder.DEFAULT.

        page_num    (int)         : 页码. Defaults to 1.
        
        page_size   (int)         : 每一页数据大小. Defaults to 20.

    Returns:
        dict: 调用 API 返回的结果
    """
    api = API["info"]["recommends"]
    params = {"cid": category_id, "sort": order.value, "pn": page_num, "ps": page_size}
    return await request("GET", api["url"], params=params)
