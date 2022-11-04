# 示例：上传视频

```python
from bilibili_api import sync, video_uploader, Credential

async def main():
    credential = Credential(sessdata="", bili_jct="", buvid3="")
    # 具体请查阅相关文档
    meta = {
            "copyright": 1,
            "source": "",
            "desc": "desc",
            "desc_format_id": 0,
            "dynamic": "233",
            "interactive": 0,
            "open_elec": 1,
            "no_reprint": 1,
            "subtitles": {
                "lan": "",
                "open": 0
            },
            "tag": "标签1,标签2,标签3",
            "tid": 21,
            "title": "title",
            "up_close_danmaku": True,
            "up_close_reply": True
        }
    page = video_uploader.VideoUploaderPage(path = 'video.mp4', title = '标题', description = '简介')
    uploader = video_uploader.VideoUploader([page], meta, credential, cover_path = 'cover.png')

    @uploader.on("__ALL__")
    async def ev(data):
        print(data)

    await uploader.start()


sync(main())

```

