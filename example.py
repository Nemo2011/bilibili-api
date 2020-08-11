from bilibili_api import video
import json

v = video.get_video_info(bvid="BV1uv411q7Mv")

print(json.dumps(v, indent=4, ensure_ascii=False))