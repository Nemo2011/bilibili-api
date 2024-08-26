# Module dynamic.py


bilibili_api.dynamic

动态相关


``` python
from bilibili_api import dynamic
```

## class BuildDynamic

**Extend: builtins.object**

构建动态内容. 提供两种 API.

- 1. 链式调用构建

``` python
BuildDynamic.empty().add_plain_text("114514").add_image(Picture.from_url("https://www.bilibili.com/favicon.ico"))
```

- 2. 参数构建

``` python
BuildDynamic.create_by_args(text="114514", topic_id=114514)
```




### def add_at()

添加@用户，支持传入 User 类或 UID


| name | type | description |
| - | - | - |
| uid | Union[int, user.User] | 用户ID |

**Returns:** None



### def add_emoji()

添加表情


| name | type | description |
| - | - | - |
| emoji_id | int | 表情ID |

**Returns:** None



### def add_image()

添加图片


| name | type | description |
| - | - | - |
| image | Picture \| List[Picture] | 图片类 |

**Returns:** None



### def add_plain_text()

添加纯文本


| name | type | description |
| - | - | - |
| text | str | 文本内容 |

**Returns:** None



### def add_text()

添加文本 (可包括 at, 表情包)


| name | type | description |
| - | - | - |
| text | str | 文本内容 |

**Returns:** None



### def add_vote()

添加投票


| name | type | description |
| - | - | - |
| vote | vote.Vote | 投票对象 |

**Returns:** None



### def get_attach_card()

获取动态预约



**Returns:** Optional[dict]: 动态预约




### def get_contents()

获取动态内容



**Returns:** list: 动态内容




### def get_dynamic_type()

获取动态类型



**Returns:** SendDynamicType: 动态类型




### def get_options()

获取动态选项



**Returns:** dict: 动态选项




### def get_pics()

获取动态图片



**Returns:** list: 动态图片




### def get_topic()

获取动态话题



**Returns:** Optional[dict]: 动态话题




### def set_attach_card()

设置直播预约

在 live.create_live_reserve 中获取 oid


| name | type | description |
| - | - | - |
| oid | int | 卡片oid |

**Returns:** None



### def set_options()

设置选项


| name | type | description |
| - | - | - |
| up_choose_comment | [bool | 精选评论flag |
| close_comment | [bool | 关闭评论flag |

**Returns:** None



### def set_send_time()

设置发送时间


| name | type | description |
| - | - | - |
| time | datetime | 发送时间 |

**Returns:** None



### def set_topic()

设置话题


| name | type | description |
| - | - | - |
| topic_id | int | 话题ID |

**Returns:** None



## class Dynamic

**Extend: builtins.object**

动态类


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |


### async def delete()

删除动态



**Returns:** dict: 调用 API 返回的结果




### def get_dynamic_id()

获取动态 id



**Returns:** int: _description_




### async def get_info()

(对 Opus 动态，获取动态内容建议使用 Opus.get_detail())

获取动态信息


| name | type | description |
| - | - | - |
| features | Union[str, None] | 默认 itemOpusStyle. |

**Returns:** dict: 调用 API 返回的结果




### async def get_likes()

获取动态点赞列表


| name | type | description |
| - | - | - |
| pn | Union[int, None] | 页码，defaults to 1 |
| ps | Union[int, None] | 每页大小，defaults to 30 |

**Returns:** dict: 调用 API 返回的结果




### async def get_reaction()

获取点赞、转发


| name | type | description |
| - | - | - |
| offset | Union[str, None] | 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to "" |

**Returns:** dict: 调用 API 返回的结果




### async def get_reposts()

获取动态转发列表


| name | type | description |
| - | - | - |
| offset | Union[str, None] | 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to "0" |

**Returns:** dict: 调用 API 返回的结果




### def is_opus()

判断是否为 opus 动态



**Returns:** bool: 是否为 opus 动态




### async def repost()

转发动态


| name | type | description |
| - | - | - |
| text | Union[str, None] | 转发动态时的文本内容. Defaults to "转发动态" |

**Returns:** dict: 调用 API 返回的结果




### async def set_like()

设置动态点赞状态


| name | type | description |
| - | - | - |
| status | Union[bool, None] | 点赞状态. Defaults to True. |

**Returns:** dict: 调用 API 返回的结果




### def turn_to_opus()

对 opus 动态，将其转换为图文



**Returns:** None



## class DynamicContentType

**Extend: enum.Enum**

动态内容类型

+ TEXT: 文本
+ EMOJI: 表情
+ AT: @User
+ VOTE: 投票




## class DynamicType

**Extend: enum.Enum**

动态类型

+ ALL: 所有动态
+ ANIME: 追番追剧
+ ARTICLE: 文章
+ VIDEO: 视频投稿




## class SendDynamicType

**Extend: enum.Enum**

发送动态类型
scene 参数

+ TEXT: 纯文本
+ IMAGE: 图片




## async def delete_schedule()

删除定时动态


| name | type | description |
| - | - | - |
| draft_id | int | 定时动态 ID |
| credential | Credential | 凭据 |

**Returns:** dict: 调用 API 返回的结果




## async def get_dynamic_page_UPs_info()

获取动态页 UP 主列表


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类. |

**Returns:** dict: 调用 API 返回的结果




## async def get_dynamic_page_info()

获取动态页动态信息

获取全部动态或者相应类型需传入 _type

获取指定 UP 主动态需传入 host_mid


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类. |
| _type | Union[DynamicType, None] | 动态类型. Defaults to DynamicType.ALL. |
| host_mid | Union[int, None] | 获取对应 UP 主动态的 mid. Defaults to None. |
| features | Union[str, None] | 默认 itemOpusStyle. |
| pn | Union[int, None] | 页码. Defaults to 1. |
| offset | Union[int, None] | 偏移值（下一页的第一个动态 ID，为该请求结果中的 offset 键对应的值），类似单向链表. Defaults to None. |

**Returns:** list[Dynamic]: 动态类列表




## async def get_live_users()

获取正在直播的关注者


| name | type | description |
| - | - | - |
| size | int | 获取的数据数量. Defaults to 10. |
| credential | Credential \| None | 凭据类. Defaults to None. |

**Returns:** dict: 调用 API 返回的结果




## async def get_new_dynamic_users()

获取更新动态的关注者


| name | type | description |
| - | - | - |
| credential | Credential \| None | 凭据类. Defaults to None. |

**Returns:** dict: 调用 API 返回的结果




## async def get_schedules_list()

获取待发送定时动态列表


| name | type | description |
| - | - | - |
| credential | Credential | 凭据 |

**Returns:** dict: 调用 API 返回的结果




## async def send_dynamic()

发送动态


| name | type | description |
| - | - | - |
| info | BuildDynamic | 动态内容 |
| credential | Credential | 凭据 |

**Returns:** dict: 调用 API 返回的结果




## async def send_schedule_now()

立即发送定时动态


| name | type | description |
| - | - | - |
| draft_id | int | 定时动态 ID |
| credential | Credential | 凭据 |

**Returns:** dict: 调用 API 返回的结果




## async def upload_image()

上传动态图片


| name | type | description |
| - | - | - |
| image | Picture | 图片流. 有格式要求. |
| credential | Credential | 凭据 |
| data | Dict | 自定义请求体 |

**Returns:** dict: 调用 API 返回的结果




## def upload_image_sync()

上传动态图片 (同步函数)


| name | type | description |
| - | - | - |
| image | Picture | 图片流. 有格式要求. |
| credential | Credential | 凭据 |
| data | Dict | 自定义请求体 |

**Returns:** dict: 调用 API 返回的结果




