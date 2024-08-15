import json

import httpx

print(
    json.dumps(
        httpx.get("https://api.bilibili.com/x/mv/tag").json(),
        indent=4,
        ensure_ascii=False,
    )
)
