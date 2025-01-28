# 示例：图文点赞/投币/收藏

注：图文此时可以理解为动态/专栏皮套，点赞/收藏靠动态一模一样的 API （所有图文都属于动态），投币靠专栏 API （专栏都是有对应的图文的）。因此只有图文是专栏的情况下才能投币。

``` python
from bilibili_api import opus, sync, Credential


OPUS_ID = 492064593401566298


async def main():
    op = opus.Opus(
        OPUS_ID,
        credential=Credential(
            sessdata="",
            bili_jct="",
        ),
    )
    await op.set_like(True)
    print("点赞成功。")
    if await op.is_article():
        await op.add_coins()
        print("投币成功。")
    await op.set_favorite(True)
    print("收藏成功。")


sync(main())
```

# 示例：专栏转为 markdown

专栏都有对应的图文，而且专栏内容目前阶段只能通过解析 html 方式获得，而图文内容是以 REST API 进行传递的，二者经过模块处理后得出的 markdown 有略微不同，可自行对比选择更佳版本。

``` python
# 已知图文求专栏

from bilibili_api import opus, sync, Credential


OPUS_ID = 492064593401566298


async def main():
    op = opus.Opus(OPUS_ID)
    with open("opus.md", "w+") as file:
        file.write(await op.markdown())
    ar = await op.turn_to_article()
    await ar.fetch_content()
    with open("article.md", "w+") as file:
        file.write(ar.markdown())


sync(main())
```

``` python
# 已知专栏求图文

from bilibili_api import article, sync, Credential


CVID = 9841312


async def main():
    ar = article.Article(cvid=CVID)
    await ar.fetch_content()
    with open("article.md", "w+") as file:
        file.write(ar.markdown())
    op = await ar.turn_to_opus()
    with open("opus.md", "w+") as file:
        file.write(await op.markdown())


sync(main())
```
