# Module bilibili_api

```typescript
import {} from "bilibili-api-ts";
```

根模块

## let Record\<string, string\> HEADERS

访问 bilibili 视频下载链接等内部网址用的 HEADERS

---

## class Credential

凭据类，用于各种请求操作的验证。

### Functions

#### _constructor_

| name     | type          | description                         |
| -------- | ------------- | ----------------------------------- |
| sessdata | string, optional | 浏览器 Cookies 中的 SESSDATA 字段值 |
| bili_jct | string, optional | 浏览器 Cookies 中的 bili_jct 字段值 |
| dedeuserid   | string, optional | 浏览器 Cookies 中的 DedeUserID 字段值   |

各字段获取方式查看：https://nemo2011.github.io/bilibili_api/#/get-credential.md

#### function get_cookies()

获取请求 Cookies 字典

**Returns:** Record\<string, string\>: 请求 Cookies 字典

#### function has_sessdata()

是否提供 sessdata。

**Returns:** boolean

#### function has_bili_jct()

是否提供 bili_jct。

**Returns:** boolean

#### function has_dedeuserid()

是否提供 dedeuserid。

**Returns:** bool

#### function raise_for_no_sessdata()

没有提供 sessdata 则抛出异常。

**Returns:** None

#### function raise_for_no_bili_jct()

没有提供 bili_jct 则抛出异常。

**Returns:** None

#### function raise_for_no_dedeuserid()

没有提供 dedeuserid 则抛出异常。

**Returns:** None

---

## function aid2bvid()

| name | type | description |
| ---- | ---- | ----------- |
| aid  | int  | AV 号       |

AV 号转 BV 号。

**Returns:** str: BV 号。

---

## function bvid2aid()

| name | type | description |
| ---- | ---- | ----------- |
| bvid | str  | BV 号。     |

BV 号转 AV 号。

**Returns:** int: AV 号。
