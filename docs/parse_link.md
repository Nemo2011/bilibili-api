# `parse_link` 函数

`parse_link` 函数是 `10.2.0.b4` 时新增的函数。这个函数可以自动解析链接获取对应的对象。

举个例子：如果有一个视频链接，想要获取对应的对象需要读取 `bvid` 或 `aid`，然后初始化 `Video` 类。
但是 `parse_link` 可以自动读取 `bvid` 或 `aid` 并生成对应的对象。

目前 `parse_link` 函数支持解析：

- 视频
- 番剧
- 番剧剧集
- 收藏夹
- 课程视频
- 音频
- 歌单
- 专栏
- 用户

具体的参数、返回值参考[正文](/modules/bilibili_api.md#parse)。

**<span id="example">下面是一个例子： </span>**

``` python
from bilibili_api import parse_link, sync

# -----------------------------------------------------------
# 注意，解析成功的 url 返回的是元组，第一项是对象，第二项是类型      
# -----------------------------------------------------------

video = sync(
    parse_link(
        "https://www.bilibili.com/video/BV1AV411x7Gs?spm_id_from=333.999.0.0&vd_source=596f678272672b05ed4386cfa6c97a16"
    )
) # 解析视频

print(video[1]) # 类型
print(video[0].get_bvid()) # 打印 bvid
print()

# -----------------------------------------------------------

audio_list = sync(
    parse_link(
        "https://www.bilibili.com/audio/am10624?type=2"
    )
) # 歌单 ...

print(audio_list[1]) # ... 也能解析
print(sync(audio_list[0].get_info())) # 打印歌单信息
print()

# -----------------------------------------------------------

user = sync(
    parse_link(
        "https://space.bilibili.com/660303135/dynamic"
    )
) # 用户，内容是用户的动态，但是获取的目标是用户

print(user[0].uid) # 打印 uid
print()

# -----------------------------------------------------------

bad_link = sync(parse_link("doge.wtf"))

print(bad_link) # -1

"""
输出：
ResourceType.VIDEO
BV1AV411x7Gs

ResourceType.AUDIO_LIST
{'menuId': 10624, 'uid': 32708543, 'uname': '大家的音乐姬', 'title': '新曲推荐', 'cover': 'http://i0.hdslb.com/bfs/music/a32c1ed4f6ec3f74f8240f4486a750dda3a509e5.jpg', 'intro': '每天11:00更新，为你推送最新音乐', 'type': 2, 'off': 0, 'ctime': 1501209433, 'curtime': 1656578636, 'statistic': {'sid': 10624, 'play': 2366732, 'collect': 20556, 'comment': 1107, 'share': 622}, 'snum': None, 'attr': 0, 'isDefault': 0, 'collectionId': 0}

660303135

无法查看目标链接！
-1
"""
```
