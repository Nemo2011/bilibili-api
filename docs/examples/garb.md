# 示例：搜索装扮/收藏集

``` python
from bilibili_api import garb, sync


async def main():
    ## 1. 使用 raw 函数返回原始字典
    raw = await garb.search_garb_dlc_raw(keyword="真白花音")
    for obj in raw["list"]:
        print(obj["name"])
        # obj 字典存在 item_id 键
        if obj["item_id"] == 0:
            # 此时对应收藏集
            props = obj["properties"]
            # 对收藏集十分重要的属性 act_id 即位于 props 中
            print("act_id", props["dlc_act_id"])
        else:
            # 此时对应装扮，装扮的 item_id 即为此处 item_id
            print("item_id", obj["item_id"])
    # 此种方式需要自行判断返回的是收藏集还是装扮，并自己初始化 Garb / DLC 类
    ## 2. 可以使用 obj 函数返回 Garb / DLC 对象
    objs = await garb.search_garb_dlc_obj(keyword="真白花音")
    for obj in objs:
        if isinstance(obj, garb.Garb):
            print("item_id", obj.get_item_id())
        elif isinstance(obj, garb.DLC):
            print("act_id", obj.get_act_id())
        else:
            raise
    # 此种方式可以直接返回模块中对应的 Garb / DLC 类。
    # 但若要在不进一步请求的情况下，还要知道所有对象的大致信息，则做不到。
    # 事实上，raw 函数返回数据中包含所有对象的大致信息，但是 obj 函数会自动取舍掉这部分内容
    # 虽然可以进一步调用对象函数获取相关信息，但需要额外的网络请求
    # *** DLC 对象存在 lottery_id，在部分接口有用处，raw 函数返回数据中便包含所有收藏集的 lottery_id ***
    # *** 如果自行初始化 DLC 对象，则需进行一次网络请求获取 lottery_id，因此使用此函数可以节省后续 DLC 的函数调用时获取 lottery_id 的请求的开销 ***
    ## 3. 返回原始字典和 Garb / DLC 对象
    for raw, obj in await garb.search_garb_dlc(keyword="真白花音"):
        print(raw["name"], end=" ")
        if isinstance(obj, garb.Garb):
            print(obj.get_item_id())
        elif isinstance(obj, garb.DLC):
            print(obj.get_act_id())
        else:
            raise
    # 这种方式同时返回 raw 函数的数据和 obj 函数的对象，可同时满足两种需求，且只进行一次网络请求

    ## 共三个函数，对应三种返回值：
    # search_garb_dlc_raw
    # search_garb_dlc_obj
    # search_garb_dlc
    ## get_garb_dlc_items 相关三个函数的设计与这里同理

sync(main())
```

# 示例：下载收藏集卡片

``` python
from bilibili_api import garb, sync, Picture, select_client


select_client("httpx") # 增加成功率


async def main():
    # act_id 获取方式：看链接
    # https://www.bilibili.com/blackboard/activity-Mz9T5bO5Q3.html?id=154&type=dlc&f_source=ogv&from=video.task
    # url 参数中 id 字段即为 act_id
    dlc = garb.DLC(act_id=154)
    detail = await dlc.get_detail()
    for item in detail["item_list"]:
        url = item["card_info"]["card_img"]
        out = item["card_info"]["card_name"] + ".png"
        (await Picture.load_url(url=url)).to_file(path=out)


sync(main())
```
