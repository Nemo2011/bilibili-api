# Module video_uploader.py

```python
from bilibili_api import video_uploader
```

Web 端视频上传。

## VideoUploaderPage

分 P 对象

### Functions

#### def \_\_init\_\_()

| name        | type          | description               |
| ----------- | ------------- | ------------------------- |
| path        | str           | 视频流文件路径            |
| title       | str           | 视频标题                  |
| description | str, optional | 视频简介. Defaults to "". |

#### async def get_size()

获取文件大小

**Returns:** int: 文件大小

## class Lines(Enum)

上传线路枚举

可选线路

bupfetch 模式下 kodo 目前弃用 `{'error': 'no such bucket'}`

- BDA2 百度
- QN 七牛
- WS 网宿
- BLDSA bldsa

## class VideoUploaderEvents(Enum)

上传事件枚举

**Events:**

- PRE_PAGE 上传分 P 前

- PREUPLOAD 获取上传信息

- PREUPLOAD_FAILED 获取上传信息失败

- PRE_CHUNK 上传分块前

- AFTER_CHUNK 上传分块后

- CHUNK_FAILED 区块上传失败

- PRE_PAGE_SUBMIT 提交分 P 前

- PAGE_SUBMIT_FAILED 提交分 P 失败

- AFTER_PAGE_SUBMIT 提交分 P 后

- AFTER_PAGE 上传分 P 后

- PRE_COVER 上传封面前

- AFTER_COVER 上传封面后

- COVER_FAILED 上传封面失败

- PRE_SUBMIT 提交视频前

- SUBMIT_FAILED 提交视频失败

- AFTER_SUBMIT 提交视频后

- COMPLETED 完成上传

- ABORTED 用户中止

- FAILED 上传失败

## class VideoPorderShowType(Enum)

**Extends: enum.Enum**

商单形式

- LOGO: Logo
- OTHER: 其他
- SPOKEN_AD: 口播
- PATCH: 贴片
- TVC_IMBEDDED: TVC 植入
- CUSTOMIZED_AD: 定制软广
- PROGRAM_SPONSORSHIP: 节目赞助
- SLOGAN: SLOGAN
- QR_CODE: 二维码
- SUBTITLE_PROMOTION: 字幕推广


## class VideoPorderType(Enum)

**Extends: enum.Enum**

视频商业类型

+ FIREWORK: 花火
+ OTHER: 其他

## class VideoPorderIndustry(Enum):

**Extends: enum.Enum**

商单行业

+ MOBILE_GAME: 手游
+ CONSOLE_GAME: 主机游戏
+ WEB_GAME: 网页游戏
+ PC_GAME: PC单机游戏
+ PC_NETWORK_GAME: PC网络游戏
+ SOFTWARE_APPLICATION: 软件应用
+ DAILY_NECESSITIES_AND_COSMETICS: 日用品化妆品
+ CLOTHING_SHOES_AND_HATS: 服装鞋帽
+ LUGGAGE_AND_ACCESSORIES: 箱包饰品
+ FOOD_AND_BEVERAGE: 食品饮料
+ PUBLISHING_AND_MEDIA: 出版传媒
+ COMPUTER_HARDWARE: 电脑硬件
+ OTHER: 其他
+ MEDICAL: 医疗类
+ FINANCE: 金融


## class VideoPorderMeta

商业相关参数

### Attributes

| name        | type                      | description    |
| ----------- | ------------------------- | -------------- |
| flow_id     | int                       | 流 ID          |
| industry_id | Optional[int]             | 可选，行业 ID  |
| official    | Optional[int]             | 可选，官方 ID  |
| brand_name  | Optional[str]             | 可选，品牌名称 |
| show_types  | List[VideoPorderShowType] | 展示类型列表   |

### Functions

#### def \_\_init\_\_()

| name          | type                           | description |
| ------------- | ------------------------------ | ----------- |
| porden_type   | VideoPorderType                | 视频商业类型，默认为花火 |
| industry_type | VideoPorderIndustry            | 行业类型，默认为 None |
| brand_name    | Optional[str]                  | 可选，品牌名称，默认为 None |
| show_types    | List[VideoPorderShowType]                      | 展示类型列表，默认为 None |

## class VideoMeta

视频上传参数

### Functions

#### def \_\_init\_\_()

