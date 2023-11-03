# 示例：上传视频

```python
from bilibili_api import sync, video_uploader, Credential

async def main():
    credential = Credential(sessdata="", bili_jct="", buvid3="")
    # 具体请查阅相关文档
    meta = {
        "act_reserve_create": 0,
        "copyright": 1,
        "source": "",
        "desc": "",
        "desc_format_id": 0, 
        "dynamic": "",
        "interactive": 0,
        "no_reprint": 1,
        "open_elec": 0,
        "origin_state": 0,
        "subtitles": {
            "lan": "",
            "open": 0
        },
        "tag": "音乐,音乐综合",
        "tid": 130,
        "title": "title",
        "up_close_danmaku": False,
        "up_close_reply": False,
        "up_selection_reply": False,
        "dtime": 0
    }
    page = video_uploader.VideoUploaderPage(path = 'video.mp4', title = '标题', description = '简介', line=video_uploader.Lines.QN) # 选择七牛线路，不选则自动测速选择最优线路
    uploader = video_uploader.VideoUploader([page], meta, credential, cover = 'cover.png')

    @uploader.on("__ALL__")
    async def ev(data):
        print(data)

    await uploader.start()


sync(main())

```

