# Module video_uploader.py


bilibili_api.video_uploader

视频上传


``` python
from bilibili_api import video_uploader
```

---

## class Lines()

**Extend: enum.Enum**

可选线路

bupfetch 模式下 kodo 目前弃用 `{'error': 'no such bucket'}`

+ BDA2：百度
+ QN：七牛
+ WS：网宿
+ BLDSA：bldsa




---

## class VideoEditor()

**Extend: bilibili_api.utils.AsyncEvent.AsyncEvent**

视频稿件编辑


| name | type | description |
| - | - | - |
| bvid | str | 稿件 BVID |
| meta | Dict | 视频信息 |
| cover_path | str | 封面路径. Defaults to None(不更换封面). |
| credential | Credential | 凭据类. Defaults to None. |


### async def abort()

中断更改



**Returns:** None



---

## class VideoEditorEvents()

**Extend: enum.Enum**

视频稿件编辑事件枚举

+ PRELOAD   : 加载数据前
+ AFTER_PRELOAD : 加载成功
+ PRELOAD_FAILED: 加载失败
+ PRE_COVER : 上传封面前
+ AFTER_COVER   : 上传封面后
+ COVER_FAILED  : 上传封面失败
+ PRE_SUBMIT: 提交前
+ AFTER_SUBMIT  : 提交后
+ SUBMIT_FAILED : 提交失败
+ COMPLETED : 完成
+ ABOTRED   : 停止
+ FAILED: 失败




---

## class VideoMeta()

视频源数据




### async def verify()

验证参数是否可用，仅供参考

检测 tags、delay_time、topic -> mission、cover 和 tid

验证失败会抛出异常



**Returns:** None



---

## class VideoPorderIndustry()

**Extend: enum.Enum**

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




---

## class VideoPorderMeta()

视频商业相关参数




---

## class VideoPorderShowType()

**Extend: enum.Enum**

商单形式

+ LOGO: Logo
+ OTHER: 其他
+ SPOKEN_AD: 口播
+ PATCH: 贴片
+ TVC_IMBEDDED: TVC植入
+ CUSTOMIZED_AD: 定制软广
+ PROGRAM_SPONSORSHIP: 节目赞助
+ SLOGAN: SLOGAN
+ QR_CODE: 二维码
+ SUBTITLE_PROMOTION: 字幕推广




---

## class VideoPorderType()

视频商业类型

+ FIREWORK: 花火
+ OTHER: 其他




---

## class VideoUploader()

**Extend: bilibili_api.utils.AsyncEvent.AsyncEvent**

视频上传


| name | type | description |
| - | - | - |
| pages | List[VideoUploaderPage] | 分 P 列表 |
| meta | VideoMeta, Dict | 视频信息 |
| credential | Credential | 凭据 |
| cover_path | str | 封面路径 |
| line | Union[Lines, None] | 线路. Defaults to None. 不选择则自动测速选择 |


### async def abort()

中断上传



**Returns:** None



---

## class VideoUploaderEvents()

**Extend: enum.Enum**

上传事件枚举

Events:
+ PRE_PAGE 上传分 P 前
+ PREUPLOAD  获取上传信息
+ PREUPLOAD_FAILED  获取上传信息失败
+ PRE_CHUNK  上传分块前
+ AFTER_CHUNK  上传分块后
+ CHUNK_FAILED  区块上传失败
+ PRE_PAGE_SUBMIT  提交分 P 前
+ PAGE_SUBMIT_FAILED  提交分 P 失败
+ AFTER_PAGE_SUBMIT  提交分 P 后
+ AFTER_PAGE  上传分 P 后
+ PRE_COVER  上传封面前
+ AFTER_COVER  上传封面后
+ COVER_FAILED  上传封面失败
+ PRE_SUBMIT  提交视频前
+ SUBMIT_FAILED  提交视频失败
+ AFTER_SUBMIT  提交视频后
+ COMPLETED  完成上传
+ ABORTED  用户中止
+ FAILED  上传失败




---

## class VideoUploaderPage()

分 P 对象




### def get_size()

获取文件大小



**Returns:** int: 文件大小




---

## async def get_available_topics()

获取可用 topic 列表



**Returns:** None



---

## async def get_missions()

获取活动信息


| name | type | description |
| - | - | - |
| tid | Union[int, None] | 分区 ID. Defaults to 0. |
| credential | Union[Credential, None] | 凭据. Defaults to None. |

**Returns:** dict API 调用返回结果




---

## async def upload_cover()

上传封面



**Returns:** str: 封面 URL




