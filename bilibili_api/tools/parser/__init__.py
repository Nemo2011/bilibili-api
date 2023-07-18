from .parser import Parser
from .app import get_fastapi, bilibili_api_web

__all__ = [
    "bilibili_api_web",
    "get_fastapi",
    "Parser",
]