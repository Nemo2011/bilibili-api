"""
bilibili_api.clients
"""

ALL_PROVIDED_CLIENTS = [
    ("curl_cffi", "CurlCFFIClient", {}),
    ("aiohttp", "AioHTTPClient", {}),
    ("httpx", "HTTPXClient", {"http2": False}),
]
