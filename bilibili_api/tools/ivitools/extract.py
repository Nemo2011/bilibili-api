"""
ivitools.extract

拆解 ivi 文件相关
"""
import os
import zipfile


def extract_ivi(path: str, dest: str):
    print("Extracting...")
    if not os.path.exists(dest):
        os.makedirs(dest)
    zipfile.ZipFile(path).extractall(dest)
