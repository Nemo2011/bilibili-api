# bangumi 模块

番剧模块。

## 名词解释

**media_id**：番剧季度id，例：<https://www.bilibili.com/bangumi/media/md4316442>

**season_id**：也是番剧季度id，链接中附上会导向番剧第一集。例：<https://www.bilibili.com/bangumi/play/ss26291/>

搞不懂这两个到底有什么关系，目前就我的观察情况来看，media_id和season_id是一一对应的，如果是早期的番剧这两个值相等。总之根据需要传入就行了。season_id可以在 [get_meta](#get_meta) 中获取到。

**epid**：番剧单集ID，例：<https://www.bilibili.com/bangumi/play/ep259664>

## 方法

### get_collective_info

获取总体信息，结合 get_episode_info 和 get_meta 等

| 参数名   | 类型 | 必须提供 | 默认 | 释义 |
| -------- | ---- | -------- | ---- | ---- |
| season_id | int  | True     | -    |     |

### get_episode_info

获取番剧单集信息

| 参数名   | 类型 | 必须提供 | 默认 | 释义 |
| -------- | ---- | -------- | ---- | ---- |
| epid | int  | True     | -    |   https://www.bilibili.com/bangumi/play/ep259653   |

可以从中提取bv号，然后当做普通的视频用video模块去获取其他信息。

### get_meta

获取番剧元数据信息（评分，封面URL，标题等）

| 参数名   | 类型 | 必须提供 | 默认 | 释义 |
| -------- | ---- | -------- | ---- | ---- |
| media_id | int  | True     | -    |      |

### get_short_comments_raw

低层级API，获取番剧短评。

| 参数名   | 类型 | 必须提供 | 默认    | 释义                                |
| -------- | ---- | -------- | ------- | ----------------------------------- |
| media_id | int  | True     | -       |                                     |
| ps       | int  | False    | 20      | 每页数量                            |
| sort     | str  | False    | default | 排序依据，default默认time按时间排序 |
| cursor   | str  | False    | None    | 返回值中的next，获取下一页用        |

### get_short_comments

获取番剧短评

| 参数名   | 类型 | 必须提供 | 默认    | 释义                                |
| -------- | ---- | -------- | ------- | ----------------------------------- |
| media_id | int  | True     | -       |                                     |
| sort     | str  | False    | default | 排序依据，default默认time按时间排序 |

参照：[循环获取数据参数说明][循环获取数据参数说明]

### get_long_comments_raw

低层级API，获取番剧长评。

| 参数名   | 类型 | 必须提供 | 默认    | 释义                                |
| -------- | ---- | -------- | ------- | ----------------------------------- |
| media_id | int  | True     | -       |                                     |
| ps       | int  | False    | 20      | 每页数量                            |
| sort     | str  | False    | default | 排序依据，default默认time按时间排序 |
| cursor   | str  | False    | None    | 返回值中的next，获取下一页用        |

### get_long_comments

获取番剧长评

| 参数名   | 类型 | 必须提供 | 默认    | 释义                                |
| -------- | ---- | -------- | ------- | ----------------------------------- |
| media_id | int  | True     | -       |                                     |
| sort     | str  | False    | default | 排序依据，default默认time按时间排序 |

参照：[循环获取数据参数说明][循环获取数据参数说明]

### get_episodes_list

获取番剧剧集列表

| 参数名    | 类型 | 必须提供 | 默认 | 释义 |
| --------- | ---- | -------- | ---- | ---- |
| season_id | int  | True     | -    |      |

### get_interact_list

获取番剧播放量，追番人数等信息

| 参数名    | 类型 | 必须提供 | 默认 | 释义 |
| --------- | ---- | -------- | ---- | ---- |
| season_id | int  | True     | -    |      |

### set_follow

设置追番状态

| 参数名    | 类型 | 必须提供 | 默认 | 释义 |
| --------- | ---- | -------- | ---- | ---- |
| season_id | int  | True     | -    |      |
| status    | bool | False    | True | 状态 |

### set_follow_status

设置追番状态（想看，在看，已看）

| 参数名    | 类型 | 必须提供 | 默认 | 释义            |
| --------- | ---- | -------- | ---- | --------------- |
| season_id | int  | True     | -    |                 |
| status    | int  | False    | 2    | 1想看2在看3已看 |

### share_to_dynamic

分享到动态。

| 参数名  | 类型 | 必须提供 | 默认 | 释义     |
| ------- | ---- | -------- | ---- | -------- |
| content | str  | True     | -    | 动态内容 |
| epid    | int  | True     | -    |          |







[循环获取数据参数说明]: /docs/通用解释.md#循环获取数据参数说明