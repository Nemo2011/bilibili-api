# Module bangumi.py

```python
from bilibili_api import bangumi
```

番剧相关

概念：

+ media_id: 番剧本身的 ID，有时候也是每季度的 ID，如 https://www.bilibili.com/bangumi/media/md28231846/
+ season_id: 每季度的 ID，只能通过 get_meta() 获取。
+ episode_id: 每集的 ID，如 https://www.bilibili.com/bangumi/play/ep374717

## class BangumiCommentOrder

**Extends: enum.Enum**

短评 / 长评 排序方式

+ DEFAULT: 默认
+ CTIME: 发布时间倒序

---

## class BangumiType

**Extends: enum.Enum**

番剧类型

+ BANGUMI: 番剧
+ FT: 影视
+ GUOCHUANG: 国创

---

## async def get_timeline()

| name | type | description |
| - | - | - |
| type_ | BangumiType | 番剧类型 ｜
| before | int | 几天前开始(0~7), defaults to 7 |
| after | int | 几天后结束(0~7), defaults to 0 |

获取番剧时间线

**Returns:** 调用 API 返回的结果

## class Index_Filter

**Extends: enum.Enum**

番剧索引筛选器

<details>
<summary> 详细参数 </summary>

+ **class Type**: 类型
+ + ANIME: 番剧
+ + MOVIE: 电影
+ + DOCUMENTARY: 纪录片
+ + GUOCHUANG: 国创番剧
+ + TV: 电视剧
+ **class Version**: 版本
+ + ALL: 全部
+ + MAIN: 正片
+ + FILM: 电影
+ + OTHER: 其他
+ **class Spoken_Language**: 配音
+ + ALL: 全部
+ + ORIGINAL: 原声
+ + CHINESE: 中配
+ **class Finish_Status**: 完结状态
+ + ALL: 全部
+ + FINISHED: 已完结
+ + UNFINISHED: 未完结
+ **class Season**: 季度
+ + ALL: 全部
+ + SPRING: 春季
+ + SUMMER: 夏季
+ + AUTUMN: 秋季
+ + WINTER: 冬季 
+ **class Producter**: 制作方
+ + ALL: 全部
+ + CCTV: 央视
+ + BBC: BBC
+ + DISCOVERY: 探索频道
+ + NATIONAL_GEOGRAPHIC: 国家地理
+ + NHK: NHK
+ + HISTORY: 历史频道
+ + STATLLITE: 卫视
+ + SELF: 自制
+ + ITV: ITV
+ + SKY: SKY
+ + ZDF: ZDF
+ + Partner: 合作机构
+ + DOMESTIC_OTHER: 国内其他
+ + FOREIGN_OTHER: 国外其他
+ **class Payment**: 付费条件
+ + ALL: 全部
+ + FREE: 免费
+ + PAID: 付费
+ + VIP: 大会员
+ **class Area**: 地区
+ + ALL: 全部
+ + CHINA: 中国
+ + CHINA_MAINLAND: 中国大陆
+ + CHINA_HONGKONG_AND_TAIWAN: 中国港台
+ + JAPAN: 日本
+ + USA: 美国
+ + UK: 英国
+ + SOUTH_KOREA: 韩国
+ + FRANCE: 法国
+ + GERMANY: 德国
+ + ITALY: 意大利
+ + SPAIN: 西班牙
+ + THAILAND: 泰国
+ + OTHER: 其他
+ **class Style**: 风格
+ + **class ANIME**: 番剧
+ + + 参数见源码
+ + **class MOVIE**: 电影
+ + + 参数见源码
+ + **class GUOCHUANG**: 国创番剧
+ + + 参数见源码
+ + **class TV**: 电视剧
+ + + 参数见源码
+ + **class DOCUMENTARY**: 纪录片
+ +  + 参数见源码
+ + **class Variety**: 综艺
+ + + 参数见源码
+ **class Order**: 排序字段
+ + UPDATE: 更新时间
+ + DANMAKU: 弹幕数
+ + PLAY: 播放量
+ + FOLLOWER: 追番人数
+ + SCORE: 评分
+ + ANIME_RELEASE: 番剧开播日期
+ + MOVIE_RELEASE: 电影上映日期
+ **class Sort**: 排序方式
+ + ASC: 升序
+ + DESC: 降序

