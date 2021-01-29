# app 模块

客户端相关 API。

## 方法

### get_loading_images

获取开屏启动画面。

| 参数名      | 类型              | 必须提供 | 默认      | 释义                        |
| ----------- | ----------------- | -------- | --------- | --------------------------- |
| build       | int               | False    | 999999999 | 客户端内部版本号            |
| mobi_app    | str               | False    | android   | 可选 android / iphone / ipad|
| platform    | str               | False    | android   | 可选 android / ios    / ios |
| height      | int               | False    | 1920      | 屏幕高度                    |
| width       | int               | False    | 1080      | 屏幕宽度                    |
| birth       | str               | False    | -         | 生日日期(四位数，例 0101)   |

* 补充获取结果关系图

|mobi_app|platform|width|height|结果(width x height)|
|-|-|-|-|-|
|android|android|200|300|320x480|
|android|android|400|700|375x647|
|android|android|300|400|480x640|
|android|android|2900|4400|480x728|
|android|android|300|500|480x800|
|android|android|0|100|480x854|
|android|android|800|1300|600x976|
|android|android|600|900|640x960|
|android|android|1300|2300|640x1136|
|android|android|1100|1800|720x1184|
|android|android|1000|1700|720x1208|
|android|android|900|1600|720x1280|
|iphone|ios|500|900|750x1334|
|android|android|0|0|768x976|
|android|android|900|1200|768x1024|
|android|android|900|1500|768x1280|
|android|android|1700|2600|800x1216|
|android|android|900|1400|800x1232|
|android|android|500|800|800x1280|
|ipad|ios|400|300|1024x768|
|android|android|1700|2800|1080x1776|
|android|android|1080|1920|1080x1920|
|iphone|ios|0|100|1125x2436|
|android|android|1200|2000|1152x1920|
|iphone|ios|900|1600|1242x2208|
|android|android|1800|3200|1440x2560|
|android|android|1500|2000|1536x2048|
|android|android|1500|2500|1536x2560|
|android|android|1500|2400|1600x2560|
|ipad|ios|0|100|2048x1536|
|android|android|500|700|2048x2732|
|ipad|ios|0|0|2732x2048|


### get_loading_images_special

获取特殊开屏启动画面。

| 参数名      | 类型              | 必须提供 | 默认      | 释义                        |
| ----------- | ----------------- | -------- | --------- | --------------------------- |
| appkey      | str               | False    |           | appkey                      |
| mobi_app    | str               | False    | android   | 可选 android / iphone / ipad|
| platform    | str               | False    | android   | 可选 android / ios    / ios |
| height      | int               | False    | 1920      | 屏幕高度                    |
| width       | int               | False    | 1080      | 屏幕宽度                    |
| ts          | int               | False    | (自动获取)| 当前UNIX秒                  |
| appsec      | str               | False    |           | appsec                      |

* appkey 及 appsec 对应关系请参考 [这里](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/other/API_auth.md)