# Module ass.py

``` python
from bilibili_api import ass
```

## _async_ def make_ass_file_danmakus_protobuf()

| name | type | description |
| ---- | ---- | ----------- |
| bvid | (str)             | BVID |
| page | (int)                | 分 P 号 |
| out | (str)              | 输出文件 |
| cid | (int) | cid |
| credential | (Credential)| 凭据 |
| date | (datetime.date)   | 获取时间 |
| stage_size | (tuple|list)| 尺寸，一般都是 1920x1080 |
| font_name | (str)        | 字体 |
| font_size | (float)      | 字体大小 |
| alpha | (float)          | 透明度(0-1) |
| fly_time | (float)       | 滚动弹幕持续时间 |
| static_time | (float)    | 静态弹幕持续时间 |

生成视频弹幕文件 *★,°*:.☆(￣▽￣)/$:*.°★* 。
强烈推荐 PotPlayer, 电影与电视加载后全部都是静态弹幕，不能滚动。
**采用 protobuf 源**

**Returns**: None

## _async_ def make_ass_file_danmakus_xml()

| name | type | description |
| ---- | ---- | ----------- |
| bvid | (str)             | BVID |
| page | (int)                | 分 P 号 |
| out | (str)              | 输出文件 |
| cid | (int) | cid |
| credential | (Credential)| 凭据 |
| date | (datetime.date)   | 获取时间 |
| stage_size | (tuple|list)| 尺寸，一般都是 1920x1080 |
| font_name | (str)        | 字体 |
| font_size | (float)      | 字体大小 |
| alpha | (float)          | 透明度(0-1) |
| fly_time | (float)       | 滚动弹幕持续时间 |
| static_time | (float)    | 静态弹幕持续时间 |

生成视频弹幕文件 *★,°*:.☆(￣▽￣)/$:*.°★* 。
强烈推荐 PotPlayer, 电影与电视加载后全部都是静态弹幕，不能滚动。
**采用 protobuf 源**

**Returns**: None

## _async_ def make_ass_file_subtitle()

| name | type | description |
| ---- | ---- | ----------- |
| bvid | str | 视频 BVID |
| out | str | 输出位置 |
| name | str | 字幕名，如”中文（自动生成）“,是简介的'subtitle'项的'list'项中的弹幕的'lan_doc'属性。|
| credential | Credential | 凭据 |

生成视频字幕文件

**Returns**: None

## _async_ def 