</details>

### Functions

#### def make_time_filter()
| name | type | description |
|------|------|-------------|
| start | datetime.datetime, str, int | 开始时间 |
| end | datetime.datetime, str, int | 结束时间 |
| include_start | bool | 是否包含开始时间，默认为 True |
| include_end | bool | 是否包含结束时间，默认为 False |

生成日期区间  
番剧、国创传入年份 (str, int)  
电影、电视剧、纪录片传入日期 (datetime.datetime)

**Returns:** str 时间区间


## class Index_Filter_Meta

Index Filter 元数据
用于传入 get_index_info 方法

子类有 Anime, Movie, Guochuang, TV, Documentary，GuoChuang

<details>
<summary> 详细子类 </summary>

### class Anime

#### Atrributes

| name       | type       | description                    |
|------------|------------|--------------------------------|
| season_type | Index_Filter.Type.ANIME | 索引类型 |
| season_version | Index_Filter.Version | 类型 |
| spoken_language_type | Index_Filter.Spoken_Language | 配音 |
| is_finish | Index_Filter.Finish_Status | 完结状态 |
| copyright | Index_Filter.Copyright | 版权方 |
| season_status | Index_Filter.Payment | 付费条件 |
| season_month | Index_Filter.Season | 季度 |
| area | Index_Filter.Area | 地区 |
| style_id | Index_Filter.Style.ANIME | 风格 |
| year | str | 年份区间 |

#### Functions

##### def \_\_init\_\_()

| name | type | description |
|------|------|-------------|
| version | Index_Filter.Version | 类型 |
| spoken_language | Index_Filter.Spoken_Language | 配音 |
| finish_status | Index_Filter.Finish_Status | 完结状态 |
| copyright | Index_Filter.Copyright | 版权方 |
| payment | Index_Filter.Payment | 付费条件 |
| season | Index_Filter.Season | 季度 |
| area | Index_Filter.Area | 地区 |
| style | Index_Filter.Style.ANIME | 风格 |
| year | str | 调用 Index_Filter.make_time_filter 传入年份 (int, str) 获取 |

### class Movie

#### Atrributes

| name       | type       | description                    |
|------------|------------|--------------------------------|
| season_type | Index_Filter.Type.MOVIE | 索引类型 |
| release_date | str | 上映日期区间 |
| season_status | Index_Filter.Payment | 付费条件 |
| area | Index_Filter.Area | 地区 |
| style_id | Index_Filter.Style.Movie | 风格 |

#### Functions

##### def \_\_init\_\_()

| name | type | description |
|------|------|-------------|
| area | Index_Filter.Area | 地区 |
| style | Index_Filter.Style.MOVIE | 风格 |
| release_date | str | 调用 Index_Filter.make_time_filter 传入时间 (datetime_datetime) 获取 |
| payment | Index_Filter.Payment | 付费条件 |

### class Documentary

#### Atrributes

| name       | type       | description                    |
|------------|------------|--------------------------------|
| season_type | Index_Filter.Type.DOCUMENTARY | 索引类型 |
| release_date | str | 上映日期区间 |
| producer_id | Index_Filter.Producer | 制片方 |
| season_status | Index_Filter.Payment | 付费条件 |
| style_id | Index_Filter.Style.Documentary | 风格 |

#### Functions

##### def \_\_init\_\_()

| name | type | description |
|------|------|-------------|
| payment | Index_Filter.Payment | 付费条件 |
| style | Index_Filter.Style.DOCUMENTARY | 风格 |
| release_date | str | 调用 Index_Filter.make_time_filter 传入时间 (datetime_datetime) 获取 |
| prodcuer | Index_Filter.Producer | 制作方 |

### class TV

#### Atrributes

| name       | type       | description                    |
|------------|------------|--------------------------------|
| season_type | Index_Filter.Type.TV | 索引类型 |
| release_date | str | 上映日期区间 |
| season_status | Index_Filter.Payment | 付费条件 |
| area | Index_Filter.Area | 地区 |
| style_id | Index_Filter.Style.TV | 风格 |

#### Functions.

