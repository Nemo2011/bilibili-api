import os
import asyncio
from bilibili_api import video, interactive_video, Credential
import re
from best_story import Oscar
import json
import time

SESSDATA = "记得填" 
BILI_JCT = "记得填"
BUVID3 = "记得填"

def reform_videos(videos):
  video_objs = {}
  for v in videos:
    video_objs[v["title"]] = v 
  return video_objs

async def save_tree(bvid):
  # 实例化 Credential 类
  credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)

  # 实例化 Video 类
  v = interactive_video.IVideo(bvid=bvid, credential=credential)

  # 查询交互视频信息
  info = await v.get_pages()
  vobjs = reform_videos(info["videos"])
  aid = info["videos"][0]["aid"]

  # 自定义一个情节树
  g = Oscar(videos=vobjs, aid=aid)
  g.gen_simple_graph(root_title="root") # 记得改 pick one video title 
  g.graph.pretty_print()
  story = json.dumps({"graph": g.graph._serialize()})
  #print(story)
  
  # 上传情节树
  graph_result = await v.submit_story_tree(story)
  return graph_result


UPLOAD_CONFIG = {
  "copyright": 1, #"1 自制，2 转载。",
  "source": "", #"str, 视频来源。投稿类型为转载时注明来源，为原创时为空。",
  "desc": "", #"str, 视频简介。",
  "desc_format_id": 0,
  "dynamic": "", #"str, 动态信息。",
  "interactive": 1,
  "open_elec": 0, #"int, 是否展示充电信息。1 为是，0 为否。",
  "no_reprint": 1, #"int, 显示未经作者授权禁止转载，仅当为原创视频时有效。1 为启用，0 为关闭。",
  "subtitles": {
    "lan": "", #"字幕语言，不清楚作用请将该项设置为空",
    "open": 0
  },
  "tag": "学习,测试", #"str, 视频标签。使用英文半角逗号分隔的标签组。示例：标签1,标签2,标签3",
  "tid": 208, #"int, 分区ID。可以使用 channel 模块进行查询。",
  #"title": "jump jump jump", #"视频标题",
  "up_close_danmaku": False, #"bool, 是否关闭弹幕。",
  "up_close_reply": False, #"bool, 是否关闭评论。",
}

async def upload_videos(video_dir, cover_img, title):
  # 上传多P视频到互动视频
  cover = open(cover_img, "r+b")

  videos = []
  for filename in os.listdir(video_dir):
    if filename.endswith(".mp4"): 
      video_file = os.path.join(video_dir, filename)
      print(video_file)
      videos.append(video.VideoUploaderPageObject(video_stream=open(video_file, "r+b"), title=filename.split(".")[0]))

  config = UPLOAD_CONFIG
  config["title"] = title

  credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)

  uploader = video.VideoUploader(cover=cover, cover_type="jpg", pages=videos, config=config, credential=credential) 

  info =  await uploader.start()

  return info

if __name__ == '__main__':
  folder = "directory contains video files" # 记得填
  img = "image file path" # 记得填
  title = "interactive video name" # 记得填

  info = asyncio.get_event_loop().run_until_complete(upload_videos(folder, img, title))
  print(info) # {"bvid": "ssssss", "aid": ddddddd}
  bvid = info["bvid"]
  time.sleep(120) # 为了 B 站视频编码的时间, 躺平 2 分钟
  graph_result = asyncio.get_event_loop().run_until_complete(save_tree(bvid))
  print(graph_result) # 成功之后，编辑树会延迟，不超过5分钟。 如果觉得有问题，就在执行一次上个存树的命令, 这时多半立即执行，推测是队列机制。
  
