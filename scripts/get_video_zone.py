import json

import httpx

from bilibili_api.utils.network import HEADERS

data = httpx.get(
    "https://api.bilibili.com/x/kv-frontend/namespace/data?appKey=333.1339&nscode=2",
    headers=HEADERS,
).json()["data"]["data"]

res = []

for key, value in data.items():
    if str(key).startswith("channel_list.") and key != "channel_list.all":
        res.append(json.loads(value))

print(json.dumps(res, indent=2, ensure_ascii=False))
