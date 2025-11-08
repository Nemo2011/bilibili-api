import json

from bilibili_api import sync, get_client, Credential

data = sync(
    get_client().request(
        url="https://api.bilibili.com/x/kv-frontend/namespace/data?appKey=333.1339&nscode=2",
        method="GET",
        cookies=sync(Credential().get_cookies()),
    )
).json()["data"]["data"]

res = []

for key, value in data.items():
    if str(key).startswith("channel_list.") and key != "channel_list.all":
        res.append(json.loads(value))

print(json.dumps(res, indent=2, ensure_ascii=False))
