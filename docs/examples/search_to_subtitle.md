# 示例：从搜索 query 到获取视频字幕

这个流程适合“先搜视频，再把字幕拿出来”的场景。

整体分 5 步：

1. 用 `search.search_by_type()` 搜索视频
2. 从搜索结果里挑一个目标视频，拿到 `bvid`
3. 用 `video.Video(...).get_info()` 取视频详情，拿到第一页的 `cid`
4. 用 `get_subtitle()` 取字幕轨道信息
5. 用 `ass.request_subtitle()` 拉字幕正文，再转成 JSON / SRT / ASS / LRC

## 前提

字幕这条链路通常需要登录态。

至少准备这些 Cookie 字段：

- `SESSDATA`
- `bili_jct`
- `DedeUserID`
- `buvid3`，建议带上

可以直接从环境变量里读：

```python
import os
from bilibili_api import Credential

credential = Credential(
    sessdata=os.environ["BILI_SESSDATA"],
    bili_jct=os.environ["BILI_CSRF"],
    buvid3=os.environ.get("BILI_BUVID3", ""),
    dedeuserid=os.environ["BILI_DEDEUSERID"],
)
```

## 完整示例

下面这段代码会：

- 搜索 `TED`
- 取搜索结果里的第一个视频
- 打印可用字幕轨道
- 下载默认字幕正文
- 输出前 10 条简化字幕
- 顺手写出一个 `subtitle.srt`

```python
import asyncio
import json
import os

from bilibili_api import Credential, ass, search, video
from bilibili_api.search import SearchObjectType


QUERY = "TED"


async def main() -> None:
    credential = Credential(
        sessdata=os.environ["BILI_SESSDATA"],
        bili_jct=os.environ["BILI_CSRF"],
        buvid3=os.environ.get("BILI_BUVID3", ""),
        dedeuserid=os.environ["BILI_DEDEUSERID"],
    )

    # 1. 搜索视频
    search_result = await search.search_by_type(
        QUERY,
        search_type=SearchObjectType.VIDEO,
        page=1,
        page_size=10,
    )
    first = search_result["result"][0]
    bvid = first["bvid"]

    # 2. 实例化视频对象
    v = video.Video(bvid=bvid, credential=credential)

    # 3. 获取视频信息，拿到第一页 cid
    info = await v.get_info()
    cid = info["pages"][0]["cid"]

    print("title:", info["title"])
    print("bvid:", info["bvid"])
    print("aid:", info["aid"])
    print("cid:", cid)

    # 4. 获取字幕轨道信息
    subtitle_meta = await v.get_subtitle(cid=cid)
    subtitles = subtitle_meta.get("subtitles", [])
    print("subtitle tracks:")
    for item in subtitles:
        print(" -", item["lan"], item["lan_doc"], item["subtitle_url"])

    if not subtitles:
        print("这个视频当前没有可用字幕")
        return

    # 5. 拉字幕正文
    subtitle_obj = await ass.request_subtitle(
        obj=v,
        cid=cid,
        credential=credential,
    )

    subtitle_json = await subtitle_obj.request_ass_data_json()
    simple_json = subtitle_obj.to_simple_json()
    srt_text = subtitle_obj.to_srt()

    print("subtitle body count:", len(subtitle_json["body"]))
    print(json.dumps(simple_json[:10], ensure_ascii=False, indent=2))

    with open("subtitle.srt", "w+", encoding="utf-8") as f:
        f.write(srt_text)


if __name__ == "__main__":
    asyncio.run(main())
```

## 每一步拿到的关键数据

### 1. 搜索结果

`search.search_by_type()` 返回搜索结果列表，里面最关键的是：

- `bvid`
- `aid`
- `title`

你也可以自己加一层筛选逻辑，比如：

- 标题命中关键词
- 时长范围
- 播放量
- 发布时间

### 2. 视频详情

`v.get_info()` 返回完整视频信息。

取字幕时最关键的是 `pages`：

```python
info = await v.get_info()
cid = info["pages"][0]["cid"]
```

如果视频有多个分 P：

- `pages[0]` 是第一 P
- `pages[1]` 是第二 P
- 也可以自己遍历每个 `cid` 分别抓字幕

### 3. 字幕轨道信息

`await v.get_subtitle(cid=cid)` 返回的是字幕轨道列表，不是字幕正文。

通常会看到这样的字段：

- `lan`：语言代码，比如 `zh-Hans`、`en-US`、`ai-zh`
- `lan_doc`：人类可读语言名
- `subtitle_url`：字幕 JSON 地址

### 4. 字幕正文

`ass.request_subtitle()` 会继续访问 `subtitle_url`，把正文 JSON 拉下来。

拿到 `AssSubtitleObject` 之后，可以转多种格式：

```python
subtitle_obj = await ass.request_subtitle(obj=v, cid=cid, credential=credential)

raw_json = await subtitle_obj.request_ass_data_json()
simple_json = subtitle_obj.to_simple_json()
srt_text = subtitle_obj.to_srt()
ass_text = subtitle_obj.to_ass()
lrc_text = subtitle_obj.to_lrc()
```

## 常见情况

### 1. 未登录直接报错

常见报错是：

```python
CredentialNoSessdataException
```

这说明当前接口链路要求 `SESSDATA`。

### 2. 有登录态，但 `subtitles` 还是空

这通常说明：

- 这个视频本身没有上传字幕
- 这个视频当前没有自动字幕
- 你拿错了分 P 的 `cid`

可以先打印：

```python
subtitle_meta = await v.get_subtitle(cid=cid)
print(subtitle_meta)
```

### 3. 想指定某一种字幕语言

可以传 `lan_code` 或 `lan_name`：

```python
subtitle_obj = await ass.request_subtitle(
    obj=v,
    cid=cid,
    credential=credential,
    lan_code="en-US",
)
```

或者：

```python
subtitle_obj = await ass.request_subtitle(
    obj=v,
    cid=cid,
    credential=credential,
    lan_name="中文（简体）",
)
```

## 一个更像“工作流”的最小版本

如果你只想记住最短路径，可以看这个：

```python
search_result = await search.search_by_type(query, search_type=SearchObjectType.VIDEO)
bvid = search_result["result"][0]["bvid"]

v = video.Video(bvid=bvid, credential=credential)
info = await v.get_info()
cid = info["pages"][0]["cid"]

subtitle_obj = await ass.request_subtitle(v, cid=cid, credential=credential)
subtitle_items = subtitle_obj.to_simple_json()
```

这几行就是：

`query -> bvid -> cid -> subtitle_url -> subtitle body`
