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

---

## class Bangumi()

番剧类


| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| media_id | Union[int, None] | 番剧本身的 ID. Defaults to -1. |
| ssid | Union[int, None] | 每季度的 ID. Defaults to -1. |
| epid | Union[int, None] | 每集的 ID. Defaults to -1. |
| oversea | Union[bool, None] | 是否要采用兼容的港澳台Api,用于仅限港澳台地区番剧的信息请求. Defaults to False. |
| credential | Union[Credential, None] | 凭据类. Defaults to None. |


### async def get_episode_list()

获取季度分集列表，自动转换出海Api的字段，适配部分，但是键还是有不同



**Returns:** dict: 调用 API 返回的结果




### async def get_episodes()

获取番剧所有的剧集，自动生成类。



**Returns:** None



### async def get_long_comment_list()

获取长评列表


| name | type | description |
| - | - | - |
| order | Union[BangumiCommentOrder, None] | 排序方式。Defaults to BangumiCommentOrder.DEFAULT |
| next | Union[str, None] | 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None |

**Returns:** dict: 调用 API 返回的结果




### def get_media_id()

获取 media_id



**Returns:** int: 获取 media_id




### async def get_meta()

获取番剧元数据信息（评分，封面 URL，标题等）



**Returns:** dict: 调用 API 返回的结果




### async def get_overview()

获取番剧全面概括信息，包括发布时间、剧集情况、stat 等情况



**Returns:** dict: 调用 API 返回的结果




### def get_raw()

原始初始化数据



**Returns:** Api 相关字段




### def get_season_id()

获取季度 id



**Returns:** int: 获取季度 id




### async def get_short_comment_list()

获取短评列表


| name | type | description |
| - | - | - |
| order | Union[BangumiCommentOrder, None] | 排序方式。Defaults to BangumiCommentOrder.DEFAULT |
| next | Union[str, None] | 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None |

**Returns:** dict: 调用 API 返回的结果




### async def get_stat()

获取番剧播放量，追番等信息



**Returns:** dict: 调用 API 返回的结果




### def get_up_info()

番剧上传者信息 出差或者原版



**Returns:** Api 相关字段




### def set_media_id()

设置 media_id


| name | type | description |
| - | - | - |
| media_id | int | 设置 media_id |

**Returns:** None



### def set_ssid()

设置季度 id


| name | type | description |
| - | - | - |
| ssid | int | 设置季度 id |

**Returns:** None



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
| credential | Credential | 凭据类 |
| video_class | Video | 视频类 |
| bangumi | Bangumi | 所属番剧 |


### def \_\_init\_\_()


| name | type | description |
| - | - | - |
| epid | int | 番剧 epid |
| credential | Union[Credential, None] | 凭据. Defaults to None. |


### def get_bangumi()

获取对应的番剧



**Returns:** Bangumi: 番剧类




### async def get_bangumi_from_episode()

获取剧集对应的番剧



**Returns:** Bangumi: 输入的集对应的番剧类




### async def get_cid()

获取稿件 cid



**Returns:** int: cid




### async def get_danmaku_view()

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。



**Returns:** dict: 二进制流解析结果




### async def get_danmaku_xml()

获取所有弹幕的 xml 源文件（非装填）



**Returns:** str: 文件源




### async def get_danmakus()

获取弹幕


| name | type | description |
| - | - | - |
| date | Union[datetime.date, None] | 指定某一天查询弹幕. Defaults to None. (不指定某一天) |

**Returns:** dict[Danmaku]: 弹幕列表




### async def get_download_url()

获取番剧剧集下载信息。



**Returns:** dict: 调用 API 返回的结果。




### def get_epid()

获取 epid



**Returns:** None



### async def get_episode_info()

获取番剧单集信息



**Returns:** HTML 中的数据




### async def get_history_danmaku_index()

获取特定月份存在历史弹幕的日期。


| name | type | description |
| - | - | - |
| date | Union[datetime.date, None] | 精确到年月. Defaults to None。 |

**Returns:** None | List[str]: 调用 API 返回的结果。不存在时为 None。




### def set_epid()

设置 epid


| name | type | description |
| - | - | - |
| epid | int | epid |

**Returns:** None



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
| start | datetime, str, int | 开始时间. 如果是 None 则不设置开头. |
| end | datetime, str, int | 结束时间. 如果是 None 则不设置结尾. |
| include_start | bool | 是否包含开始时间. 默认为 True. |
| include_end | bool | 是否包含结束时间. 默认为 False. |

