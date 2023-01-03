"""
ivitools.ffmpeg

FFmpeg 相关

Licensed under the MIT License. 
"""
import platform
import os
import zipfile

def freeze_ffmpeg():
    if "nt" == os.name:
        # Windows
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "ffmpeg.exe"
        )
    else:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "ffmpeg"
        )
