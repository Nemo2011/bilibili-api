import json

from bilibili_api import sync
from bilibili_api.exceptions import *
from bilibili_api.utils.initial_state import get_initial_state


async def main() -> None:
    with open("bangumi_index_params.json", "w", encoding="UTF-8") as f:
        content = {}
        content["anime"] = (
            await get_initial_state("https://www.bilibili.com/anime/index/")
        )[0]
        content["movie"] = (
            await get_initial_state("https://www.bilibili.com/movie/index/")
        )[0]
        content["tv"] = (await get_initial_state("https://www.bilibili.com/tv/index/"))[
            0
        ]
        content["documentary"] = (
            await get_initial_state("https://www.bilibili.com/documentary/index/")
        )[0]
        content["variety"] = (
            await get_initial_state("https://www.bilibili.com/variety/index/")
        )[0]
        content["guochuang"] = (
            await get_initial_state("https://www.bilibili.com/guochuang/index/")
        )[0]
        json.dump(content, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    sync(main())
