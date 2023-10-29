# 示例：上传视频

```python
from bilibili_api import sync, video_uploader, Credential

async def main():
    credential = Credential(sessdata="", bili_jct="", buvid3="")
    # 具体请查阅相关文档和 VideoMeta 内代码注释
    # 建议使用 VideoMeta 类来构建 meta 信息，避免参数错误，但也兼容直接传入 dict
    # meta = {
    #     "act_reserve_create": 0,
    #     "copyright": 1,
    #     "source": "",
    #     "desc": "",
    #     "desc_format_id": 0, 
    #     "dynamic": "",
    #     "interactive": 0,
    #     "no_reprint": 1,
    #     "open_elec": 0,
    #     "origin_state": 0,
    #     "subtitles": {
    #         "lan": "",
    #         "open": 0
    #     },
    #     "tag": "音乐,音乐综合",
    #     "tid": 130,
    #     "title": "title",
    #     "up_close_danmaku": False,
    #     "up_close_reply": False,
    #     "up_selection_reply": False,
    #     "dtime": 0
    # }
    vu_meta = video_uploader.VideoMeta(tid=130, title='title', tags=['音乐综合', '音乐'], desc='', cover="/cover.png", no_reprint=True)
    # await vu_meta.verify(credential=credential) # 本地预检 meta 信息，出错则抛出异常
    page = video_uploader.VideoUploaderPage(path = 'video.mp4', title = '标题', description='简介', line=video_uploader.Lines.QN) # 选择七牛线路，不选则自动测速选择最优线路
    uploader = video_uploader.VideoUploader([page], vu_meta, credential)
    # uploader = video_uploader.VideoUploader([page], meta, credential, cover='cover.png') 
    # # meta 直接传入 dict 则需要手动传入封面

    @uploader.on("__ALL__")
    async def ev(data):
        print(data)

    await uploader.start()


sync(main())

```

