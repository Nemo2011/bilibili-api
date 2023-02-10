"""
ivitools.extract

拆解 ivi 文件相关
"""
import zipfile
import os


def extract_ivi(path: str, dest: str):
    print("Extracting...")
    if not os.path.exists(dest):
        os.makedirs(dest)
    zipfile.ZipFile(path).extractall(dest)
