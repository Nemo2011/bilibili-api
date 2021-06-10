import os
import asyncio
from bilibili_api import video, Credential
import re


SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""

UPLOAD_CONFIG = {
  "copyright": 1, #"1 自制，2 转载。",
  "source": "", #"str, 视频来源。投稿类型为转载时注明来源，为原创时为空。",
  "desc": "", #"str, 视频简介。",
  "desc_format_id": 0,
  "dynamic": "", #"str, 动态信息。",
  "interactive": 0,
  "open_elec": 0, #"int, 是否展示充电信息。1 为是，0 为否。",
  "no_reprint": 1, #"int, 显示未经作者授权禁止转载，仅当为原创视频时有效。1 为启用，0 为关闭。",
  "subtitles": {
    "lan": "", #"字幕语言，不清楚作用请将该项设置为空",
    "open": 0
  },
  "tag": "学习,测试", #"str, 视频标签。使用英文半角逗号分隔的标签组。示例：标签1,标签2,标签3",
  "tid": 208, #"int, 分区ID。可以使用 channel 模块进行查询。",
  #"title": "英语测试第一弹", #"视频标题",
  "up_close_danmaku": False, #"bool, 是否关闭弹幕。",
  "up_close_reply": False, #"bool, 是否关闭评论。",
}

async def upload_video(video_file, cover_img, extension, title):
  cover = open(cover_img, "r+b")
  filename = os.path.basename(video_file).split(".")[0]
  print(filename)
  v = video.VideoUploaderPageObject(video_stream=open(video_file, "r+b"), title=filename, extension=extension)

  config = UPLOAD_CONFIG
  config["title"] = title

  credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)

  uploader = video.VideoUploader(cover=cover, cover_type="jpg", pages=[v], config=config, credential=credential) 

  await uploader.start()

if __name__ == '__main__':
  img_123 = "123.jpg"
  img_124 = "124.jpg"
  img_125 = "125.jpg"
  img_126 = "126.jpg"

  mp4_video = "example.mp4"
  mov_video = "example.mov"
  avi_video = "example.avi"
  wmv_video = "example.wmv"
  
  asyncio.get_event_loop().run_until_complete(upload_videos(mp4_video, img_123, 'mp4', "first mp4"))
  asyncio.get_event_loop().run_until_complete(upload_video(mov_video, img_124, 'mov', "first mov"))
  asyncio.get_event_loop().run_until_complete(upload_video(avi_video, img_125, 'avi', "first avi"))
  asyncio.get_event_loop().run_until_complete(upload_video(wmv_video, img_126, 'wmv', "first wmv"))

  
