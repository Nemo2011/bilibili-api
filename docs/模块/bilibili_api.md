# bilibili_api

`import bilibili_api`

通用模块。

## 设置

对API的请求方法进行设置。设置方式如下：

```python
import bilibili_api
bilibili_api.request_settings = {
    "use_https": True,
    "proxies": None
}
```

参数解释：

| 参数名    | 类型 | 默认 | 释义                                                         |
| --------- | ---- | ---- | ------------------------------------------------------------ |
| use_https | bool | True | 使用HTTPS                                                    |
| proxies   | dict | None | 使用代理，参考 [requests 设置代理](https://requests.readthedocs.io/zh_CN/latest/user/advanced.html?highlight=proxies#proxies) |



## 方法

### aid2bvid

av号转bv号。

代码来源：<https://www.zhihu.com/question/381784377/answer/1099438784>

| 参数名 | 类型 | 必须提供 | 默认 | 释义 |
| ------ | ---- | -------- | ---- | ---- |
| aid    | int  | True     | -    | av号 |

### bvid2aid

bv号转av号。

代码来源：<https://www.zhihu.com/question/381784377/answer/1099438784>

| 参数名 | 类型 | 必须提供 | 默认 | 释义 |
| ------ | ---- | -------- | ---- | ---- |
| bvid   | str  | True     | -    | av号 |

### upload_image

上传图片到b站服务器（动态），需要登录。

| 参数名     | 类型 | 必须提供 | 默认 | 释义     |
| ---------- | ---- | -------- | ---- | -------- |
| image_path | str  | True     | -    | 图片路径 |

### get_vote_info

获取投票详细信息。

| 参数名  | 类型 | 必须提供 | 默认 | 释义   |
| ------- | ---- | -------- | ---- | ------ |
| vote_id | int  | True     | -    | 投票ID |

### web_search

在首页以关键字搜索，只指定关键字，其他参数不指定

| 参数名  | 类型 | 必须提供 | 默认 | 释义           |
| ------- | ---- | -------- | ---- | -------------- |
| keyword | str  | True     | -    | 搜索用的关键字 |

**search_type说明：**

| 中文 | 对应的参数    |
| ---- | ------------- |
| 视频 | video         |
| 番剧 | media_bangumi |
| 影视 | media_ft      |
| 直播 | live          |
| 专栏 | article       |
| 话题 | topic         |
| 用户 | bili_user     |

### web_search_video

在首页以关键字搜索视频，只指定关键字，其他参数不指定

| 参数名  | 类型 | 必须提供 | 默认 | 释义           |
| ------- | ---- | -------- | ---- | -------------- |
| keyword | str  | True     | -    | 搜索用的关键字 |

## 类

### Danmaku

获取到的视频弹幕，要发送的视频弹幕和直播弹幕均会使用这个类来传送。

注意，发送弹幕时部分参数无需传入，请自行根据b站弹幕系统规则和常识判断。

#### 实例化参数

| 参数名    | 类型            | 必须提供 | 默认                     | 释义             |
| --------- | --------------- | -------- | ------------------------ | ---------------- |
| text      | str             | True     | -                        | 内容             |
| dm_time   | float           | False    | 0.0                      | 出现时间         |
| send_time | float           | False    | -                        | 发送时间         |
| crc32_id  | str             | False    | None                     | 发送者crc32(uid) |
| mode      | int             | False    | Danmaku.MODE_FLY         | 弹幕显示模式     |
| font_size | int             | False    | Danmaku.FONT_SIZE_NORMAL | 弹幕字体大小     |
| is_sub    | bool            | False    | False                    | 是否为字幕弹幕   |
| color     | [Color](#Color) | False    | 白色                     | 弹幕颜色         |
| weight    | int             | False    | -1                       | 不知道           |
| id_       | int             | False    | -1                       | 弹幕ID           |
| id_str    | str             | False    | ""                       | 弹幕字符串ID     |
| action    | str             | False    | ""                       | 不知道           |
| pool      | int             | False    | -1                       | 不知道           |
| attr      | int             | False    | -1                       | 不知道           |

#### 属性

| 属性名    | 类型               | 释义             |
| --------- | ------------------ | ---------------- |
| text      | str                | 内容             |
| dm_time   | datetime.timedelta | 出现时间         |
| send_time | datetime.datetime  | 发送时间         |
| crc32_id  | str                | 发送者crc32(uid) |
| mode      | int                | 弹幕显示模式     |
| font_size | int                | 弹幕字体大小     |
| is_sub    | bool               | 是否为字幕弹幕   |
| color     | [Color](#Color)    | 弹幕颜色         |
| uid       | int                | 发送者真实UID    |
| weight    | int             | 不知道           |
| id_       | int             | 弹幕ID           |
| id_str    | str            | 弹幕字符串ID     |
| action    | str         | 不知道           |
| pool      | int          | 不知道           |
| attr      | int            | 不知道           |

#### 常量

| 名字                    | 解释     |
| ----------------------- | -------- |
| FONT_SIZE_EXTREME_SMALL | 极小字体 |
| FONT_SIZE_SUPER_SMALL   | 超小字体 |
| FONT_SIZE_SMALL         | 小字体   |
| FONT_SIZE_BIG           | 大字体   |
| FONT_SIZE_SUPER_BIG     | 超大字体 |
| FONT_SIZE_EXTREME_BIG   | 极大字体 |
| FONT_SIZE_NORMAL        | 标准字体 |
| MODE_FLY                | 飞行弹幕 |
| MODE_TOP                | 顶部弹幕 |
| MODE_BOTTOM             | 底部弹幕 |
| MODE_REVERSE            | 反向弹幕 |
| TYPE_NORMAL             | 普通弹幕 |
| TYPE_SUBTITLE           | 字幕弹幕 |

#### 方法

##### crack_uid

破解发送者UID，即弹幕发送者反查。

代码翻译自：<https://github.com/esterTion/BiliBili_crc2mid>



### Verify

验证类，用于传入各种方法中。

获取参数方法见 [获取_SESSDATA_和_CSRF](/README.md#获取-sessdata-和-csrf)

#### 实例化参数

| 参数名   | 类型 | 必须提供 | 默认 | 释义 |
| -------- | ---- | -------- | ---- | ---- |
| sessdata | str  | False    | None | -    |
| csrf     | str  | False    | None | -    |

#### 属性

同参数

#### 方法

##### get_cookies

获取cookies

##### has_sess

是否存在sessdata

##### has_csrf

是否存在csrf

##### check

检查权限情况。

```
-1: csrf 校验失败
-2: SESSDATA值有误
-3: 未提供SESSDATA
```

~~会偷偷给视频 BV1uv411q7Mv 点个赞~~



### Color

颜色类，一般用于Danmaku类。

#### 实例化参数

| 参数名 | 类型 | 必须提供 | 默认   | 释义            |
| ------ | ---- | -------- | ------ | --------------- |
| hex_   | str  | False    | FFFFFF | 十六进制RGB颜色 |

#### 属性

不允许直接操作

#### 方法

##### set_hex_color

设置十六进制颜色

| 参数名    | 类型 | 必须提供 | 默认 | 释义            |
| --------- | ---- | -------- | ---- | --------------- |
| hex_color | str  | True     |      | 十六进制RGB颜色 |

##### set_rgb_color

设置RGB颜色值

| 参数名 | 类型 | 必须提供 | 默认 | 释义     |
| ------ | ---- | -------- | ---- | -------- |
| r      | int  | True     |      | 红色分量 |
| g      | int  | True     |      | 绿色分量 |
| b      | int  | True     |      | 蓝色分量 |

##### set_dec_color

设置十进制颜色值

| 参数名 | 类型 | 必须提供 | 默认 | 释义       |
| ------ | ---- | -------- | ---- | ---------- |
| color  | int  | True     |      | 十进制颜色 |

##### get_hex_color

获取十六进制颜色

##### get_rgb_color

获取RGB颜色值

return r, g, b

##### get_dec_color

获取十进制颜色值