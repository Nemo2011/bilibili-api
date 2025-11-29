# Module ass.py


bilibili_api.ass

有关 ASS 文件的操作


``` python
from bilibili_api import ass
```

- [class AssSubtitleObject()](#class-AssSubtitleObject)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def get\_lan\_list()](#def-get\_lan\_list)
  - [async def request\_ass\_data\_json()](#async-def-request\_ass\_data\_json)
  - [def to\_ass()](#def-to\_ass)
  - [def to\_lrc()](#def-to\_lrc)
  - [def to\_simple\_json()](#def-to\_simple\_json)
  - [def to\_simple\_json\_str()](#def-to\_simple\_json\_str)
  - [def to\_srt()](#def-to\_srt)
- [async def make\_ass\_file\_danmakus\_protobuf()](#async-def-make\_ass\_file\_danmakus\_protobuf)
- [async def make\_ass\_file\_danmakus\_xml()](#async-def-make\_ass\_file\_danmakus\_xml)
- [async def make\_ass\_file\_subtitle()](#async-def-make\_ass\_file\_subtitle)
- [async def make\_lrc\_file\_subtitle()](#async-def-make\_lrc\_file\_subtitle)
- [async def make\_simple\_json\_file\_subtitle()](#async-def-make\_simple\_json\_file\_subtitle)
- [async def make\_srt\_file\_subtitle()](#async-def-make\_srt\_file\_subtitle)
- [async def request\_subtitle\_languages()](#async-def-request\_subtitle\_languages)
- [async def request\_subtitle()](#async-def-request\_subtitle)

---

## class AssSubtitleObject()





### def \_\_init\_\_()

获取远程字幕


| name | type | description |
| - | - | - |
| `json_lan_list` | `json` | 字幕可选语言 |
| `obj` | `Union[Video,Episode]` | 对象 |
| `lan_set` | `str` | 设置默认字幕语言,如果为None,则自动获取可获取语言 |


### def get_lan_list()

获取字幕语言列表



**Returns:** `Tuple[List[str], List[Optional[str]]]`:  字幕名,字幕语言代码




### async def request_ass_data_json()

获取对应语言的字幕


| name | type | description |
| - | - | - |
| `lan_set` | `str` | 如果为None，则获取默认字幕语言 |

**Returns:** `json`:  字幕数据




### def to_ass()

获取ass格式的字幕



**Returns:** `str`:  ass字幕




### def to_lrc()

获取lrc格式的字幕



**Returns:** `str`:  lrc字幕




### def to_simple_json()

获取简化后的JSON数据



**Returns:** `json`:  字幕数据




### def to_simple_json_str()

获取简化后的JSON字符串



**Returns:** `str`:  获取简化后的JSON字符串




### def to_srt()

获取srt格式的字幕



**Returns:** `str`:  srt字幕




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

生成ass格式视频字幕文件

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




---

## async def make_lrc_file_subtitle()

生成lrc格式视频字幕文件

编码默认采用 utf-8


| name | type | description |
| - | - | - |
| `obj` | `Union[Video,Episode]` | 对象 |
| `page_index` | `int, optional` | 分 P 索引 |
| `cid` | `int, optional` | cid |
| `out` | `str, optional` | 输出位置. Defaults to "test.lrc". |
| `lan_name` | `str, optional` | 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）". |
| `lan_code` | `str, optional` | 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh" |
| `credential` | `Credential, optional` | Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处 |




---

## async def make_simple_json_file_subtitle()

生成简化后的json格式视频字幕文件

编码默认采用 utf-8


| name | type | description |
| - | - | - |
| `obj` | `Union[Video,Episode]` | 对象 |
| `page_index` | `int, optional` | 分 P 索引 |
| `cid` | `int, optional` | cid |
| `out` | `str, optional` | 输出位置. Defaults to "test.json". |
| `lan_name` | `str, optional` | 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）". |
| `lan_code` | `str, optional` | 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh" |
| `credential` | `Credential, optional` | Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处 |




---

## async def make_srt_file_subtitle()

生成srt格式视频字幕文件

编码默认采用 utf-8


| name | type | description |
| - | - | - |
| `obj` | `Union[Video,Episode]` | 对象 |
| `page_index` | `int, optional` | 分 P 索引 |
| `cid` | `int, optional` | cid |
| `out` | `str, optional` | 输出位置. Defaults to "test.srt". |
| `lan_name` | `str, optional` | 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）". |
| `lan_code` | `str, optional` | 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh" |
| `credential` | `Credential, optional` | Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处 |




---

## async def request_subtitle_languages()

获取远程字幕语言列表


| name | type | description |
| - | - | - |
| `obj` | `Union[Video,Episode]` | 对象 |
| `page_index` | `int, optional` | 分 P 索引 |
| `cid` | `int, optional` | cid |
| `credential` | `Credential, optional` | Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处 |

**Returns:** `AssSubtitleObject`:  字幕对象



---

## async def request_subtitle()

获取远程字幕


| name | type | description |
| - | - | - |
| `obj` | `Union[Video,Episode]` | 对象 |
| `page_index` | `int, optional` | 分 P 索引 |
| `cid` | `int, optional` | cid |
| `lan_name` | `str, optional` | 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）" 默认None 则自动获取可用歌词. |
| `lan_code` | `str, optional` | 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh" 默认None 则自动获取可用歌词 |
| `credential` | `Credential, optional` | Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处 |

**Returns:** `AssSubtitleObject`:  字幕对象




