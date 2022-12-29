"""
ivitools.scan

扫描 ivi 文件相关
"""
import os
from bilibili_api.interactive_video import get_ivi_file_meta
from colorama import Fore, Cursor
from colorama.ansi import clear_line
import zipfile
import tempfile
import time
import json
from tqdm import tqdm

def scan_ivi_file(path: str):
    print(Fore.RESET + f"Scanning {path} ...")
    # First, make a temp folder. 
    tmp_dir = tempfile.gettempdir()
    if not os.path.exists(os.path.join(tmp_dir, "ivitools")):
        os.mkdir(os.path.join(tmp_dir, "ivitools"))
    for root, dirs, files in os.walk(os.path.join(tmp_dir, "ivitools"), topdown = False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    # Then, extract the ivi file. 
    extract_dir = os.path.join(tmp_dir, "ivitools", str(time.time())) 
                                                    # Use the time to make folders different
    zipfile.ZipFile(open(path, "rb")).extractall(extract_dir)
    # Finally, display the result. 
    Cursor.UP()
    clear_line()
    print(path)
    meta = get_ivi_file_meta(path)
    print(f'{meta["title"]}({meta["bvid"]})')
    graph = json.load(open(os.path.join(extract_dir, "ivideo.json"), encoding = "utf-8"))
    print(f"There're {len(graph.keys())} nodes in the file! ")
    bar = tqdm(graph.keys())
    for item in bar:
        bar.set_description("Scanning node ")
        if not ("cid" in graph[str(item)].keys()):
            raise Exception(f"Missing CID in the node {item}")
            return
        else:
            cid = graph[str(item)]["cid"]
        if not (os.path.exists(os.path.join(extract_dir, str(cid) + ".video.mp4"))):
            raise Exception(f"Missing video source of the node {item}")
        time.sleep(0.01)
    print(Fore.GREEN + "Congratulation! Your file is OK. ", Fore.RESET)
