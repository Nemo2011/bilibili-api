"""
ivitools.ffmpeg

FFmpeg 相关

Licensed under the MIT License. 
"""
import platform
import os
from .chunks import hebing
import zipfile

def freeze_file(part1: str, part2: str):
    hebing(
        os.path.join(os.path.dirname(__file__), part1), 
        os.path.join(os.path.dirname(__file__), part2), 
        os.path.join(os.path.dirname(__file__), "temp.file")
    )
    if os.name == "nt":
        zipfile.ZipFile(open(os.path.join(os.path.dirname(__file__), "temp.file"), "rb")).extractall(
            os.path.dirname(__file__)
        )
    else:
        os.system(f'unzip -o {os.path.join(os.path.dirname(__file__), "temp.file")} -d {os.path.dirname(__file__)}')

def freeze_ffmpeg():
    if "darwin" in platform.system().lower():
        # MacOS
        freeze_file("mac.chunk1", "mac.chunk2")
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "ffmpeg.mac"
        )
    elif "nt" == os.name:
        # Windows
        freeze_file("win.chunk1", "win.chunk2")
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "ffmpeg.exe"
        )
    elif "linux" in platform.platform().lower():
        # Linux
        if os.system("ffmpeg -version") != 0:
            raise SystemError("FFmpeg binary not found. You can install it by apt or yum. \n因为 linux 系统架构类型太多了，不会只有 x64 和 arm，所以这里建议自己编译。")
        return "ffmpeg"
    else:
        raise SystemError("您的系统不受支持：", platform.platform())
