# Module dynamic.py


bilibili_api.dynamic

动态相关


``` python
from bilibili_api import dynamic
```

- [class BuildDynamic()](#class-BuildDynamic)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [def add\_at()](#def-add\_at)
  - [def add\_emoji()](#def-add\_emoji)
  - [def add\_image()](#def-add\_image)
  - [def add\_plain\_text()](#def-add\_plain\_text)
  - [def add\_text()](#def-add\_text)
  - [def add\_vote()](#def-add\_vote)
  - [def create\_by\_args()](#def-create\_by\_args)
  - [def empty()](#def-empty)
  - [def get\_attach\_card()](#def-get\_attach\_card)
  - [async def get\_contents()](#async-def-get\_contents)
  - [def get\_dynamic\_type()](#def-get\_dynamic\_type)
  - [def get\_options()](#def-get\_options)
  - [def get\_pics()](#def-get\_pics)
  - [def get\_topic()](#def-get\_topic)
  - [def set\_attach\_card()](#def-set\_attach\_card)
  - [def set\_options()](#def-set\_options)
  - [def set\_send\_time()](#def-set\_send\_time)
  - [def set\_topic()](#def-set\_topic)
- [class Dynamic()](#class-Dynamic)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def delete()](#async-def-delete)
  - [def get\_dynamic\_id()](#def-get\_dynamic\_id)
  - [async def get\_info()](#async-def-get\_info)
  - [async def get\_likes()](#async-def-get\_likes)
  - [async def get\_lottery\_info()](#async-def-get\_lottery\_info)
  - [async def get\_reaction()](#async-def-get\_reaction)
  - [async def get\_reposts()](#async-def-get\_reposts)
  - [async def get\_rid()](#async-def-get\_rid)
  - [async def is\_article()](#async-def-is\_article)
  - [async def is\_opus()](#async-def-is\_opus)
  - [async def markdown()](#async-def-markdown)
  - [async def repost()](#async-def-repost)
  - [async def set\_favorite()](#async-def-set\_favorite)
  - [async def set\_like()](#async-def-set\_like)
  - [async def turn\_to\_article()](#async-def-turn\_to\_article)
  - [def turn\_to\_opus()](#def-turn\_to\_opus)
- [class DynamicContentType()](#class-DynamicContentType)
- [class DynamicType()](#class-DynamicType)
- [class SendDynamicType()](#class-SendDynamicType)
- [async def delete\_schedule()](#async-def-delete\_schedule)
- [async def get\_dynamic\_page\_UPs\_info()](#async-def-get\_dynamic\_page\_UPs\_info)
- [async def get\_dynamic\_page\_info()](#async-def-get\_dynamic\_page\_info)
- [async def get\_dynamic\_page\_list()](#async-def-get\_dynamic\_page\_list)
- [async def get\_live\_users()](#async-def-get\_live\_users)
- [async def get\_new\_dynamic\_users()](#async-def-get\_new\_dynamic\_users)
- [async def get\_schedules\_list()](#async-def-get\_schedules\_list)
- [async def send\_dynamic()](#async-def-send\_dynamic)
- [async def send\_schedule\_now()](#async-def-send\_schedule\_now)
- [async def upload\_image()](#async-def-upload\_image)

---

## class BuildDynamic()

构建动态内容. 提供两种 API.

- 1. 链式调用构建

``` python
BuildDynamic.empty().add_plain_text("114514").add_image(await Picture.load_url("https://www.bilibili.com/favicon.ico"))
```

- 2. 参数构建

``` python
BuildDynamic.create_by_args(text="114514", topic_id=114514)
```




### def \_\_init\_\_()

构建动态内容




### def add_at()

添加@用户，支持传入 用户名或 UID


| name | type | description |
| - | - | - |
| `uid` | `int` | 用户ID |
| `uname` | `str` | 用户名称. Defaults to "". |




### def add_emoji()

添加表情


| name | type | description |
| - | - | - |
| `emoji` | `str` | 表情文字 |




### def add_image()

添加图片


| name | type | description |
| - | - | - |
| `image` | `Picture \| List[Picture]` | 图片类 |




### def add_plain_text()

添加纯文本


| name | type | description |
| - | - | - |
| `text` | `str` | 文本内容 |




### def add_text()

添加文本 (可包括 at, 表情包)


| name | type | description |
| - | - | - |
| `text` | `str` | 文本内容 |




### def add_vote()

添加投票


| name | type | description |
| - | - | - |
| `vote_id` | `int` | 投票对象 |




**@staticmethod** 

### def create_by_args()

通过参数构建动态


| name | type | description |
| - | - | - |
| `text` | `str, optional` | 动态文字. Defaults to "". |
| `pics` | `List[Picture]  , optional` | 动态图片列表. Defaults to []. |
| `topic_id` | `int, optional` | 动态话题 id. Defaults to -1. |
| `vote_id` | `int, optional` | 动态中的投票的 id. 将放在整个动态的最后面. Defaults to -1. |
| `live_reserve_id` | `int, optional` | 直播预约 oid. 通过 `live.create_live_reserve` 获取. Defaults to -1. |
| `send_time` | `datetime \| None, optional` | 发送时间. Defaults to None. |




**@staticmethod** 

### def empty()

新建空的动态以链式逐步构建






### def get_attach_card()

获取动态预约



**Returns:** `Optional[dict]`:  动态预约




### async def get_contents()

获取动态内容，通过请求完善字段后返回


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类。必需。 |

**Returns:** `list`:  动态内容




### def get_dynamic_type()

获取动态类型



**Returns:** `SendDynamicType`:  动态类型




### def get_options()

获取动态选项



**Returns:** `dict`:  动态选项




### def get_pics()

获取动态图片



**Returns:** `list`:  动态图片




### def get_topic()

获取动态话题



**Returns:** `Optional[dict]`:  动态话题




### def set_attach_card()

设置直播预约

在 live.create_live_reserve 中获取 oid


| name | type | description |
| - | - | - |
| `oid` | `int` | 卡片oid |




### def set_options()

设置选项


| name | type | description |
| - | - | - |
| `up_choose_comment` | `bool` | 精选评论flag |
| `close_comment` | `bool` | 关闭评论flag |




### def set_send_time()

设置发送时间


| name | type | description |
| - | - | - |
| `time` | `datetime` | 发送时间 |




### def set_topic()

设置话题


| name | type | description |
| - | - | - |
| `topic_id` | `int` | 话题ID |




---

## class Dynamic()

动态类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `dynamic_id` | `int` | 动态 ID |
| `credential` | `Credential \| None, optional` | 凭据类. Defaults to None. |


### async def delete()

删除动态



**Returns:** `dict`:  调用 API 返回的结果




### def get_dynamic_id()

获取 动态 ID。



**Returns:** `int`:  动态 ID。




### async def get_info()

获取动态信息



**Returns:** `dict`:  调用 API 返回的结果




### async def get_likes()

获取动态点赞列表


| name | type | description |
| - | - | - |
| `pn` | `int, optional` | 页码，defaults to 1 |
| `ps` | `int, optional` | 每页大小，defaults to 30 |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_lottery_info()

获取动态抽奖信息



**Returns:** `dict`:  调用 API 返回的结果




### async def get_reaction()

获取点赞、转发


| name | type | description |
| - | - | - |
| `offset` | `str, optional` | 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to "" |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_reposts()

获取动态转发列表


| name | type | description |
| - | - | - |
| `offset` | `str, optional` | 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to "0" |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_rid()

获取 rid，以传入 `comment.get_comments_lazy` 等函数 oid 参数对评论区进行操作



**Returns:** `int`:  rid




### async def is_article()

判断动态是否为专栏发布动态（评论、点赞等数据专栏/动态/图文共享）



**Returns:** `bool`:  是否为专栏




### async def is_opus()

判断动态是否为图文

如果是图文，则动态/图文评论/点赞/转发数据共享



**Returns:** `bool`:  是否为图文




### async def markdown()

生成动态富文本对应 markdown



**Returns:** `str`:  markdown




### async def repost()

转发动态


| name | type | description |
| - | - | - |
| `text` | `str, optional` | 转发动态时的文本内容. Defaults to "转发动态" |

**Returns:** `dict`:  调用 API 返回的结果




### async def set_favorite()

设置动态（图文）收藏状态


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 收藏状态. Defaults to True |

**Returns:** `dict`:  调用 API 返回的结果




### async def set_like()

设置动态点赞状态


| name | type | description |
| - | - | - |
| `status` | `bool, optional` | 点赞状态. Defaults to True. |

**Returns:** `dict`:  调用 API 返回的结果




### async def turn_to_article()

将专栏发布动态转为对应专栏（评论、点赞等数据专栏/动态/图文共享）

如动态无对应专栏将报错。

转换后可投币。



**Returns:** `Article`:  专栏实例




### def turn_to_opus()

对图文动态，转换为图文

此函数不会核验动态是否为图文



**Returns:** `Opus`:  图文对象




---

## class DynamicContentType()

**Extend: enum.Enum**

动态内容类型

+ TEXT: 文本
+ EMOJI: 表情
+ AT: @User
+ VOTE: 投票




---

## class DynamicType()

**Extend: enum.Enum**

动态类型

+ ALL: 所有动态
+ ANIME: 追番追剧
+ ARTICLE: 文章
+ VIDEO: 视频投稿




---

## class SendDynamicType()

**Extend: enum.Enum**

发送动态类型
scene 参数

+ TEXT: 纯文本
+ IMAGE: 图片




---

## async def delete_schedule()

删除定时动态


| name | type | description |
| - | - | - |
| `draft_id` | `int` | 定时动态 ID |
| `credential` | `Credential` | 凭据 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_dynamic_page_UPs_info()

获取动态页 UP 主列表


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_dynamic_page_info()

获取动态页动态信息

获取全部动态或者相应类型需传入 _type

获取指定 UP 主动态需传入 host_mid


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类. |
| `_type` | `DynamicType, optional` | 动态类型. Defaults to DynamicType.ALL. |
| `host_mid` | `int, optional` | 获取对应 UP 主动态的 mid. Defaults to None. |
| `features` | `str, optional` | 默认 itemOpusStyle. |
| `pn` | `int, optional` | 页码. Defaults to 1. |
| `offset` | `int, optional` | 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_dynamic_page_list()

获取动态页动态列表

获取全部动态或者相应类型需传入 _type

获取指定 UP 主动态需传入 host_mid


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类. |
| `_type` | `DynamicType, optional` | 动态类型. Defaults to DynamicType.ALL. |
| `host_mid` | `int, optional` | 获取对应 UP 主动态的 mid. Defaults to None. |
| `features` | `str, optional` | 默认 itemOpusStyle. |
| `pn` | `int, optional` | 页码. Defaults to 1. |
| `offset` | `int, optional` | 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to None. |

**Returns:** `list[Dynamic]`:  动态类列表




---

## async def get_live_users()

获取正在直播的关注者


| name | type | description |
| - | - | - |
| `size` | `int` | 获取的数据数量. Defaults to 10. |
| `credential` | `Credential \| None` | 凭据类. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_new_dynamic_users()

获取更新动态的关注者


| name | type | description |
| - | - | - |
| `credential` | `Credential \| None` | 凭据类. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_schedules_list()

获取待发送定时动态列表


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def send_dynamic()

发送动态


| name | type | description |
| - | - | - |
| `info` | `BuildDynamic` | 动态内容 |
| `credential` | `Credential` | 凭据 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def send_schedule_now()

立即发送定时动态


| name | type | description |
| - | - | - |
| `draft_id` | `int` | 定时动态 ID |
| `credential` | `Credential` | 凭据 |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def upload_image()

上传动态图片


| name | type | description |
| - | - | - |
| `image` | `Picture` | 图片流. 有格式要求. |
| `credential` | `Credential` | 凭据 |
| `data` | `Dict` | 自定义请求体 |

**Returns:** `dict`:  调用 API 返回的结果




