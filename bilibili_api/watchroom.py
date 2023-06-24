"""
bilibili_api.watchroom

放映室相关 API
"""

from .utils.network_httpx import request
from .utils.utils import get_api
from . import Credential

API = get_api("watchroom")

