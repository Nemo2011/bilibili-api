from bilibili_api import video, Verify
import json
# 设置验证
verify = Verify(sessdata="your sessdata", csrf="your csrf")
# 初始化VideoInfo类
my_video = video.VideoInfo(aid="40473736", verify=verify)
# 获取视频信息
info = my_video.get_video_info()
# 转换成可格式化JSON并打印
print(json.dumps(info, indent=4, ensure_ascii=False))