##### def \_\_init\_\_()

| name | type | description |
|------|------|-------------|
| area | Index_Filter.Area | 地区 |
| style | Index_Filter.Style.TV | 风格 |
| release_date | str | 调用 Index_Filter.make_time_filter 传入时间 (datetime_datetime) 获取 |
| payment | Index_Filter.Payment | 付费条件 |

### class GuoChuang

#### Atrributes

| name       | type       | description                    |
|------------|------------|--------------------------------|
| season_type | Index_Filter.Type.ANIME | 索引类型 |
| season_version | Index_Filter.Version | 类型 |
| is_finish | Index_Filter.Finish_Status | 完结状态 |
| copyright | Index_Filter.Copyright | 版权方 |
| season_status | Index_Filter.Payment | 付费条件 |
| season_month | Index_Filter.Season | 季度 |
| style_id | Index_Filter.Style.ANIME | 风格 |
| year | str | 年份区间 |

#### Functions

##### def \_\_init\_\_()

| name | type | description |
|------|------|-------------|
| version | Index_Filter.Version | 类型 |
| finish_status | Index_Filter.Finish_Status | 完结状态 |
| copyright | Index_Filter.Copyright | 版权方 |
| payment | Index_Filter.Payment | 付费条件 |
| style | Index_Filter.Style.ANIME | 风格 |
| year | str | 调用 Index_Filter.make_time_filter 传入年份 (int, str) 获取 |
---

### class Variety

#### Atrributes

| name       | type       | description                    |
|------------|------------|--------------------------------|
| season_type | Index_Filter.Type.TV | 索引类型 |
| season_status | Index_Filter.Payment | 付费条件 |
| style_id | Index_Filter.Style.TV | 风格 |

#### Functions.

##### def \_\_init\_\_()

| name | type | description |
|------|------|-------------|
| style | Index_Filter.Style.TV | 风格 |
| payment | Index_Filter.Payment | 付费条件 |

</details>

## async def get_index_info

| name | type | description |
|------|------|-------------|
| filters | Index_Filter_Meta | 筛选条件元数据，默认为番剧 |
| order | Index_Filter.Order | 排序方式 默认为最高评分 |
| sort | Index_Filter.Sort | 排序方式，默认为降序 |
| pn | int | 页数，默认为 1 |
| ps | int | 每页数量，默认为 20 |

查询番剧索引，索引的详细参数信息见 Index_Filter_Meta
请先通过 Index_Filter_Meta 构造 filters

**Returns:** dict: 调用 API 返回的结果

## class Bangumi

番剧类

### Atrributes

| name       | type       | description                    |
|------------|------------|--------------------------------|
| credential | Credential | 凭据类                            |
| ep_list    | list       | 获取到的分集列表                       |
| ep_item    | list       | 如果存在有效`epid`则获取对应数据，不存在为`[{}]` |

### Functions

#### def \_\_init\_\_()

| name       | type       | description        |
|------------|------------|--------------------|
| media_id   | int        | 教程 ID（不与番剧相通）      |
| ssid       | int        | 教程季度 ID（不与番剧相通）    |
| epid       | int        | 剧集 ID              |
| oversea    | bool       | 是否采用港澳台 Api(与大陆通用) |
| credential | Credential \| None | 凭据                 |

media_id ，ssid ,epid 三者必须有其一，如果含有所有参数，字段会被提交到Api查询

#### def get_media_id()

获取 media_id

**Returns:** media_id

#### def get_season_id()

获取 season_id

**Returns:** season_id

#### def get_up_info()

获取番剧的上传者信息，一般为哔哩哔哩出差和哔哩哔哩两种

**Returns:** Api 相关字段

#### def get_episode_info()

获取传入的 epid 剧集相对应的各种数据，比如 标题，avid,bvid 等等,如果没有传入 epid 参数将会抛出错误

**Returns:** Api 相关字段

#### def get_raw()

获取初始化得到的，和 get_overview 一个格式的数据

**Returns:** Api 字段

#### async def set_ssid()

设置 season_id

**Returns:** None

#### async def set_media_id()

设置 media_id

**Returns:** None

#### async def get_meta()

获取番剧元数据信息（评分，封面URL，标题等）

