import json

from bilibili_api import sync, get_client, Credential

data = sync(
    get_client().request(
        url="https://api.bilibili.com/x/mv/tag",
        method="GET",
        cookies=sync(Credential().get_cookies()),
    )
).json()

print(json.dumps(data, indent=4, ensure_ascii=False))
