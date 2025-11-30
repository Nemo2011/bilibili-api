import json
import time

import httpx

from bilibili_api import Credential, emoji, sync

PATH_TO_CREDENTIAL_JSON = "test1.json"

data = json.load(open(PATH_TO_CREDENTIAL_JSON, "r"))
cred = Credential(
    sessdata=data["SESSDATA"],
    bili_jct=data["bili_jct"],
    buvid3=data["buvid3"],
    ac_time_value=data["ac_time_value"],
)

res1 = sync(emoji.get_all_emoji(credential=cred))


ids = []
for pkg in res1["all_packages"][1:]:
    ids.append(pkg["id"])

data = {}
for seg in range(0, len(ids), 10):
    print(f"{seg} ~ {seg + 9}")
    res2 = sync(emoji.get_emoji_detail(ids[seg : seg + 10]))
    time.sleep(0.8)
    for pkg in res2["packages"]:
        if pkg.get("emote"):
            for emj in pkg["emote"]:
                data[emj["id"]] = emj["text"]

json.dump(data, open("emote.json", "w+"), ensure_ascii=False, indent=4)
