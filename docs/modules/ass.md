# Module ass.py


bilibili_api.ass

有关 ASS 文件的操作


``` python
from bilibili_api import ass
```

- [async def make\_ass\_file\_danmakus\_protobuf()](#async-def-make\_ass\_file\_danmakus\_protobuf)
- [async def make\_ass\_file\_danmakus\_xml()](#async-def-make\_ass\_file\_danmakus\_xml)
- [async def make\_ass\_file\_subtitle()](#async-def-make\_ass\_file\_subtitle)

---

## async def make_ass_file_danmakus_protobuf()

生成视频弹幕文件

弹幕数据来源于 protobuf 接口

编码默认采用 utf-8


| name | type | description |
| - | - | - |
| `obj` | `Union[Video,Episode,CheeseVideo]` | 对象 |
| `page` | `int, optional` | 分 P 号. Defaults to 0. |
| `out` | `str, optional` | 输出文件. Defaults to "test.ass" |
| `cid` | `int \| None, optional` | cid. Defaults to None. |
| `date` | `datetime.date, optional` | 获取时间. Defaults to None. |
| `font_name` | `str, optional` | 字体. Defaults to "Simsun". |
| `font_size` | `float, optional` | 字体大小. Defaults to 25.0. |
| `alpha` | `float, optional` | 透明度(0-1). Defaults to 1. |
| `fly_time` | `float, optional` | 滚动弹幕持续时间. Defaults to 7. |
| `static_time` | `float, optional` | 静态弹幕持续时间. Defaults to 5. |




---

## async def make_ass_file_danmakus_xml()

生成视频弹幕文件

弹幕数据来源于 xml 接口

编码默认采用 utf-8


| name | type | description |
| - | - | - |
| `obj` | `Union[Video,Episode,Cheese]` | 对象 |
| `page` | `int, optional` | 分 P 号. Defaults to 0. |
| `out` | `str, optional` | 输出文件. Defaults to "test.ass". |
| `cid` | `int \| None, optional` | cid. Defaults to None. |
| `font_name` | `str, optional` | 字体. Defaults to "Simsun". |
| `font_size` | `float, optional` | 字体大小. Defaults to 25.0. |
| `alpha` | `float, optional` | 透明度(0-1). Defaults to 1. |
| `fly_time` | `float, optional` | 滚动弹幕持续时间. Defaults to 7. |
| `static_time` | `float, optional` | 静态弹幕持续时间. Defaults to 5. |




---

## async def make_ass_file_subtitle()

生成视频字幕文件

编码默认采用 utf-8


| name | type | description |
| - | - | - |
| `obj` | `Union[Video,Episode]` | 对象 |
| `page_index` | `int, optional` | 分 P 索引 |
| `cid` | `int, optional` | cid |
| `out` | `str, optional` | 输出位置. Defaults to "test.ass". |
| `lan_name` | `str, optional` | 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）". |
| `lan_code` | `str, optional` | 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh" |
| `credential` | `Credential, optional` | Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处 |




