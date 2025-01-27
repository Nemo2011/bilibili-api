# 示例：下载一个表情下所有表情包

``` python
from bilibili_api import emoji, sync, Credential, Picture


EMOJI_NAME = "孤独摇滚"


async def main():
    credential = Credential(
        sessdata="",
        bili_jct="",
    )
    emojis = await emoji.get_all_emoji(credential=credential)
    for pkg in emojis["all_packages"]:
        # 遍历所有表情
        if pkg["text"] == EMOJI_NAME:
            # 获取表情详情
            detail = await emoji.get_emoji_detail(int(pkg["id"]))
            # 遍历表情包
            for emj in detail["packages"][0]["emote"]:
                url = emj["url"].split("@")[0] # 恢复原图
                (await Picture.load_url(url)).to_file(f'{emj["text"]}.png')
            return


sync(main())
```
