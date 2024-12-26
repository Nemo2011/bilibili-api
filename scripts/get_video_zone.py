import json

import httpx

from bilibili_api.utils.network import HEADERS

data = httpx.get(
    "https://api.bilibili.com/x/kv-frontend/namespace/data?appKey=333.1339&nscode=2",
    headers=HEADERS,
).json()["data"]

res = []

for key, value in data:
    if str(key).startswith("channel.") and key != "channel.all":
        res.append(value)

print(json.dumps(res, indent=4, ensure_ascii=False))
