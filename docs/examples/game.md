# 示例：获取游戏详情

``` python
from bilibili_api import game, sync

g = game.Game(105667)
print(sync(g.get_detail()))
```

# 示例：获取 B 站原神 WIKI 页面源码

``` python
import async_mediawiki as mw # 此库并非十分适配此模块，可能需要简单调教，目前没找到更好的了
from bilibili_api import game, get_aiohttp_session
import asyncio


async def main() -> None:
    # BWIKI 基于 MediaWiki 开发，MediaWiki 会暴露一个 api.php，可以通过此进行获取、操作信息
    # bilibili_api 提供获取 api.php 位置相关的 API，然后就需要交给第三方库来进行具体处理。

    # 首先通过 game.game_name2id("原神") 将游戏名转换为需要的游戏编码
    # 就例如这里 "原神" 对应的编码为 "ys"
    # 然后传入 game.get_wiki_api_root
    # 生成可供第三方库使用的 api 链接
    api_root = game.get_wiki_api_root(await game.game_name2id("原神"))

    # 最后调用第三方库进行操作
    ys_wiki = mw.Wiki(base_url=api_root, session=get_aiohttp_session())
    page = ys_wiki.get_page("胡桃")
    with open("page.txt", "w+") as file:
        file.write(await page.markdown)
    await ys_wiki.close()


if __name__ == '__main__':
    asyncio.run(main())
```
