"""
ivitools.touch

获取 ivi 文件信息
"""
from bilibili_api import interactive_video

def touch_ivi(path: str):
    print(interactive_video.get_ivi_file_meta(path))
