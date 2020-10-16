# video 模块

`from bilibili_api import video`

该模块可以获取视频信息（弹幕，评论，播放量等），对视频进行操作（点赞、投币等）。

## 通用名词解释

aid: av号，即b站改版之前用于标识视频的唯一ID。

bvid: bv号，即b站改版之后用于标识视频的唯一ID。和aid可以互转

**如无特殊说明，下面所有方法中默认需要传入bvid和aid中的其中一个，之后的参数不再赘述。**

## 方法

### get_video_info

获取视频投币，点赞，up主等信息。

| 参数名    | 类型 | 必须提供 | 默认  | 释义                      |
| --------- | ---- | -------- | ----- | ------------------------- |
| is_simple | bool | True     | False | 简易信息，将调用另一个API |

### get_danmaku

获取弹幕信息。

| 参数名 | 类型          | 必须提供 | 默认       | 释义                                                         |
| ------ | ------------- | -------- | ---------- | ------------------------------------------------------------ |
| page   | int           | False    | 0          | 分p，从0开始                                                 |
| date   | datetime.date | False    | 今天的日期 | 弹幕日期，查询历史弹幕索引参见 [get_history_danmaku_index](#get_history_danmaku_index) |

返回 [Danmaku][Danmaku] 类的列表。

### get_history_danmaku_index

获取历史弹幕日期索引。

| 参数名 | 类型          | 必须提供 | 默认   | 释义         |
| ------ | ------------- | -------- | ------ | ------------ |
| page   | int           | False    | 0      | 分p，从0开始 |
| date   | datetime.date | False    | 这个月 | 提供年月即可 |

返回存在历史弹幕的日期列表，例：["2020-01-01", "2020-08-08"]

### get_tags

获取视频标签信息。

### get_chargers

获取视频充电信息。

### get_pages

获取视频分P信息。

### get_download_url

获取视频下载链接。

| 参数名 | 类型 | 必须提供 | 默认 | 释义         |
| ------ | ---- | -------- | ---- | ------------ |
| page   | int  | False    | 0    | 分p，从0开始 |

### get_related

获取相关视频推荐。

### get_added_coins

获取已投币数量。

| 参数名 | 类型   | 必须提供 | 默认 | 释义             |
| ------ | ------ | -------- | ---- | ---------------- |
| verify | Verify | True     | -    | 必须提供SESSDATA |

### get_favorite_list

获取对该视频的收藏情况。

| 参数名 | 类型   | 必须提供 | 默认 | 释义             |
| ------ | ------ | -------- | ---- | ---------------- |
| verify | Verify | True     | -    | 必须提供SESSDATA |

### is_liked

是否已点赞。

| 参数名 | 类型   | 必须提供 | 默认 | 释义             |
| ------ | ------ | -------- | ---- | ---------------- |
| verify | Verify | True     | -    | 必须提供SESSDATA |

### is_favoured

是否已收藏。

| 参数名 | 类型   | 必须提供 | 默认 | 释义             |
| ------ | ------ | -------- | ---- | ---------------- |
| verify | Verify | True     | -    | 必须提供SESSDATA |

### set_like

设置视频点赞状态

| 参数名 | 类型 | 必须提供 | 默认 | 释义     |
| ------ | ---- | -------- | ---- | -------- |
| status | bool | False    | True | 是否点赞 |

### add_coins

给视频投币

| 参数名 | 类型 | 必须提供 | 默认 | 释义            |
| ------ | ---- | -------- | ---- | --------------- |
| num    | int  | False    | 1    | 投币数量，1~2个 |
| likr   | bool | False    | True | 同时点赞        |

### operate_favorite

操作对该视频的收藏情况。

| 参数名        | 类型 | 必须提供 | 默认 | 释义                     |
| ------------- | ---- | -------- | ---- | ------------------------ |
| add_media_ids | list | -        | []   | 要添加到的收藏夹ID       |
| del_media_ids | list | -        | []   | 要从收藏夹移除的收藏夹ID |

### 评论相关

参见 [评论信息和操作](/docs/bilibili_api/通用解释#评论信息和操作)，id还是一样传入bvid或aid。

### send_danmaku

发送弹幕。

| 参数名  | 类型               | 必须提供 | 默认 | 释义         |
| ------- | ------------------ | -------- | ---- | ------------ |
| danmaku | [Danmaku][Danmaku] | True     | -    | 要发送的弹幕 |
| page    | int                | False    | 0    | 分p号        |

### add_tag

给视频添加标签。

| 参数名   | 类型 | 必须提供 | 默认 | 释义     |
| -------- | ---- | -------- | ---- | -------- |
| tag_name | str  | True     | -    | 标签名字 |

### del_tag

删除视频标签。

| 参数名 | 类型 | 必须提供 | 默认 | 释义   |
| ------ | ---- | -------- | ---- | ------ |
| tag_id | int  | True     | -    | 标签ID |

### share_to_dynamic

分享视频到动态。

| 参数名  | 类型 | 必须提供 | 默认 | 释义     |
| ------- | ---- | -------- | ---- | -------- |
| content | str  | True     | -    | 动态内容 |


## 上传视频

上传视频步骤略繁琐，故单独在这说明。

一共有三个方法，分别如下：

`video_upload(path, verify)`: 上传视频文件到b站服务器

`video_cover_upload(path, verify)`: 上传视频封面

`video_submit(data, verify)`: 提交投稿

verify传入完全参数，必须提供。

因为投稿参数过多，而且不知道以后会不会变，所以直接传入原始请求参数

提交投稿data参数如下：

```json
{
    "copyright": 1自制2转载,
    "source": "类型为转载时注明转载来源，为自制时删除此键",
    "cover": "封面URL",
    "desc": "简介",
    "desc_format_id": 0,
    "dynamic": "动态信息",
    "interactive": 0,
    "no_reprint": 1为显示禁止转载,
    "subtitles": {
        // 字幕格式，请自行研究
        "lan": "语言",
        "open": 0
    },
    "tag": "标签1,标签2,标签3（英文半角逗号分隔）",
    "tid": 分区ID（channel模块里头可以获取到）,
    "title": "标题",
    "videos": [
        {
            "desc": "描述",
            "filename": "video_upload(返回值)",
            "title": "分P标题"
        }
    ]
}
```

举个栗子

```python
from bilibili_api import video, Verify

verify = Verify("sessdata", "csrf")
# 上传视频
filename = video.video_upload("D:/整活.mp4", verify=verify)
# 上传封面
cover_url = video.video_cover_upload("D:/整活.png", verify=verify)
data = {
    "copyright": 1,
    "cover": cover_url,
    "desc": "无端迫害",
    "desc_format_id": 0,
    "dynamic": "",
    "interactive": 0,
    "no_reprint": 1,
    "subtitles": {
        "lan": "",
        "open": 0
    },
    "tag": "哲学,请问您今天要来点兔子吗,鬼畜调教",
    "tid": 22,
    "title": "请问您今天要来点哲♂学吗",
    "videos": [
        {
            "desc": "",
            "filename": filename,
            "title": "P1"
        }
    ]
}
# 提交投稿
result = video.video_submit(data, verify=verify)

# 成功的话会返回bv号和av号
print(result)

```

[Danmaku]: /docs/bilibili_api/模块/bilibili_api#Danmaku