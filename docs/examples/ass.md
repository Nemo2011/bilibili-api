# 示例：下载视频的弹幕

``` python
from bilibili_api import *

v = video.Video("BV1P24y1a7Lt")  # 初始化视频对象

sync(ass.make_ass_file_danmakus_protobuf(
    obj=v, # 生成弹幕文件的对象
    page=0, # 哪一个分 P (从 0 开始)
    out="test.ass" # 输出文件地址
))

# test.ass 即为弹幕文件

# make_ass_file_danmakus_protobuf 代表从 protobuf 格式的新接口中抓取弹幕
# make_ass_file_danmakus_xml 代表从旧的 xml 接口中抓取弹幕
```