**Returns:** dict: 调用 API 返回的结果

#### async def get_short_comment_list()

| name  | type                          | description                                  |
|-------|-------------------------------|----------------------------------------------|
| order | BangumiCommentOrder, optional | 排序方式。Defaults to BangumiCommentOrder.DEFAULT |
| next  | str \| None, optional                 | 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None  |

获取短评列表

**Returns:** dict: 调用 API 返回的结果

#### async def get_long_comment_list()

| name  | type                          | description                                  |
|-------|-------------------------------|----------------------------------------------|
| order | BangumiCommentOrder, optional | 排序方式。Defaults to BangumiCommentOrder.DEFAULT |
| next  | str \| None, optional                 | 调用返回结果中的 next 键值，用于获取下一页数据。Defaults to None  |

获取长评列表

**Returns:** dict: 调用 API 返回的结果

#### async def get_episode_list()

获取季度分集列表

**Returns:** dict: 调用 API 返回的结果

#### async def get_episodes()

获取番剧所有的剧集

**Returns:** List[Episode]: 所有的剧集

#### async def get_stat()

获取番剧播放量，追番等信息

**Returns:** dict: 调用 API 返回的结果

#### async def get_overview()

获取番剧全面概括信息，包括发布时间、剧集情况、stat 等情况

**Returns:** dict: 调用 API 返回的结果

***

## async def set_follow()

| name       | type                 | description           |
|------------|----------------------|-----------------------|
| bangumi    | Bangumi              | 番剧类                   |
| status     | bool, optional       | 追番状态，Defaults to True |
| credential | Credential \| None, optional | 凭据. Defaults to None  |

追番状态设置

**Returns:** dict: 调用 API 返回的结果

## async def update_follow_status()

| name       | type                 | description           |
|------------|----------------------|-----------------------|
| bangumi    | Bangumi              | 番剧类                   |
| status     | int                  | 追番状态，1 想看 2 在看 3 已看 |
| credential | Credential \| None, optional | 凭据. Defaults to None  |

更新已追番状态设置

**Returns:** dict: 调用 API 返回的结果

## class Episode

**Extends: bilibili_api.video.Video**

番剧剧集类

### Atrributes

| name | type | description |
| - | - | - |
| credential | Credential | 凭据类 |
| video_class | Video | 对应视频 |
| bangumi | Bangumi | 对应番剧 |

### Functions

**这里仅列出新增的或重写过的函数，Video 类的其他函数都可使用**

#### def \_\_init\_\_()

| name       | type       | description |
|------------|------------|-------------|
| epid       | int        | epid        | 
| credential | Credential \| None | 凭据          |

#### def get_bangumi()

获取对应的番剧

**Returns:** Bangumi: 番剧类

#### def set_epid()

设置 epid

**Returns:** None

#### def get_epid()

获取 epid

**Returns:** epid

#### async def get_episode_info()

获取番剧单集信息

**Returns:** dict: 调用 API 返回的结果。

#### async def get_download_url()

获取番剧下载链接

**Returns:** dict: 调用 API 返回的结果。

#### async def get_danmaku_view()

获取弹幕设置、特殊弹幕、弹幕数量、弹幕分段等信息。

**Returns:** dict: 二进制流解析结果

#### async def get_danmakus()

| name | type                    | description                           |
|------|-------------------------|---------------------------------------|
| date | datetime.Date, optional | 指定日期后为获取历史弹幕，精确到年月日。Defaults to None. |

获取弹幕

**Returns:** dict\[Danmaku\]: 弹幕列表

#### async def get_danmaku_xml()

获取所有弹幕的 xml 源文件（非装填的弹幕）

**Returns:** str: 文件源

#### async def get_history_danmaku_index()

| name | type                    | description                           |
|------|-------------------------|---------------------------------------|
| date | datetime.Date \| None, optional | 指定日期后为获取历史弹幕，精确到年月日。Defaults to None. |

获取特定月份存在历史弹幕的日期。

**Returns**: None | List[str]: 调用 API 返回的结果。不存在时为 None。

#### async def get_bangumi_from_episode()

获取剧集对应的番剧

**Returns**: Bangumi: 输入的集对应的番剧类