**Returns:** str: 年代条件




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
| version | Index_Filter.Version | 类型，如正片、电影等 |
| spoken_language | Index_Filter.Spoken_Language | 配音 |
| area | Index_Filter.Area | 地区 |
| finish_status | Index_Filter.Finish_Status | 是否完结 |
| copyright | Index_Filter.Copryright | 版权 |
| payment | Index_Filter.Payment | 付费门槛 |
| season | Index_Filter.Season | 季度 |
| year | str | 年份，调用 Index_Filter.make_time_filter() 传入年份 (int, str) 获取 |
| style | Index_Filter.Style.Anime | 风格 |


### class Documentary()

纪录片




#### def \_\_init\_\_()

Documentary Meta

| name | type | description |
| - | - | - |
| area | Index_Filter.Area | 地区 |
| release_date | str | 上映时间，调用 Index_Filter.make_time_filter() 传入年份 (datetime.datetime) 获取 |
| style | Index_Filter.Style.Documentary | 风格 |
| producer | Index_Filter.Producer | 制作方 |


### class GuoChuang()

国创




#### def \_\_init\_\_()

Guochuang Meta

| name | type | description |
| - | - | - |
| version | Index_Filter.VERSION | 类型，如正片、电影等 |
| finish_status | Index_Filter.Finish_Status | 是否完结 |
| copyright | Index_Filter.Copyright | 版权 |
| payment | Index_Filter.Payment | 付费门槛 |
| year | str | 年份，调用 Index_Filter.make_time_filter() 传入年份 (int, str) 获取 |
| style | Index_Filter.Style.GuoChuang | 风格 |


### class Movie()

电影




#### def \_\_init\_\_()

Movie Meta

| name | type | description |
| - | - | - |
| area | Index_Filter.Area | 地区 |
| payment | Index_Filter.Payment | 付费门槛 |
| season | Index_Filter.Season | 季度 |
| release_date | str | 上映时间，调用 Index_Filter.make_time_filter() 传入年份 (datetime.datetime) 获取 |
| style | Index_Filter.Style.Movie | 风格 |


### class TV()

TV




#### def \_\_init\_\_()

TV Meta

| name | type | description |
| - | - | - |
| area | Index_Filter.Area | 地区 |
| payment | Index_Filter.Payment | 付费门槛 |
| release_date | str | 上映时间，调用 Index_Filter.make_time_filter() 传入年份 (datetime.datetime) 获取 |
| style | Index_Filter.Style.TV | 风格 |


### class Variety()

综艺




#### def \_\_init\_\_()

Variety Meta

| name | type | description |
| - | - | - |
| payment | Index_Filter.Payment | 付费门槛 |
| style | Index_Filter.Style.Variety | 风格 |


---

## async def get_index_info()

查询番剧索引，索引的详细参数信息见 `IndexFilterMeta`

请先通过 `IndexFilterMeta` 构造 filters


| name | type | description |
| - | - | - |
| filters | Union[Index_Filter_Meta, None] | 筛选条件元数据. Defaults to Anime. |
| order | Union[BANGUMI_INDEX.ORDER, None] | 排序字段. Defaults to SCORE. |
| sort | Union[BANGUMI_INDEX.SORT, None] | 排序方式. Defaults to DESC. |
| pn | Union[int, None] | 页数. Defaults to 1. |
| ps | Union[int, None] | 每页数量. Defaults to 20. |

**Returns:** dict: 调用 API 返回的结果




---

## async def get_timeline()

获取番剧时间线


| name | type | description |
| - | - | - |
| type_ | BangumiType | 番剧类型 |
| before | int | 几天前开始(0~7), defaults to 7 |
| after | int | 几天后结束(0~7), defaults to 0 |

**Returns:** None



---

## async def set_follow()

追番状态设置


| name | type | description |
| - | - | - |
| bangumi | Bangumi | 番剧类 |
| status | Union[bool, None] | 追番状态. Defaults to True. |
| credential | Union[Credential, None] | 凭据. Defaults to None. |

**Returns:** dict: 调用 API 返回的结果




---

## async def update_follow_status()

更新追番状态


| name | type | description |
| - | - | - |
| bangumi | Bangumi | 番剧类 |
| credential | Union[Credential, None] | 凭据. Defaults to None. |
| status | int | 追番状态 1 想看 2 在看 3 已看 |

**Returns:** dict: 调用 API 返回的结果




