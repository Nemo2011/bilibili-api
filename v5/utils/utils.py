"""
bilibili_api.utils.utils

通用工具库
"""

import json
import os


def get_api(field: str):
    """
    获取 API

    :param field: API所属分类
    """
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "api", f"{field.lower()}.json"))
    if os.path.exists(path):
        with open(path, encoding="utf8") as f:
            return json.loads(f.read())
