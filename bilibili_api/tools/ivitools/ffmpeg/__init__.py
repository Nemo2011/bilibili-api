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
    os.system(f'unzip -o {os.path.join(os.path.dirname(__file__), "temp.file")}')

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
        if "arm" in platform.platform().lower():
            # Linux arm
            freeze_file("linux.arm.chunk1", "linux.arm.chunk2")
            return os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "ffmpeg",
                "ffmpeg.arm.linux"
            )
        else:
            # Linux x64
            freeze_file("linux.x64.chunk1", "linux.x64.chunk2")
            return os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "ffmpeg",
                "ffmpeg.x64.linux"
            )
    else:
        raise SystemError("您的系统不受支持：", platform.platform())
