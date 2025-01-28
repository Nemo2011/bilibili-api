# 示例：获取展出信息

``` python
from bilibili_api import show, sync


async def main():
    # https://show.bilibili.com/platform/detail.html?id=75650&from=pc_ticketlist
    print(await show.get_project_info(75650))


sync(main())
```