| name               | type                           | description                              |
| ------------------ | ------------------------------ | ---------------------------------------- |
| tid                | int                            | 分区 ID。可以使用 channel 模块进行查询。 |
| title              | str                            | 视频标题                                 |
| desc               | str                            | 视频简介                                 |
| cover              | Picture                        | 封面 URL                                 |
| original           | bool                           | 可选，是否为原创视频                     |
| tags               | Union[List[str], str]          | 使用英文半角逗号分隔的标签组             |
| topic_id           | Optional[int]                  | 可选，话题 ID                            |
| mission_id         | Optional[int]                  | 可选，任务 ID                            |
| source             | Optional[str]                  | 可选，视频来源                           |
| recreate           | Optional[bool]                 | 可选，是否允许重新上传                   |
| no_reprint         | Optional[bool]                 | 可选，是否禁止转载                       |
| open_elec          | Optional[bool]                 | 可选，是否展示充电信息                   |
| up_selection_reply | Optional[bool]                 | 可选，是否开启评论精选                   |
| up_close_danmu     | Optional[bool]                 | 可选，是否关闭弹幕                       |
| up_close_reply     | Optional[bool]                 | 可选，是否关闭评论                       |
| lossless_music     | Optional[bool]                 | 可选，是否启用无损音乐                   |
| dolby              | Optional[bool]                 | 可选，是否启用杜比音效                   |
| subtitle           | Optional[dict]                 | 可选，字幕设置                           |
| dynamic            | Optional[str]                  | 可选，动态信息                           |
| neutral_mark       | Optional[str]                  | 可选，创作者声明                         |
| delay_time         | Optional[Union[int, datetime]] | 可选，定时发布时间戳（秒）               |
| porder             | Optional[VideoPorderMeta]      | 可选，商业相关参数                       |

#### async def verify()

验证参数，需要传入凭据

检测 tags、delay_time、topic -> mission、cover 和 tid

验证失败会抛出异常

| name       | type                         | description             |
| ---------- | ---------------------------- | ----------------------- |
| credential | Credential \| None, optional | 凭据. Defaults to None. |

**Returns:** bool: 是否验证通过

## class VideoUploader(asyncEvent)

上传视频

### Functions

#### def \_\_init\_\_()

| name       | type                    | description                                 |
| ---------- | ----------------------- | ------------------------------------------- |
| pages      | List[VideoUploaderPage] | 分 P 列表                                   |
| meta       | dict, VideoMeta         | 视频信息，建议传入 `VideoMeta` 对象         |
| credential | Credential              | 凭据                                        |
| cover      | str \| Picture          | 路径，传入 meta 类型为 `VideoMeta` 时可不传 |
| line       | Lines                   | 上传线路，不选择则自动测速选择              |

`meta` 建议传入 `VideoMeta` 对象，避免参数有误

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

---

## async def get_missions()

| name       | type                         | description             |
| ---------- | ---------------------------- | ----------------------- |
| tid        | int, optional                | 分区 ID. Defaults to 0. |
| credential | Credential \| None, optional | 凭据. Defaults to None. |

获取活动信息

**Returns:** dict: API 调用返回结果

---

## class VideoEditorEvents

**Extends: enum.Enum**

- PRELOAD : 加载数据前
- AFTER_PRELOAD : 加载成功
- PRELOAD_FAILED: 加载失败
- PRE_COVER : 上传封面前
- AFTER_COVER : 上传封面后
- COVER_FAILED : 上传封面失败
- PRE_SUBMIT : 提交前
- AFTER_SUBMIT : 提交后
- SUBMIT_FAILED : 提交失败
- COMPLETED : 完成
- ABOTRED : 停止
- FAILED : 失败

---

## class VideoEditor

**Extends: AsyncEvent**

### Attributes

| name       | type               | description                             |
| ---------- | ------------------ | --------------------------------------- |
| bvid       | str                | 稿件 BVID                               |
| meta       | dict               | 视频信息                                |
| cover_path | str                | 封面路径. Defaults to None(不更换封面). |
| credential | Credential \| None | 凭据类. Defaults to None.               |

### Functions

#### def \_\_init\_\_()

| name       | type           | description                             |
| ---------- | -------------- | --------------------------------------- |
| bvid       | str            | 稿件 BVID                               |
| meta       | dict           | 视频信息                                |
| cover      | str \| Picture | 封面路径. Defaults to None(不更换封面). |
| credential | Credential     | 凭据类. Defaults to None.               |

meta 参数示例: (保留 video, cover, tid, aid 字段)

```json
{
  "title": "str: 标题",
  "copyright": "int: 是否原创，0 否 1 是",
  "tag": "标签. 用,隔开. ",
  "desc_format_id": "const int: 0",
  "desc": "str: 描述",
  "dynamic": "str: 动态信息",
  "interactive": "const int: 0",
  "new_web_edit": "const int: 1",
  "act_reserve_create": "const int: 0",
  "handle_staff": "const bool: false",
  "topic_grey": "const int: 1",
  "no_reprint": "int: 是否显示“未经允许禁止转载”. 0 否 1 是",
  "subtitles # 字幕设置": {
    "lan": "str: 字幕投稿语言，不清楚作用请将该项设置为空",
    "open": "int: 是否启用字幕投稿，1 or 0"
  },
  "web_os": "const int: 2"
}
```

#### async def start()

开始更改

**Returns:** dict: 返回带有 bvid 和 aid 的字典。

#### async def abort()

中断更改
