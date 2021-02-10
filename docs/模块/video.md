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
| like   | bool | False    | True | 同时点赞        |

### operate_favorite

操作对该视频的收藏情况。

| 参数名        | 类型 | 必须提供 | 默认 | 释义                     |
| ------------- | ---- | -------- | ---- | ------------------------ |
| add_media_ids | list | -        | []   | 要添加到的收藏夹ID       |
| del_media_ids | list | -        | []   | 要从收藏夹移除的收藏夹ID |

## 弹幕相关

### get_danmaku

获取所有弹幕信息。

page_id，请先调用 get_video_info() ，然后取其中的 \["pages"]\[分P号-1]\["cid"]

| 参数名 | 类型          | 必须提供 | 默认       | 释义                                                         |
| ------ | ------------- | -------- | ---------- | ------------------------------------------------------------ |
| page_id   | int           | True    | -          | 分p id                                                |
| date   | datetime.date | False    | 今天的日期 | 弹幕日期，查询历史弹幕索引参见 [get_history_danmaku_index](#get_history_danmaku_index) |

返回 [Danmaku][Danmaku] 类的列表。

### get_danmaku_g

获取弹幕信息。返回生成器

page_id，请先调用 get_video_info() ，然后取其中的 \["pages"]\[分P号-1]\["cid"]

| 参数名 | 类型          | 必须提供 | 默认       | 释义                                                         |
| ------ | ------------- | -------- | ---------- | ------------------------------------------------------------ |
| page_id   | int           | True    | -          | 分p id                                                |
| date   | datetime.date | False    | 今天的日期 | 弹幕日期，查询历史弹幕索引参见 [get_history_danmaku_index](#get_history_danmaku_index) |

返回 [Danmaku][Danmaku] 类的生成器。

### get_danmaku_view

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息

page_id，请先调用 get_video_info() ，然后取其中的 \["pages"]\[分P号-1]\["cid"]

| 参数名 | 类型          | 必须提供 | 默认       | 释义                                                         |
| ------ | ------------- | -------- | ---------- | ------------------------------------------------------------ |
| page_id   | int           | True    | -          | 分p id                                                |
| date   | datetime.date | False    | 今天的日期 | 弹幕日期，查询历史弹幕索引参见 [get_history_danmaku_index](#get_history_danmaku_index) |

返回对象，自己打印出来看

### get_history_danmaku_index

获取历史弹幕日期索引。

| 参数名 | 类型          | 必须提供 | 默认   | 释义         |
| ------ | ------------- | -------- | ------ | ------------ |
| page   | int           | False    | 0      | 分p，从0开始 |
| date   | datetime.date | False    | 这个月 | 提供年月即可 |

返回存在历史弹幕的日期列表，例：["2020-01-01", "2020-08-08"]

### like_danmaku

点赞弹幕

无需提供bvid, aid

| 参数名 | 类型 | 必须提供 | 默认 | 释义            |
| ------ | ---- | -------- | ---- | --------------- |
| dmid    | int  | True    | -    | 弹幕id |
| oid   | int | True    | - | 分P id，也叫cid        |
| is_like   | bool | False    | True | 是否点赞      |

### has_liked_danmaku

是否已点赞弹幕

无需提供bvid, aid

| 参数名 | 类型 | 必须提供 | 默认 | 释义            |
| ------ | ---- | -------- | ---- | --------------- |
| dmid    | int/list  | True    | -    | 弹幕id，为list时同时查询多个弹幕，为int时只查询一条弹幕 |
| oid   | int | True    | - | 分P id，也叫cid        |

### send_danmaku

发送弹幕。

| 参数名  | 类型               | 必须提供 | 默认 | 释义         |
| ------- | ------------------ | -------- | ---- | ------------ |
| danmaku | [Danmaku][Danmaku] | True     | -    | 要发送的弹幕 |
| page    | int                | False    | 0    | 分p号        |


### 评论相关

参见 [评论信息和操作](/docs/bilibili_api/通用解释#评论信息和操作)，id还是一样传入bvid或aid。

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

`video_upload(path, verify, on_progress=None)`: 上传视频文件到b站服务器

`video_cover_upload(path, verify)`: 上传视频封面

`video_submit(data, verify)`: 提交投稿

**on_progress 说明：**

进度回调，数据格式：

{"event": "事件名", "ok": "是否成功", "data": "附加数据"}

事件名：PRE_UPLOAD，GET_UPLOAD_ID，UPLOAD_CHUNK，VERIFY

---

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

## 类

### VideoOnlineMonitor

通过Websocket实时连接视频房间，可实时获取在线人数、弹幕更新，

#### 初始化参数

| 参数名          | 类型 | 必须提供 | 默认  | 释义                          |
| --------------- | ---- | -------- | ----- | ----------------------------- |
| bvid | str  | False     | None     | bv号（aid和bvid两者必须提供其中一个，bv号优先级更高）                    |
| aid | int  | False     | None     | av号（aid和bvid两者必须提供其中一个）                    |
| debug           | bool | False    | False | 调试模式，将输出详细的信息    |
| should_reconnect         | bool | False    | True  | 异常断开后是否重连 |
| page         | int | False    | 0  | 分P编号，从0开始 |
| event_handler         | Function | False    | None  | 事件处理器，因为事件比较少所以就没像live.LiveDanmaku那样写装饰器了 |

#### 属性

| 属性名 | 类型           | 释义                           |
| ------ | -------------- | ------------------------------ |
| logger | logging.Logger | 日志记录，可以自行设置一些输出 |

#### 方法

##### connect

连接弹幕服务器。

| 参数名          | 类型 | 必须提供 | 默认  | 释义                          |
| --------------- | ---- | -------- | ----- | ----------------------------- |
| return_coroutine | bool  | False     | False     | 返回 Coroutine 类，供用户自行调用协程 |


##### disconnect

断开弹幕服务器连接。

##### get_connect_status

获取连接直播间状态

0未连接，1已连接，3已正常断开，-1异常断开

#### 事件

收到事件时调用用户指定方法，完整例子：

```python
from bilibili_api.video import VideoOnlineMonitor

def event_handler(data):
    print(data)

room = VideoOnlineMonitor(bvid="BV1uv411q7Mv", event_handler=event_handler)

    
if __name__ == "__main__":
    room.connect()
```

常用事件名：

```
ONLINE： 在线人数更新
DANMAKU： 收到实时弹幕
DISCONNECT： 断开连接（传入连接状态码参数）
```

回调数据格式：
```json
{
    "type": "事件名，类型str", 
    "aid": "av号，类型int", 
    "bvid": "bv号，类型str", 
    "data": "事件内容，类型根据事件类型而定"
}
```

需要注意的是收到弹幕时会返回 [Danmaku][Danmaku] 类，已经帮你解析好了。

### 连接多个视频

```python
import bilibili_api

def on_event(data):
    print(data)

room = bilibili_api.video.VideoOnlineMonitor('BV1y54y1k7CB', debug=False, event_handler=on_event)
room1 = bilibili_api.video.VideoOnlineMonitor('BV1y54y1k7CB', debug=False, event_handler=on_event)

if __name__ == '__main__':
    bilibili_api.video.connect_all_VideoOnlineMonitor(room, room1)
    # 用列表解构
    rooms = [room, room1]
    bilibili_api.video.connect_all_VideoOnlineMonitor(*rooms)
```

[Danmaku]: /docs/模块/bilibili_api.md#Danmaku