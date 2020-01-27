from bilibili_api import video
import json
my_video = video.VideoInfo(aid="40473736")
info = my_video.get_video_info()
print(json.dumps(my_video, indent=4, ensure_ascii=False))