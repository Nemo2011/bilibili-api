# Module ass.py

``` python
from bilibili_api import ass
```

## async def make_ass_file_danmakus_protobuf()

| name | type | description |
| ---- | ---- | ----------- |
| obj   |      Union[Video,Episode,CheeseVideo] |  对象  |
| page   |     int, optional                    |  分 P 号. Defaults to 0.  |
| out     |    str, optional                    | 输出文件. Defaults to "test.ass" |
| cid      |   int \| None, optional                    | cid. Defaults to None.  |
| credential |  Credential \| None, optional           | 凭据. Defaults to None.  |
| date      |  datetime.date, optional        | 获取时间. Defaults to None.  |
| font_name  | str, optional                    | 字体. Defaults to "Simsun".  |
| font_size  | float, optional                  | 字体大小. Defaults to 25.0.  |
| alpha      | float, optional                  | 透明度(0-1). Defaults to 1.  |
| fly_time  |  float, optional                  | 滚动弹幕持续时间. Defaults to 7. | 
| static_time | float, optional                  | 静态弹幕持续时间. Defaults to 5. |

生成视频弹幕文件

**采用 protobuf 源**

**Returns**: None

## async def make_ass_file_danmakus_xml()

| name | type | description |
| ---- | ---- | ----------- |
| obj | Union[Video, Episode, CheeseVideo] | 对象 |
| page | (int)                | 分 P 号 |
| out | (str)              | 输出文件. Defaults to "test.ass" |
| cid | (int \| None) | cid. Defaults to None.  |
| font_name | (str)        | 字体. Defaults to "Simsun".  |
| font_size | (float)      | 字体大小. Defaults to 25.0.  |
| alpha | (float)          | 透明度(0-1). Defaults to 1.  |
| fly_time | (float)       | 滚动弹幕持续时间. Defaults to 7.  |
| static_time | (float)    | 静态弹幕持续时间. Defaults to 5.  |

生成视频弹幕文件

**采用 xml 源**

**Returns**: None

## async def make_ass_file_subtitle()

| name | type | description |
| ---- | ---- | ----------- |
| obj | Union[Video, Episode] | 对象 |
| out | str | 输出位置. Defaults to "test.ass".  |
| name | str | 字幕名，如”中文（自动生成）“,是简介的'subtitle'项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）". |

生成视频字幕文件

**Returns**: None
