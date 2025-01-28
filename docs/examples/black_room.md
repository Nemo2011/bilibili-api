# 示例：小黑屋鉴赏

``` python
from bilibili_api import black_room, sync


async def main():
    for case in await black_room.get_blocked_list():
        with open("test.html", "a") as file:
            # html 下观赏更佳
            file.write(case["originContentModify"])
            file.write("\n")


sync(main())
```
