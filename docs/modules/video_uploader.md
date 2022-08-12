# Module video_uploader.py

```python
from bilibili_api import video_uploader
```

Web 端视频上传。

## VideoUploaderPage

分 P 对象

### Functions

#### def \_\_init\_\_()

| name         | type           | description                      |
| ------------ | -------------- | -------------------------------- |
| path | str | 视频流文件路径                          |
| title        | str            | 视频标题                         |
| description  | str, optional  | 视频简介. Defaults to "".        |

#### async def get_size()

获取文件大小

**Returns:** int: 文件大小

## class VideoUploaderEvents(Enum)

上传事件枚举

 **Events:**

+ PRE_PAGE 上传分 P 前

+ PREUPLOAD 获取上传信息

+ PREUPLOAD_FAILED 获取上传信息失败

+ PRE_CHUNK 上传分块前

+ AFTER_CHUNK 上传分块后

+ CHUNK_FAILED 区块上传失败

+ PRE_PAGE_SUBMIT 提交分 P 前

+ PAGE_SUBMIT_FAILED 提交分 P 失败

+ AFTER_PAGE_SUBMIT 提交分 P 后

+ AFTER_PAGE 上传分 P 后

+ PRE_COVER 上传封面前

+ AFTER_COVER 上传封面后

+ COVER_FAILED 上传封面失败

+ PRE_SUBMIT 提交视频前

+ SUBMIT_FAILED 提交视频失败

+ AFTER_SUBMIT 提交视频后

+ COMPLETED 完成上传

+ ABORTED 用户中止

+ FAILED 上传失败

## class VideoUploader(asyncEvent)

上传视频

### Functions

#### def \_\_init\_\_()

| name         | type                    | description                                                  |
| ------------ | ----------------------- | ------------------------------------------------------------ |
| pages        | list[VideoUploaderPage] | 分 P 列表                                                    |
| meta         | dict                    | 视频信息                                                     |
| credential   | VideoUploaderCredential | 凭据（注意，是 VideoUploaderCredential）                     |
| cover_path | str          | 路径                                                      |

**meta 参数示例：**

```json

{
    "act_reserve_create": "const int: 0",
    "copyright": "int, 投稿类型。1 自制，2 转载。",
    "source": "str: 视频来源。投稿类型为转载时注明来源，为原创时为空。",
    "cover": "str: 封面 URL",
    "desc": "str: 视频简介。",
    "desc_format_id": "const int: 0",
    "dynamic": "str: 动态信息。",
    "interactive": "const int: 0",
    "no_reprint": "int: 显示未经作者授权禁止转载，仅当为原创视频时有效。1 为启用，0 为关闭。",
    "open_elec": "int: 是否展示充电信息。1 为是，0 为否。",
    "origin_state": "const int: 0",
    "subtitles # 字幕设置": {
        "lan": "str: 字幕投稿语言，不清楚作用请将该项设置为空",
        "open": "int: 是否启用字幕投稿，1 or 0"
    },
    "tag": "str: 视频标签。使用英文半角逗号分隔的标签组。示例：标签 1,标签 1,标签 1",
    "tid": "int: 分区 ID。可以使用 channel 模块进行查询。",
    "title": "str: 视频标题",
    "up_close_danmaku": "bool: 是否关闭弹幕。",
    "up_close_reply": "bool: 是否关闭评论。",
    "up_selection_reply": "bool: 是否开启评论精选",
    "videos # 分 P 列表": [
        {
        "title": "str: 标题",
        "desc": "str: 简介",
        "filename": "str: preupload 时返回的 filename"
        }
    ],
    "dtime": "int?: 可选，定时发布时间戳（秒）"
}
```

meta 保留字段：`videos`, `cover`

#### async def start()

开始上传

**Returns:** dict: 返回带有 bvid 和 aid 的字典。

#### async def abort()

中断上传

## async def get_missions()

| name       | type                 | description             |
| ---------- | -------------------- | ----------------------- |
| tid        | int, optional        | 分区 ID. Defaults to 0. |
| credential | Credential, optional | 凭据. Defaults to None. |

获取活动信息

**Returns:** dict: API 调用返回结果
