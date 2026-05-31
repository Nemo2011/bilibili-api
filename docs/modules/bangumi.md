# Module bangumi.py


bilibili_api.bangumi

番剧相关

概念：
+ media_id: 番剧本身的 ID，有时候也是每季度的 ID，如 https://www.bilibili.com/bangumi/media/md28231846/
+ season_id: 每季度的 ID
+ episode_id: 每集的 ID，如 https://www.bilibili.com/bangumi/play/ep374717



``` python
from bilibili_api import bangumi
```

- [class Bangumi()](#class-Bangumi)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_episode\_list()](#async-def-get\_episode\_list)
  - [async def get\_episodes()](#async-def-get\_episodes)
  - [async def get\_long\_comment\_list()](#async-def-get\_long\_comment\_list)
  - [async def get\_media\_id()](#async-def-get\_media\_id)
  - [async def get\_meta()](#async-def-get\_meta)
  - [async def get\_overview()](#async-def-get\_overview)
  - [async def get\_raw()](#async-def-get\_raw)
  - [async def get\_season\_id()](#async-def-get\_season\_id)
  - [async def get\_short\_comment\_list()](#async-def-get\_short\_comment\_list)
  - [async def get\_stat()](#async-def-get\_stat)
  - [async def get\_up\_info()](#async-def-get\_up\_info)
  - [async def set\_media\_id()](#async-def-set\_media\_id)
  - [async def set\_ssid()](#async-def-set\_ssid)
- [class BangumiCommentOrder()](#class-BangumiCommentOrder)
- [class BangumiType()](#class-BangumiType)
- [class Episode()](#class-Episode)
  - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [async def get\_ai\_conclusion()](#async-def-get\_ai\_conclusion)
  - [async def get\_aid()](#async-def-get\_aid)
  - [async def get\_bangumi()](#async-def-get\_bangumi)
  - [async def get\_bangumi\_from\_episode()](#async-def-get\_bangumi\_from\_episode)
  - [async def get\_bvid()](#async-def-get\_bvid)
  - [async def get\_cid()](#async-def-get\_cid)
  - [async def get\_danmaku\_view()](#async-def-get\_danmaku\_view)
  - [async def get\_danmaku\_xml()](#async-def-get\_danmaku\_xml)
  - [async def get\_danmakus()](#async-def-get\_danmakus)
  - [async def get\_download\_url()](#async-def-get\_download\_url)
  - [def get\_epid()](#def-get\_epid)
  - [async def get\_episode\_info()](#async-def-get\_episode\_info)
  - [async def get\_history\_danmaku\_index()](#async-def-get\_history\_danmaku\_index)
  - [async def get\_pbp()](#async-def-get\_pbp)
  - [async def get\_player\_info()](#async-def-get\_player\_info)
  - [async def get\_subtitle()](#async-def-get\_subtitle)
  - [async def recall\_danmaku()](#async-def-recall\_danmaku)
  - [async def send\_danmaku()](#async-def-send\_danmaku)
  - [async def set\_epid()](#async-def-set\_epid)
  - [async def set\_favorite()](#async-def-set\_favorite)
  - [async def submit\_subtitle()](#async-def-submit\_subtitle)
  - [async def turn\_to\_video()](#async-def-turn\_to\_video)
- [class IndexFilter()](#class-IndexFilter)
  - [class Area()](#class-Area)
  - [class Copyright()](#class-Copyright)
  - [class Finish\_Status()](#class-Finish\_Status)
  - [class Order()](#class-Order)
  - [class Payment()](#class-Payment)
  - [class Producer()](#class-Producer)
  - [class Season()](#class-Season)
  - [class Sort()](#class-Sort)
  - [class Spoken\_Language()](#class-Spoken\_Language)
  - [class Style()](#class-Style)
    - [class Anime()](#class-Anime)
    - [class Documentary()](#class-Documentary)
    - [class GuoChuang()](#class-GuoChuang)
    - [class Movie()](#class-Movie)
    - [class TV()](#class-TV)
    - [class Variety()](#class-Variety)
  - [class Type()](#class-Type)
  - [class Version()](#class-Version)
  - [def make\_time\_filter()](#def-make\_time\_filter)
- [class IndexFilterMeta()](#class-IndexFilterMeta)
  - [class Anime()](#class-Anime)
    - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [class Documentary()](#class-Documentary)
    - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [class GuoChuang()](#class-GuoChuang)
    - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [class Movie()](#class-Movie)
    - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [class TV()](#class-TV)
    - [def \_\_init\_\_()](#def-\_\_init\_\_)
  - [class Variety()](#class-Variety)
    - [def \_\_init\_\_()](#def-\_\_init\_\_)
- [async def get\_index\_info()](#async-def-get\_index\_info)
- [async def get\_timeline()](#async-def-get\_timeline)
- [async def set\_follow()](#async-def-set\_follow)
- [async def update\_follow\_status()](#async-def-update\_follow\_status)

---

## class Bangumi()

番剧类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `media_id` | `int, optional` | 番剧本身的 ID. Defaults to -1. |
| `ssid` | `int, optional` | 每季度的 ID. Defaults to -1. |
| `epid` | `int, optional` | 每集的 ID. Defaults to -1. |
| `oversea` | `bool, optional` | 是否要采用兼容的港澳台Api,用于仅限港澳台地区番剧的信息请求. Defaults to False. |
| `credential` | `Credential \| None, optional` | 凭据类. Defaults to None. |


### async def get_episode_list()

获取季度分集列表，自动转换出海Api的字段，适配部分，但是键还是有不同



**Returns:** `dict`:  调用 API 返回的结果




### async def get_episodes()

获取番剧所有的剧集，自动生成类。



**Returns:** `list['Episode']`:  剧集类列表




### async def get_long_comment_list()

获取长评列表


| name | type | description |
| - | - | - |
| `order` | `BangumiCommentOrder, optional` | 排序方式。Defaults to BangumiCommentOrder.DEFAULT. |
| `next` | `str \| None, optional` | 调用返回结果中的 next 键值，用于获取下一页数据. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_media_id()

获取 media_id



**Returns:** `int`:  获取 media_id




### async def get_meta()

获取番剧元数据信息（评分，封面 URL，标题等）



**Returns:** `dict`:  调用 API 返回的结果




### async def get_overview()

获取番剧全面概括信息，包括发布时间、剧集情况、stat 等情况



**Returns:** `dict`:  调用 API 返回的结果




### async def get_raw()

原始初始化数据



**Returns:** `tuple[dict, bool]`:  Api 相关字段




### async def get_season_id()

获取季度 id



**Returns:** `int`:  获取季度 id




### async def get_short_comment_list()

获取短评列表


| name | type | description |
| - | - | - |
| `order` | `BangumiCommentOrder, optional` | 排序方式。Defaults to BangumiCommentOrder.DEFAULT. |
| `next` | `str \| None, optional` | 调用返回结果中的 next 键值，用于获取下一页数据. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




### async def get_stat()

获取番剧播放量，追番等信息



**Returns:** `dict`:  调用 API 返回的结果




### async def get_up_info()

番剧上传者信息 出差或者原版



**Returns:** `dict`:  Api 相关字段




### async def set_media_id()

设置 media_id


| name | type | description |
| - | - | - |
| `media_id` | `int` | 设置 media_id |




### async def set_ssid()

设置季度 id


| name | type | description |
| - | - | - |
| `ssid` | `int` | 设置季度 id |




---

## class BangumiCommentOrder()

**Extend: enum.Enum**

短评 / 长评 排序方式

+ DEFAULT: 默认
+ CTIME: 发布时间倒序




---

## class BangumiType()

**Extend: enum.Enum**

番剧类型

+ BANGUMI: 番剧
+ FT: 影视
+ GUOCHUANG: 国创




---

## class Episode()

**Extend: bilibili_api.video.Video**

番剧剧集类


| name | type | description |
| - | - | - |
| `credential` | `Credential` | 凭据类 |
| `video_class` | `Video` | 视频类 |
| `bangumi` | `Bangumi` | 所属番剧 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| `epid` | `int` | 番剧 epid |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |


### async def get_ai_conclusion()

获取稿件 AI 总结结果。


| name | type | description |
| - | - | - |
| `up_mid` | `int \| None, optional` | up 主的 mid. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果。




### async def get_aid()

获取 AID。



**Returns:** `int`:  AID。




### async def get_bangumi()

获取对应的番剧



**Returns:** `Bangumi`:  番剧类




### async def get_bangumi_from_episode()

获取剧集对应的番剧



**Returns:** `Bangumi`:  输入的集对应的番剧类




### async def get_bvid()

获取 BVID。



**Returns:** `str`:  BVID。




### async def get_cid()

获取稿件 cid



**Returns:** `int`:  cid




### async def get_danmaku_view()

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。



**Returns:** `dict`:  二进制流解析结果




### async def get_danmaku_xml()

获取所有弹幕的 xml 源文件（非装填）



**Returns:** `str`:  文件源




### async def get_danmakus()

获取弹幕


| name | type | description |
| - | - | - |
| `date` | `datetime.date \| None, optional` | 指定某一天查询弹幕.  (不指定某一天). Defaults to None. |
| `from_seg` | `int \| None, optional` | 从第几段开始(0 开始编号，None 为从第一段开始，一段 6 分钟). Defaults to None. |
| `to_seg` | `int \| None, optional` | 到第几段结束(0 开始编号，None 为到最后一段，包含编号的段，一段 6 分钟). Defaults to None. |

**Returns:** `list['Danmaku']`:  弹幕列表




### async def get_download_url()

获取番剧剧集下载信息。



**Returns:** `dict`:  调用 API 返回的结果。




### def get_epid()

获取 epid



**Returns:** `int`:  epid




### async def get_episode_info()

获取番剧单集信息



**Returns:** `tuple[dict, utils.initial_state.InitialDataType]`:  前半部分为数据，后半部分为数据类型（\_\_INITIAL_STATE\_\_ 或 \_\_NEXT_DATA\_\_）




### async def get_history_danmaku_index()

获取特定月份存在历史弹幕的日期。


| name | type | description |
| - | - | - |
| `date` | `datetime.date \| None, optional` | 精确到年月. Defaults to None. |

**Returns:** `None | list[str]`:  调用 API 返回的结果。不存在时为 None。




### async def get_pbp()

获取高能进度条



**Returns:** `dict`:  调用 API 返回的结果




### async def get_player_info()

获取视频上一次播放的记录，字幕和地区信息。需要分集的 cid, 返回数据中含有json字幕的链接



**Returns:** `dict`:  调用 API 返回的结果




### async def get_subtitle()

获取字幕信息



**Returns:** `dict`:  调用 API 返回的结果




### async def recall_danmaku()

撤回弹幕。


| name | type | description |
| - | - | - |
| `dmid` | `int` | 弹幕 id |

**Returns:** `dict`:  调用 API 返回的结果。




### async def send_danmaku()

发送弹幕。


| name | type | description |
| - | - | - |
| `danmaku` | `Danmaku` | Danmaku 类。 |

**Returns:** `dict`:  调用 API 返回的结果。




### async def set_epid()

设置 epid


| name | type | description |
| - | - | - |
| `epid` | `int` | epid |




### async def set_favorite()

设置视频收藏状况。


| name | type | description |
| - | - | - |
| `add_media_ids` | `List[int], optional` | 要添加到的收藏夹 ID. Defaults to []. |
| `del_media_ids` | `List[int], optional` | 要移出的收藏夹 ID. Defaults to []. |

**Returns:** `dict`:  调用 API 返回结果。




### async def submit_subtitle()

上传字幕

字幕数据 data 参考：

```json
{
  "font_size": "float: 字体大小，默认 0.4",
  "font_color": "str: 字体颜色，默认 #FFFFFF",
  "background_alpha": "float: 背景不透明度，默认 0.5",
  "background_color": "str: 背景颜色，默认 #9C27B0",
  "Stroke": "str: 描边，目前作用未知，默认为 none",
  "body": [
{
  "from": "int: 字幕开始时间（秒）",
  "to": "int: 字幕结束时间（秒）",
  "location": "int: 字幕位置，默认为 2",
  "content": "str: 字幕内容"
}
  ]
}
```


| name | type | description |
| - | - | - |
| `lan` | `str` | 字幕语言代码，参考 https |
| `data` | `Dict` | 字幕数据 |
| `submit` | `bool` | 是否提交，不提交为草稿 |
| `sign` | `bool` | 是否署名 |

**Returns:** `dict`:  API 调用返回结果




### async def turn_to_video()

将番剧剧集对象转换为视频



**Returns:** `video.Video`:  视频对象




---

## class IndexFilter()

番剧索引相关固定参数以及值




### class Area()

**Extend: enum.Enum**

地区

+ ALL: 全部
+ CHINA: 中国
+ CHINA_MAINLAND: 中国大陆
+ CHINA_HONGKONG_AND_TAIWAN: 中国港台
+ JAPAN: 日本
+ USA: 美国
+ UK: 英国
+ SOUTH_KOREA: 韩国
+ FRANCE: 法国
+ THAILAND: 泰国
+ GERMANY: 德国
+ ITALY: 意大利
+ SPAIN: 西班牙
+ ANIME_OTHER: 番剧其他
+ MOVIE_OTHER: 影视其他
+ DOCUMENTARY_OTHER: 纪录片其他

注意：各索引的 其他 表示的地区都不同




### class Copyright()

**Extend: enum.Enum**

版权方

+ ALL: 全部
+ EXCLUSIVE: 独家
+ OTHER: 其他




### class Finish_Status()

**Extend: enum.Enum**

完结状态

+ ALL: 全部
+ FINISHED: 完结
+ UNFINISHED: 连载




### class Order()

**Extend: enum.Enum**

排序字段

+ UPDATE: 更新时间
+ DANMAKU: 弹幕数量
+ PLAY: 播放数量
+ FOLLOWER: 追番人数
+ SOCRE: 最高评分
+ ANIME_RELEASE: 番剧开播日期
+ MOVIE_RELEASE: 电影上映日期




### class Payment()

**Extend: enum.Enum**

观看条件

+ ALL: 全部
+ FREE: 免费
+ PAID: 付费
+ VIP: 大会员




### class Producer()

**Extend: enum.Enum**

制作方

+ ALL: 全部
+ CCTV: CCTV
+ BBC: BBC
+ DISCOVERY: 探索频道
+ NATIONAL_GEOGRAPHIC: 国家地理
+ NHK: NHK
+ HISTORY: 历史频道
+ SATELLITE: 卫视
+ SELF: 自制
+ ITV: ITV
+ SKY: SKY
+ ZDF: ZDF
+ PARTNER: 合作机构
+ SONY: 索尼
+ GLOBAL_NEWS: 环球
+ PARAMOUNT: 派拉蒙
+ WARNER: 华纳
+ DISNEY: 迪士尼
+ HBO: HBO
+ DOMESTIC_OTHER: 国内其他
+ FOREIGN_OTHER: 国外其他




### class Season()

**Extend: enum.Enum**

季度

+ ALL: 全部
+ SPRING: 春季
+ SUMMER: 夏季
+ AUTUMN: 秋季
+ WINTER: 冬季




### class Sort()

**Extend: enum.Enum**

排序方式

+ DESC: 降序
+ ASC: 升序




### class Spoken_Language()

**Extend: enum.Enum**

配音

+ ALL: 全部
+ ORIGINAL: 原声
+ CHINESE: 中配




### class Style()

风格，根据索引不同，可选的风格也不同




#### class Anime()

**Extend: enum.Enum**

番剧风格

+ ALL: 全部
+ ORIGINAL: 原创
+ COMIC: 漫画改
+ NOVEL: 小说改
+ GAME: 游戏改
+ TOKUSATSU: 特摄
+ BUDAIXI: 布袋戏
+ WARM: 热血
+ TIMEBACK: 穿越
+ IMAGING: 奇幻
+ WAR: 战斗
+ FUNNY: 搞笑
+ DAILY: 日常
+ SCIENCE_FICTION: 科幻
+ MOE: 萌系
+ HEAL: 治愈
+ SCHOOL: 校园
+ CHILDREN: 儿童
+ NOODLES: 泡面
+ LOVE: 恋爱
+ GIRLISH: 少女
+ MAGIC: 魔法
+ ADVENTURE: 冒险
+ HISTORY: 历史
+ ALTERNATE: 架空
+ MACHINE_BATTLE: 机战
+ GODS_DEM: 神魔
+ VOICE: 声控
+ SPORT: 运动
+ INSPIRATION: 励志
+ MUSIC: 音乐
+ ILLATION: 推理
+ SOCIEITES: 社团
+ OUTWIT: 智斗
+ TEAR: 催泪
+ FOOD: 美食
+ IDOL: 偶像
+ OTOME: 乙女
+ WORK: 职场




#### class Documentary()

**Extend: enum.Enum**

纪录片风格

+ ALL: 全部
+ HISTORY: 历史
+ FOODS: 美食
+ HUMANITIES: 人文
+ TECHNOLOGY: 科技
+ DISCOVER: 探险
+ UNIVERSE: 宇宙
+ PETS: 萌宠
+ SOCIAL: 社会
+ ANIMALS: 动物
+ NATURE: 自然
+ MEDICAL: 医疗
+ WAR: 战争
+ DISATER: 灾难
+ INVESTIGATIONS: 罪案
+ MYSTERIOUS: 神秘
+ TRAVEL: 旅行
+ SPORTS: 运动
+ MOVIES: 电影




#### class GuoChuang()

**Extend: enum.Enum**

国创风格

+ ALL: 全部
+ ORIGINAL: 原创
+ COMIC: 漫画改
+ NOVEL: 小说改
+ GAME: 游戏改
+ DYNAMIC: 动态漫
+ BUDAIXI: 布袋戏
+ WARM: 热血
+ IMAGING: 奇幻
+ FANTASY: 玄幻
+ WAR: 战斗
+ FUNNY: 搞笑
+ WUXIA: 武侠
+ DAILY: 日常
+ SCIENCE_FICTION: 科幻
+ MOE: 萌系
+ HEAL: 治愈
+ SUSPENSE: 悬疑
+ SCHOOL: 校园
+ CHILDREN: 少儿
+ NOODLES: 泡面
+ LOVE: 恋爱
+ GIRLISH: 少女
+ MAGIC: 魔法
+ HISTORY: 历史
+ MACHINE_BATTLE: 机战
+ GODS_DEMONS: 神魔
+ VOICE: 声控
+ SPORT: 运动
+ INSPIRATION: 励志
+ MUSIC: 音乐
+ ILLATION: 推理
+ SOCIEITES: 社团
+ OUTWIT: 智斗
+ TEAR: 催泪
+ FOOD: 美食
+ IDOL: 偶像
+ OTOME: 乙女
+ WORK: 职场
+ ANCIENT: 古风




#### class Movie()

**Extend: enum.Enum**

电影风格

+ ALL: 全部
+ SKETCH: 短片
+ PLOT: 剧情
+ COMEDY: 喜剧
+ ROMANTIC: 爱情
+ ACTION: 动作
+ SCAIRIER: 恐怖
+ SCIENCE_FICTION: 科幻
+ CRIME: 犯罪
+ TIRILLER: 惊悚
+ SUSPENSE: 悬疑
+ IMAGING: 奇幻
+ WAR: 战争
+ ANIME: 动画
+ BIOAGRAPHY: 传记
+ FAMILY: 家庭
+ SING_DANCE: 歌舞
+ HISTORY: 历史
+ DISCOVER: 探险
+ DOCUMENTARY: 纪录片
+ DISATER: 灾难
+ COMIC: 漫画改
+ NOVEL: 小说改




#### class TV()

**Extend: enum.Enum**

电视剧风格

+ ALL: 全部
+ FUNNY: 搞笑
+ IMAGING: 奇幻
+ WAR: 战争
+ WUXIA: 武侠
+ YOUTH: 青春
+ SKETCH: 短剧
+ CITY: 都市
+ ANCIENT: 古装
+ SPY: 谍战
+ CLASSIC: 经典
+ EMOTION: 情感
+ SUSPENSE: 悬疑
+ INSPIRATION: 励志
+ MYTH: 神话
+ TIMEBACK: 穿越
+ YEAR: 年代
+ COUNTRYSIDE: 乡村
+ INVESTIGATION: 刑侦
+ PLOT: 剧情
+ FAMILY: 家庭
+ HISTORY: 历史
+ EMOTION: 情感
+ ARMY: 军旅
+ SCIENCE_FICTION: 科幻




#### class Variety()

**Extend: enum.Enum**

综艺风格

+ ALL: 全部
+ MUSIC: 音乐
+ TALK: 访谈
+ TALK_SHOW: 脱口秀
+ REALITY_SHOW: 真人秀
+ TALENT_SHOW: 选秀
+ FOOD: 美食
+ TRAVEL: 旅行
+ SOIREE: 晚会
+ CONCERT: 演唱会
+ EMOTION: 情感
+ COMEDY: 喜剧
+ PARENT_CHILD: 亲子
+ CULTURE: 文化
+ OFFICE: 职场
+ PET: 萌宠
+ CULTIVATE: 养成





### class Type()

**Extend: enum.Enum**

索引类型

+ ANIME: 番剧
+ MOVIE: 电影
+ DOCUMENTARY: 纪录片
+ GUOCHUANG: 国创
+ TV: 电视剧
+ VARIETY: 综艺




### class Version()

**Extend: enum.Enum**

番剧版本

+ ALL: 全部
+ MAIN: 正片
+ FILM: 电影
+ OTHER: 其他




**@staticmethod** 

### def make_time_filter()

生成番剧索引所需的时间条件

番剧、国创直接传入年份，为 int 或者 str 类型，如 `make_time_filter(start=2019, end=2020)`

影视、纪录片、电视剧传入 datetime.datetime，如 `make_time_filter(start=datetime.datetime(2019, 1, 1), end=datetime.datetime(2020, 1, 1))`

start 或 end 为 None 时则表示不设置开始或结尾


| name | type | description |
| - | - | - |
| `start` | `datetime.datetime \| str \| int \| None, optional` | 开始时间. 如果是 None 则不设置开头. Defaults to None. |
| `end` | `datetime.datetime \| str \| int \| None, optional` | 结束时间. 如果是 None 则不设置结尾. Defaults to None. |
| `include_start` | `bool, optional` | 是否包含开始时间. Defaults to True. |
| `include_end` | `bool, optional` | 是否包含结束时间. Defaults to False. |

**Returns:** `str`:  年代条件




---

## class IndexFilterMeta()

IndexFilter 元数据

用于传入 get_index_info 方法




### class Anime()

动画




#### def \_\_init\_\_()

Anime Meta


| name | type | description |
| - | - | - |
| `version` | `Version, optional` | 类型，如正片、电影等. Defaults to Version.ALL. |
| `spoken_language` | `Spoken_Language, optional` | 配音. Defaults to Spoken_Language.ALL. |
| `area` | `Area, optional` | 地区. Defaults to Area.ALL. |
| `finish_status` | `Finish_Status, optional` | 是否完结. Defaults to Finish_Status.ALL. |
| `copyright` | `Copyright, optional` | 版权. Defaults to Copyright.ALL. |
| `payment` | `Payment, optional` | 付费门槛. Defaults to Payment.ALL. |
| `season` | `Season, optional` | 季度. Defaults to Season.ALL. |
| `year` | `str, optional` | 年份，调用 Index_Filter.make_time_filter() 传入年份 (int, str) 获取. Defaults to '-1'. |
| `style` | `Anime, optional` | 风格. Defaults to Anime.ALL. |


### class Documentary()

纪录片




#### def \_\_init\_\_()

Documentary Meta


| name | type | description |
| - | - | - |
| `release_date` | `str, optional` | 上映时间，调用 Index_Filter.make_time_filter() 传入年份 (datetime.datetime) 获取. Defaults to '-1'. |
| `style` | `Documentary, optional` | 风格. Defaults to Documentary.ALL. |
| `payment` | `Payment, optional` | 观看条件. Defaults to Payment.ALL. |
| `producer` | `Producer, optional` | 制作方. Defaults to Producer.ALL. |


### class GuoChuang()

国创




#### def \_\_init\_\_()

Guochuang Meta


| name | type | description |
| - | - | - |
| `version` | `Version, optional` | 类型，如正片、电影等. Defaults to Version.ALL. |
| `finish_status` | `Finish_Status, optional` | 是否完结. Defaults to Finish_Status.ALL. |
| `copyright` | `Copyright, optional` | 版权. Defaults to Copyright.ALL. |
| `payment` | `Payment, optional` | 付费门槛. Defaults to Payment.ALL. |
| `year` | `str, optional` | 年份，调用 Index_Filter.make_time_filter() 传入年份 (int, str) 获取. Defaults to '-1'. |
| `style` | `GuoChuang, optional` | 风格. Defaults to GuoChuang.ALL. |


### class Movie()

电影




#### def \_\_init\_\_()

Movie Meta


| name | type | description |
| - | - | - |
| `area` | `Area, optional` | 地区. Defaults to Area.ALL. |
| `release_date` | `str, optional` | 上映时间，调用 Index_Filter.make_time_filter() 传入年份 (datetime.datetime) 获取. Defaults to '-1'. |
| `style` | `Movie, optional` | 风格. Defaults to Movie.ALL. |
| `payment` | `Payment, optional` | 付费门槛. Defaults to Payment.ALL. |


### class TV()

TV




#### def \_\_init\_\_()

TV Meta


| name | type | description |
| - | - | - |
| `area` | `Area, optional` | 地区. Defaults to Area.ALL. |
| `release_date` | `str, optional` | 上映时间，调用 Index_Filter.make_time_filter() 传入年份 (datetime.datetime) 获取. Defaults to '-1'. |
| `style` | `TV, optional` | 风格. Defaults to TV.ALL. |
| `payment` | `Payment, optional` | 付费门槛. Defaults to Payment.ALL. |


### class Variety()

综艺




#### def \_\_init\_\_()

Variety Meta


| name | type | description |
| - | - | - |
| `style` | `Variety, optional` | 风格. Defaults to Variety.ALL. |
| `payment` | `Payment, optional` | 付费门槛. Defaults to Payment.ALL. |


---

## async def get_index_info()

查询番剧索引，索引的详细参数信息见 `IndexFilterMeta`

请先通过 `IndexFilterMeta` 构造 filters


| name | type | description |
| - | - | - |
| `filters` | `object, optional` | 筛选条件元数据. Defaults to <bilibili_api.bangumi.IndexFilterMeta.Anime object at 0x105571160>. |
| `order` | `Order, optional` | 排序字段. Defaults to Order.SCORE. |
| `sort` | `Sort, optional` | 排序方式. Defaults to Sort.DESC. |
| `pn` | `int, optional` | 页数. Defaults to 1. |
| `ps` | `int, optional` | 每页数量. Defaults to 20. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_timeline()

获取番剧时间线


| name | type | description |
| - | - | - |
| `type_` | `BangumiType` | 番剧类型 |
| `before` | `int, optional` | 几天前开始(0~7),. Defaults to 7. |
| `after` | `int, optional` | 几天后结束(0~7),. Defaults to 0. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def set_follow()

追番状态设置


| name | type | description |
| - | - | - |
| `bangumi` | `bangumi.Bangumi` | 番剧类 |
| `status` | `bool, optional` | 追番状态. Defaults to True. |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def update_follow_status()

更新追番状态


| name | type | description |
| - | - | - |
| `bangumi` | `bangumi.Bangumi` | 番剧类 |
| `status` | `int` | 追番状态 1 想看 2 在看 3 已看 |
| `credential` | `Credential \| None, optional` | 凭据. Defaults to None. |

**Returns:** `dict`:  调用 API 返回的结果




