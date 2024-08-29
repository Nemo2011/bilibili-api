# Module ass.py


bilibili_api.ass

有关 ASS 文件的操作


``` python
from bilibili_api import ass
```

---

## async def make_ass_file_danmakus_protobuf()

生成视频弹幕文件

来源：protobuf


| name | type | description |
| - | - | - |
| obj | Union[Video,Episode,CheeseVideo] | 对象 |
| page | Union[int, None] | 分 P 号. Defaults to 0. |
| out | Union[str, None] | 输出文件. Defaults to "test.ass" |
| cid | Union[int, None] | cid. Defaults to None. |
| credential | Union[Credential, None] | 凭据. Defaults to None. |
| date | Union[datetime.date, None] | 获取时间. Defaults to None. |
| font_name | Union[str, None] | 字体. Defaults to "Simsun". |
| font_size | Union[float, None] | 字体大小. Defaults to 25.0. |
| alpha | Union[float, None] | 透明度(0-1). Defaults to 1. |
| fly_time | Union[float, None] | 滚动弹幕持续时间. Defaults to 7. |
| static_time | Union[float, None] | 静态弹幕持续时间. Defaults to 5. |

**Returns:** None



---

## async def make_ass_file_danmakus_xml()

生成视频弹幕文件

来源：xml


| name | type | description |
| - | - | - |
| obj | Union[Video,Episode,Cheese] | 对象 |
| page | Union[int, None] | 分 P 号. Defaults to 0. |
| out | Union[str, None] | 输出文件. Defaults to "test.ass". |
| cid | Union[int, None] | cid. Defaults to None. |
| font_name | Union[str, None] | 字体. Defaults to "Simsun". |
| font_size | Union[float, None] | 字体大小. Defaults to 25.0. |
| alpha | Union[float, None] | 透明度(0-1). Defaults to 1. |
| fly_time | Union[float, None] | 滚动弹幕持续时间. Defaults to 7. |
| static_time | Union[float, None] | 静态弹幕持续时间. Defaults to 5. |

**Returns:** None



---

## async def make_ass_file_subtitle()

生成视频字幕文件


| name | type | description |
| - | - | - |
| obj | Union[Video,Episode] | 对象 |
| page_index | Union[int, None] | 分 P 索引 |
| cid | Union[int, None] | cid |
| out | Union[str, None] | 输出位置. Defaults to "test.ass". |
| lan_name | Union[str, None] | 字幕名，如”中文（自动生成）“,是简介的 subtitle 项的'list'项中的弹幕的'lan_doc'属性。Defaults to "中文（自动生成）". |
| lan_code | Union[str, None] | 字幕语言代码，如 ”中文（自动翻译）” 和 ”中文（自动生成）“ 为 "ai-zh" |
| credential | Union[Credential, None] | Credential 类. 必须在此处或传入的视频 obj 中传入凭据，两者均存在则优先此处 |

**Returns:** None



