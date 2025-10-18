"""
bilibili_api.clients
"""

ALL_PROVIDED_CLIENTS = [
    ("curl_cffi", "CurlCFFIClient", {"impersonate": "", "http2": False}),
    ("aiohttp", "AioHTTPClient", {}),
    ("httpx", "HTTPXClient", {"http2": False}),
]
