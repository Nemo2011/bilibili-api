# Module video_zone.py


bilibili_api.video_zone

分区相关操作，与频道不互通。


``` python
from bilibili_api import video_zone
```

- [class VideoZoneTypes()](#class-VideoZoneTypes)
- [async def get\_zone\_hot\_tags()](#async-def-get\_zone\_hot\_tags)
- [def get\_zone\_info\_by\_name()](#def-get\_zone\_info\_by\_name)
- [def get\_zone\_info\_by\_tid()](#def-get\_zone\_info\_by\_tid)
- [def get\_zone\_list()](#def-get\_zone\_list)
- [def get\_zone\_list\_sub()](#def-get\_zone\_list\_sub)
- [async def get\_zone\_new\_videos()](#async-def-get\_zone\_new\_videos)
- [async def get\_zone\_top10()](#async-def-get\_zone\_top10)
- [async def get\_zone\_videos\_count\_today()](#async-def-get\_zone\_videos\_count\_today)

---

## class VideoZoneTypes()

**Extend: enum.Enum**

所有分区枚举

- MAINPAGE: 主页
- ANIME: 番剧
- ANIME_SERIAL: 连载动画
- ANIME_FINISH: 完结动画
- ANIME_INFORMATION: 资讯
- ANIME_OFFICAL: 官方延伸
- MOVIE: 电影
- GUOCHUANG: 国创
- GUOCHUANG_CHINESE: 国产动画
- GUOCHUANG_ORIGINAL: 国产原创相关
- GUOCHUANG_PUPPETRY: 布袋戏
- GUOCHUANG_MOTIONCOMIC: 动态漫·广播剧
- GUOCHUANG_INFORMATION: 资讯
- TELEPLAY: 电视剧
- DOCUMENTARY: 纪录片
- DOUGA: 动画
- DOUGA_MAD: MAD·AMV
- DOUGA_MMD: MMD·3D
- DOUGA_HANDDRAWN: 同人·手书
- DOUGA_VOICE: 配音
- DOUGA_GARAGE_KIT: 模玩·周边
- DOUGA_TOKUSATSU: 特摄
- DOUGA_ACGNTALKS: 动漫杂谈
- DOUGA_OTHER: 综合
- GAME: 游戏
- GAME_STAND_ALONE: 单机游戏
- GAME_ESPORTS: 电子竞技
- GAME_MOBILE: 手机游戏
- GAME_ONLINE: 网络游戏
- GAME_BOARD: 桌游棋牌
- GAME_GMV: GMV
- GAME_MUSIC: 音游
- GAME_MUGEN: Mugen
- KICHIKU: 鬼畜
- KICHIKU_GUIDE: 鬼畜调教
- KICHIKU_MAD: 音MAD
- KICHIKU_MANUAL_VOCALOID: 人力VOCALOID
- KICHIKU_THEATRE: 鬼畜剧场
- KICHIKU_COURSE: 教程演示
- MUSIC: 音乐
- MUSIC_ORIGINAL: 原创音乐
- MUSIC_COVER: 翻唱
- MUSIC_PERFORM: 演奏
- MUSIC_VOCALOID: VOCALOID·UTAU
- MUSIC_LIVE: 音乐现场
- MUSIC_MV: MV
- MUSIC_COMMENTARY: 乐评盘点
- MUSIC_TUTORIAL: 音乐教学
- MUSIC_FAN_VIDEOS: 音乐粉丝饭拍
- MUSIC_AI_MUSIC: AI音乐
- MUSIC_RADIO: 电台
- MUSIC_OTHER: 音乐综合
- DANCE: 舞蹈
- DANCE_OTAKU: 宅舞
- DANCE_HIPHOP: 街舞
- DANCE_STAR: 明星舞蹈
- DANCE_CHINA: 国风舞蹈
- DANCE_THREE_D: 舞蹈综合
- DANCE_DEMO: 舞蹈教程
- DANGE_GESTURES: 颜值·网红舞
- CINEPHILE: 影视
- CINEPHILE_CINECISM: 影视杂谈
- CINEPHILE_MONTAGE: 影视剪辑
- CINEPHILE_MASHUP: 影视整活
- CINEPHILE_AI_IMAGING: AI影像
- CINEPHILE_SHORTFILM: 短片
- CINEPHILE_SHORTPLAY: 小剧场
- CINEPHILE_TRAILER_INFO: 预告·资讯
- CINEPHILE_COMPREHENSIVE: 影视综合
- ENT: 娱乐
- ENT_VARIETY: 综艺
- ENT_TALKER: 娱乐杂谈
- ENT_FANS: 粉丝创作
- ENT_CELEBRITY: 明星综合
- ENT_CP_RECOMMENDATION: CP安利
- ENT_BEAUTY: 颜值安利
- ENT_ENTERTAINMENT_NEWS: 娱乐资讯
- KNOWLEDGE: 知识
- KNOWLEDGE_SCIENCE: 科学科普
- KNOWLEDGE_SOCIAL_SCIENCE: 社科·法律·心理
- KNOWLEDGE_HUMANITY_HISTORY: 人文历史
- KNOWLEDGE_BUSINESS: 财经商业
- KNOWLEDGE_CAMPUS: 校园学习
- KNOWLEDGE_CAREER: 职业职场
- KNOWLEDGE_DESIGN: 设计·创意
- KNOWLEDGE_SKILL: 野生技能协会
- TECH: 科技
- TECH_DIGITAL: 数码
- TECH_APPLICATION: 软件应用
- TECH_COMPUTER_TECH: 计算机技术
- TECH_INDUSTRY: 科工机械
- TECH_DIY: 极客DIY
- INFORMATION: 资讯
- INFORMATION_HOTSPOT: 热点
- INFORMATION_GLOBAL: 环球
- INFORMATION_SOCIAL: 社会
- INFORMATION_MULTIPLE: 综合
- FOOD: 美食
- FOOD_MAKE: 美食制作
- FOOD_DETECTIVE: 美食侦探
- FOOD_MEASUREMENT: 美食测评
- FOOD_RURAL: 田园美食
- FOOD_RECORD: 美食记录
- LIFE: 生活
- LIFE_FUNNY: 搞笑
- LIFE_PARENTING: 亲子
- LIFE_TRAVEL: 出行
- LIFE_RURALLIFE: 三农
- LIFE_HOME: 家居房产
- LIFE_HANDMAKE: 手工
- LIFE_PAINTING: 绘画
- LIFE_DAILY: 日常
- CAR: 汽车
- CAR_RACING: 赛车
- CAR_MODIFIEDVEHICLE: 改装玩车
- CAR_NEWENERGYVEHICLE: 新能源车
- CAR_TOURINGCAR: 房车
- CAR_MOTORCYCLE: 摩托车
- CAR_STRATEGY: 购车攻略
- CAR_LIFE: 汽车生活
- CAR_KNOWLEDGE: 汽车知识科普
- FASHION: 时尚
- FASHION_MAKEUP: 美妆护肤
- FASHION_COS: 仿妆cos
- FASHION_CLOTHING: 穿搭
- FASHION_TREND: 时尚潮流
- SPORTS: 运动
- SPORTS_BASKETBALL: 篮球
- SPORTS_FOOTBALL: 足球
- SPORTS_AEROBICS: 健身
- SPORTS_ATHLETIC: 竞技体育
- SPORTS_CULTURE: 运动文化
- SPORTS_COMPREHENSIVE: 运动综合
- ANIMAL: 动物圈
- ANIMAL_CAT: 喵星人
- ANIMAL_DOG: 汪星人
- ANIMAL_REPTILES: 小宠异宠
- ANIMAL_PANDA: 动物二创
- ANIMAL_WILD_ANIMAL: 野生动物
- ANIMAL_COMPOSITE: 动物综合




---

## async def get_zone_hot_tags()

获取分区热门标签


| name | type | description |
| - | - | - |
| `tid` | `int` | 分区 id |

**Returns:** `List[dict]`:  热门标签




---

## def get_zone_info_by_name()

根据分区名称获取分区信息。


| name | type | description |
| - | - | - |
| `name` | `str` | 频道的名称。 |

**Returns:** `Tuple[dict | None, dict | None]`:  第一个是主分区，第二个是子分区，没有时返回 None。




---

## def get_zone_info_by_tid()

根据 tid 获取分区信息。


| name | type | description |
| - | - | - |
| `tid` | `int` | 频道的 tid。 |

**Returns:** `Tuple[dict | None, dict | None]`:  第一个是主分区，第二个是子分区，没有时返回 None。




---

## def get_zone_list()

获取所有分区的数据



**Returns:** `List[dict]`:  所有分区的数据




---

## def get_zone_list_sub()

获取所有分区的数据
含父子关系（即一层次只有主分区）



**Returns:** `dict`:  所有分区的数据




---

## async def get_zone_new_videos()

获取分区最新投稿


| name | type | description |
| - | - | - |
| `tid` | `int` | 分区 id |
| `page_num` | `int` | 第几页. Defaults to 1. |
| `page_size` | `int` | 每页的数据大小. Defaults to 10. |

**Returns:** `dict`:  调用 API 返回的结果




---

## async def get_zone_top10()

获取分区前十排行榜。


| name | type | description |
| - | - | - |
| `tid` | `int` | 频道的 tid。 |
| `day` | `int, optional` | 3 天排行还是 7 天排行。 Defaults to 7. |
| `credential` | `Credential \| None, optional` | Credential 类。Defaults to None. |

**Returns:** `list`:  前 10 的视频信息。




---

## async def get_zone_videos_count_today()

获取每个分区当日最新投稿数量


| name | type | description |
| - | - | - |
| `credential` | `Credential \| None` | 凭据类 |

**Returns:** `dict`:  调用 API 返回的结果




