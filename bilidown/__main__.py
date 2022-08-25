r"""
BiliDown: 哔哩哔哩命令行下载器
"""

import os
import time
from typing import List, Union
from bilibili_api import *
from bilibili_api.exceptions import *
import sys
import httpx
import requests
import signal
from colorama import Fore, Back, Style, init

PROXY = None
PATH = "#default"
PATHS = []
RPATH = ""
DIC = "."
FFMPEG = "ffmpeg"
DEFAULT_SETTINGS = False
VIDEO_QUALITY = {
    126: "杜比视界",
    125: "真彩 HDR",
    120: "超清 4K",
    116: "高清 1080P60",
    112: "高清 1080P+",
    80: "高清 1080P",
    64: "高清 720P60",
    32: "清晰 480P",
    16: "流畅 360P",
}
VIDEO_CODECS = {"hev": "HEVC(H.265)", "avc": "AVC(H.264)", "av01": "AV1"}
AUDIO_QUALITY = {30280: "高品质", 30232: "中等品质", 30216: "低品质"}
CREDENTIAL = Credential()
DOWNLOAD_DANMAKUS = "ask"  # (true|false|only)
DOWNLOAD_LIST = False
BANNER = r"""
                                         _____
________   ___   ___        ___          |   |
|\   __  \ |\  \ |\  \      |\  \        |   |
\ \  \|\ /_\ \  \\ \  \     \ \  \       |   |
 \ \   __  \\ \  \\ \  \     \ \  \    --     --
  \ \  \|\  \\ \  \\ \  \____ \ \  \   \       /
   \ \_______\\ \__\\ \_______\\ \__\   \     /
    \|_______| \|__| \|_______| \|__|    \   /
                                          \_/
"""


def _exit(*args, **kwargs):
    exit()


signal.signal(signal.SIGINT, _exit)

init(autoreset=True)


def _ask_settings_download(question: str):
    global DEFAULT_SETTINGS, DOWNLOAD_LIST
    if "下载的分 P" in question and DOWNLOAD_LIST:
        return "all"
    if DEFAULT_SETTINGS:
        return ""
    else:
        return input(question)


def _download(url: str, out: str, description: str):
    """
    下载函数
    """
    global PROXY
    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"},
        proxies={"all://": PROXY},
        stream=True
    )
    resp.raise_for_status()

    if os.path.exists(out):
        os.remove(out)

    print(Fore.MAGENTA + f"DWN: 开始下载 {description} 至 {out}")

    all_length = int(resp.headers["Content-Length"])
    parts = all_length // 1024 + (1 if all_length % 1024 != 0 else 0)
    cnt = 0
    start_time = time.perf_counter()
    print(Fore.MAGENTA + "DWN: " + str(cnt) + "\r", end="")

    with open(out, "wb") as f:
        for chunk in resp.iter_content(1024):
            cnt += 1
            print(Fore.MAGENTA + "DWN: " + str(int(time.perf_counter() - start_time)) + "s. Done " + str(cnt) + " parts. All " + str(parts) + " parts. (1 part = 1024 bytes)" + "\r", end="")
            f.write(chunk)
    print()
    print(Fore.MAGENTA + "DWN: 完成下载")
    return out



def _require_file_type(filename: str, filetype: str):
    """
    自动修改文件后缀
    """
    if filename == "#default":
        return filename
    if filename.rstrip(filetype) == filename:
        print(Fore.YELLOW + f"WRN: 识别到您的输出文件类型可能有误 (提供的文件名 {filename} 目标{filetype})")
        print(Fore.YELLOW + f"WRN: 您可以使用参数 --disable-filetype-check 忽略")
        repair = input(Fore.BLUE + f"Y/N: 是否自动修复(默认为修复): ")
        if repair.upper() == "N":
            return filename
        else:
            if len(filename.split(".")) == 1:
                print(Fore.YELLOW + f"WRN: 自动添加成 {filename + filetype}")
                return filename + filetype
            now_name = "".join(filename.split(".")[:-1]) + filetype
            print(Fore.YELLOW + f"WRN: 自动替换成 {now_name}")
            return now_name
    else:
        return filename


def _require_ass_for_danmakus(filename: str):
    global DOWNLOAD_DANMAKUS
    if DOWNLOAD_DANMAKUS.upper() == "ONLY":
        return _require_file_type(filename, ".ass")
    else:
        if filename == filename.rstrip(".ass"):
            now_name = "".join(filename.split(".")[:-1]) + ".ass"
            return now_name
    return filename


def _help():
    """
    显示帮助
    """
    print()
    print('使用方法: bilidown "https://bilibili.com/.../"', end=" ")
    print(Fore.RED + '链接为第一个参数, 允许多个链接, 请使用 "|" 隔开每一个链接' + Fore.RESET)
    print(
        '参数:   --out/-o                  文件名(默认为 "#default")                                   "a.mp4"',
        end=" ",
    )
    print(Fore.RED + '允许多个输出文件名, 请使用 "|" 隔开每一个输出文件名' + Fore.RESET)
    print(
        '参数:   --dic/-d                  下载至文件夹(默认为 "default")                              "~/Desktop"'
    )
    print(
        '参数:   --proxy                   代理                                                        "https://user:password@your-proxy.com"'
    )
    print(
        '参数:   --ffmpeg                  ffmpeg 地址(如果没有 ffmpeg 可以使用 "#none")               "ffmpeg"'
    )
    print(
        '参数:   --sessdata                Cookies 中 SESSDATA 的值, 用于下载会员专享、高清晰度        "SECRET绝密SECRET绝密"'
    )
    print(
        "参数:   --danmakus-settings       是否下载弹幕"
        + '                                                "true"'
        + Fore.RED
        + " ( true 下载 | false 不下载 | only 只下载弹幕 ) "
    )
    print(
        "参数:   --default-settings        下载时使用默认设置(视频和专栏)                             "
        + Fore.RED
        + " (分 P, 清晰度, 音质, 视频编码, 专栏下载格式)"
    )
    print("参数:   --disable-filetype-check  忽略自动检查文件后缀")
    print("参数:   --download-list           下载视频、音频对应的列表(番剧所有剧集、视频所有分 P、歌单所有音频)")
    print("参数:   --debug                   显示错误详细信息")
    print("参数:   -h                        帮助")
    print()
    print(
        Fore.LIGHTRED_EX
        + "参数 --out/-o 允许使用自定义格式, 如 "
        + Fore.GREEN
        + '"{title} - {bvid} - P{p} - {owner} - {uid}"'
        + Fore.RED
        + " 请务必使用小写"
    )
    print(
        "| {bvid}         -> BVID            | {aid}          -> AID            | {title}        -> 标题      | {p}            -> 分 P        |"
    )
    print(
        "| {owner}        -> UP              | {uid}          -> UP uid         | {bangumi_epid} -> 番剧 epid | {bangumi_name} -> 番剧名      |"
    )
    print(
        "| {bangumi_ep}   -> 番剧第几集      | {cheese_epid}  -> 课程 epid      | {cheese_name}  -> 课程名    | {cheese_ep}    -> 课程第几集  |"
    )
    print(
        "| {bangumi_id}   -> 番剧 season_id  | {cheese_id}    -> 课程 season_id | {cvid}         -> 专栏 cvid | {live_id}      -> 直播间 id   |"
    )
    print(Fore.LIGHTRED_EX + '在参数最后加上 "#" 表示所有视频均使用此格式, 如 ' + Fore.GREEN + '"{bvid}#"')
    print(Fore.LIGHTRED_EX + '使用 "\{" 和 "/{" 表示当作纯文本')

    exit()


def _print_banner():
    global BANNER
    print(BANNER)


def _download_video(obj: video.Video, now_file_name: str):
    """
    下载视频
    """
    global VIDEO_QUALITY, VIDEO_CODECS, AUDIO_QUALITY, DIC, RPATH
    print(Fore.GREEN + "INF: 视频 AID: ", obj.get_aid())
    pages_data = sync(obj.get_pages())
    print(Fore.GREEN + "INF: 视频分 P 数: ", len(pages_data))
    if len(pages_data) > 1:
        download_p1 = None
        while download_p1 == None:
            p = _ask_settings_download(
                Fore.BLUE
                + "NUM: 请输入想要下载的分 P 【默认全部下载(输入 all), 或者在数字两边扩上括号，获取此分 P 的信息，如 P(2)】: P"
            )
            if p == "":
                download_p1 = -1
                continue
            if p.upper() == "ALL":
                download_p1 = -1
                continue
            if (p[0] == "(" or p[0] == "（") and (p[-1] == ")" or p[-1] == "）"):
                p = (
                    p.replace("(", "")
                    .replace(")", "")
                    .replace("）", "")
                    .replace("（", "")
                )
                data = pages_data[int(p) - 1]
                print(f"INF: P{int(p)}", ": ", data["part"])
            else:
                try:
                    download_p1 = int(p)
                except:
                    pass
        if download_p1 == -1:
            print(Fore.GREEN + f"INF: 已选择所有分 P")
        else:
            print(Fore.GREEN + f"INF: 已选择 {p}, 分 p 编号 {sync(obj.get_cid(int(p) - 1))}")
    else:
        download_p1 = 0
    if download_p1 > -1:
        r = [download_p1]
    else:
        r = range(len(pages_data))
    for download_p in r:
        print(Fore.GREEN + f"INF: 正在获取下载地址(P{download_p + 1})")
        download_url = sync(obj.get_download_url(download_p))
        vinfo = sync(obj.get_info())
        if FFMPEG != "#none":
            if "dash" in download_url.keys():
                now_file_name = _require_file_type(now_file_name, ".mp4")

                data = download_url["dash"]

                videos_data = data["video"]
                video_qualities = []
                video_codecs = []
                for video_data in videos_data:
                    if not video_data["id"] in video_qualities:
                        video_qualities.append(video_data["id"])
                    for codename, description in VIDEO_CODECS.items():
                        if codename in video_data["codecs"]:
                            if not codename in video_codecs:
                                video_codecs.append(codename)
                print(Fore.GREEN + "INF: 视频清晰度：", end="|")
                for q in video_qualities:
                    print(f"  {q}: {VIDEO_QUALITY[q]}", "  |", end="")
                print()
                qnum = _ask_settings_download(Fore.BLUE + "NUM: 请选择清晰度对应数字(默认为最大清晰度): ")
                VIDEO_QUALITY_NUMBER = int(qnum) if qnum != "" else max(video_qualities)
                print(Fore.GREEN + "INF: 视频编码：", end="|")
                for c in video_codecs:
                    for codename, description in VIDEO_CODECS.items():
                        if codename in c:
                            print(f"  {codename}: {description}", "  |", end="")
                print()
                CODECS = _ask_settings_download(
                    Fore.BLUE + f'STR: 请选择视频编码对应的号码(默认为 "{video_codecs[0]}"): '
                )
                if CODECS == "":
                    CODECS = video_codecs[0]

                audios_data = data["audio"]
                audio_qualities = []
                for audio_data in audios_data:
                    if not audio_data["id"] in audio_qualities:
                        audio_qualities.append(audio_data["id"])
                print(Fore.GREEN + "INF: 音频音质：", end="|")
                for q in audio_qualities:
                    print(f"  {q}: {AUDIO_QUALITY[q]}", "  |", end="")
                print()
                qnuma = _ask_settings_download(Fore.BLUE + "NUM: 请选择音质对应数字(默认为最好音质): ")
                AUDIO_QUALITY_NUMBER = (
                    int(qnuma) if qnuma != "" else max(audio_qualities)
                )

                try:
                    print(
                        Fore.GREEN
                        + f"INF: 选择的视频清晰度 {VIDEO_QUALITY[VIDEO_QUALITY_NUMBER]} | ({VIDEO_QUALITY_NUMBER})"
                    )
                    print(
                        Fore.GREEN + f"INF: 选择的视频编码 {VIDEO_CODECS[CODECS]} | ({CODECS})"
                    )
                    print(
                        Fore.GREEN
                        + f"INF: 选择的音频音质 {AUDIO_QUALITY[AUDIO_QUALITY_NUMBER]} | ({AUDIO_QUALITY_NUMBER})"
                    )
                except KeyError:
                    print(Fore.RED + "ERR: 没有目标清晰度/编码/音质")
                    continue
                except Exception as e:
                    raise e

                print()
                download_url = sync(obj.get_download_url(download_p))
                video_url = None
                audio_url = None
                for video_data in download_url["dash"]["video"]:
                    if (
                        video_data["id"] == VIDEO_QUALITY_NUMBER
                        and CODECS in video_data["codecs"]
                    ):
                        video_url = video_data["baseUrl"]
                for audio_data in download_url["dash"]["audio"]:
                    if audio_data["id"] == AUDIO_QUALITY_NUMBER:
                        audio_url = audio_data["baseUrl"]
                if video_url == None:
                    print(Fore.RED + "ERR: 没有目标视频下载链接")
                    exit()
                if audio_url == None:
                    print(Fore.RED + "ERR: 没有目标音频下载链接")
                    exit()
                print(Fore.GREEN + f"INF: 开始下载视频(P{download_p + 1})")
                video_path = _download(
                    video_url,
                    "video_temp.m4s",
                    vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}) - 视频",
                )
                print(Fore.GREEN + f"INF: 开始下载音频(P{download_p + 1})")
                audio_path = _download(
                    audio_url,
                    "audio_temp.m4s",
                    vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}) - 音频",
                )
                print(Fore.GREEN + "INF: 下载视频完成 开始混流")
                print(Fore.RESET)
                if now_file_name == "#default":
                    RNAME = (
                        vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}).mp4"
                    )
                else:
                    RNAME = (
                        now_file_name.replace("{bvid}", obj.get_bvid())
                        .replace("{aid}", str(obj.get_aid()))
                        .replace("{owner}", vinfo["owner"]["name"])
                        .replace("{uid}", str(vinfo["owner"]["mid"]))
                        .replace("{title}", vinfo["title"])
                    )
                RPATH = os.path.join(DIC, RNAME)
                if not os.path.exists(DIC):
                    os.mkdir(DIC)
                if os.path.exists(RPATH):
                    os.remove(RPATH)
                print(Fore.MAGENTA)
                os.system(
                    f'{FFMPEG} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy "{RPATH}"'
                )
                os.remove("video_temp.m4s")
                os.remove("audio_temp.m4s")
                print(Fore.GREEN + f"INF: 混流完成(或用户手动取消)")
                PATHS.append(RPATH)
            elif "durl" in download_url.keys():
                now_file_name = _require_file_type(now_file_name, ".mp4")

                new_download_url = sync(obj.get_download_url(download_p))
                video_audio_url = new_download_url["durl"][0]["url"]
                if now_file_name == "#default":
                    RNAME = (
                        vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}).mp4"
                    )
                else:
                    RNAME = (
                        now_file_name.replace("{bvid}", obj.get_bvid())
                        .replace("{aid}", str(obj.get_aid()))
                        .replace("{owner}", vinfo["owner"]["name"])
                        .replace("{uid}", str(vinfo["owner"]["mid"]))
                        .replace("{title}", vinfo["title"])
                    )
                RPATH = os.path.join(DIC, RNAME)
                if not os.path.exists(DIC):
                    os.mkdir(DIC)
                PATH_FLV = RPATH.rstrip(".mp4") + ".flv"
                print(Fore.GREEN + f"INF: 开始下载视频(P{download_p + 1})")
                video_path = _download(
                    video_audio_url,
                    PATH_FLV,
                    vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1})",
                )
                turn_format = input(Fore.BLUE + "Y/N: 是否转换成 MP4 视频(默认转换): ")
                if turn_format.upper() == "N":
                    PATHS.append(PATH_FLV)
                else:
                    print(Fore.GREEN + "INF: 下载视频完成 正在转换格式")
                    if os.path.exists(RPATH):
                        os.remove(RPATH)
                    print(Fore.MAGENTA)
                    os.system(f'{FFMPEG} -i "{PATH_FLV}" "{RPATH}"')
                    print(Fore.GREEN + "INF: 格式转换完成(或用户手动取消)")
                    delete_flv = input(Fore.BLUE + "Y/N: 是否删除 FLV 文件(默认删除): ")
                    if delete_flv.upper() == "N":
                        PATHS.append(PATH_FLV)
                    else:
                        os.remove(PATH_FLV)
                    PATHS.append(RPATH)
        else:
            if "dash" in download_url.keys():
                now_file_name = _require_file_type(now_file_name, ".mp4")

                data = download_url["dash"]

                videos_data = data["video"]
                video_qualities = []
                video_codecs = []
                for video_data in videos_data:
                    if not video_data["id"] in video_qualities:
                        video_qualities.append(video_data["id"])
                    if not video_data["codecs"] in video_codecs:
                        video_codecs.append(video_data["codecs"])
                print(Fore.GREEN + "INF: 视频清晰度：", end="|")
                for q in video_qualities:
                    print(f"  {q}: {VIDEO_QUALITY[q]}", "  |", end="")
                print()
                qnum = _ask_settings_download(Fore.BLUE + "NUM: 请选择清晰度对应数字(默认为最大清晰度): ")
                VIDEO_QUALITY_NUMBER = int(qnum) if qnum != "" else max(video_qualities)
                print(Fore.GREEN + "INF: 视频编码：", end="|")
                for c in video_codecs:
                    for codename, description in VIDEO_CODECS.items():
                        if codename in c:
                            print(f"  {codename}: {description}", "  |", end="")
                print()
                CODECS = _ask_settings_download(
                    Fore.BLUE + 'STR: 请选择视频编码对应的号码(默认为 "hev"): '
                )
                if CODECS == "":
                    CODECS = "hev"

                audios_data = data["audio"]
                audio_qualities = []
                for audio_data in audios_data:
                    if not audio_data["id"] in audio_qualities:
                        audio_qualities.append(audio_data["id"])
                print(Fore.GREEN + "INF: 音频音质：", end="|")
                for q in audio_qualities:
                    print(f"  {q}: {AUDIO_QUALITY[q]}", "  |", end="")
                print()
                qnuma = _ask_settings_download(Fore.BLUE + "NUM: 请选择音质对应数字(默认为最好音质): ")
                AUDIO_QUALITY_NUMBER = (
                    int(qnuma) if qnuma != "" else max(audio_qualities)
                )

                print()
                try:
                    print(
                        Fore.GREEN
                        + f"INF: 选择的视频清晰度 {VIDEO_QUALITY[VIDEO_QUALITY_NUMBER]} | ({VIDEO_QUALITY_NUMBER})"
                    )
                    print(
                        Fore.GREEN + f"INF: 选择的视频编码 {VIDEO_CODECS[CODECS]} | ({CODECS})"
                    )
                    print(
                        Fore.GREEN
                        + f"INF: 选择的音频音质 {AUDIO_QUALITY[AUDIO_QUALITY_NUMBER]} | ({AUDIO_QUALITY_NUMBER})"
                    )
                except KeyError:
                    print(Fore.RED, "ERR: 没有目标清晰度/编码/音质")
                    exit()
                except Exception as e:
                    raise e

                print()
                download_url = sync(obj.get_download_url(download_p))
                video_url = None
                audio_url = None
                for video_data in download_url["dash"]["video"]:
                    if (
                        video_data["id"] == VIDEO_QUALITY_NUMBER
                        and CODECS in video_data["codecs"]
                    ):
                        video_url = video_data["baseUrl"]
                for audio_data in download_url["dash"]["audio"]:
                    if audio_data["id"] == AUDIO_QUALITY_NUMBER:
                        audio_url = audio_data["baseUrl"]
                if video_url == None:
                    print(Fore.RED + "ERR: 没有目标视频下载链接")
                    exit()
                if audio_url == None:
                    print(Fore.RED + "ERR: 没有目标音频下载链接")
                    exit()
                if now_file_name == "#default":
                    RNAME = (
                        vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}).mp4"
                    )
                else:
                    RNAME = (
                        now_file_name.replace("{bvid}", obj.get_bvid())
                        .replace("{aid}", str(obj.get_aid()))
                        .replace("{owner}", vinfo["owner"]["name"])
                        .replace("{uid}", str(vinfo["owner"]["mid"]))
                        .replace("{title}", vinfo["title"])
                    )
                if not os.path.exists(DIC):
                    os.mkdir(DIC)
                print(Fore.GREEN + f"INF: 开始下载视频(P{download_p + 1})")
                video_path = _download(
                    video_url,
                    os.path.join(DIC, "视频 - " + RNAME),
                    vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}) - 视频",
                )
                print(Fore.GREEN + f"INF: 开始下载音频(P{download_p + 1})")
                audio_path = _download(
                    audio_url,
                    os.path.join(DIC, "音频 - " + RNAME),
                    vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}) - 音频",
                )
                PATHS.append(os.path.join(DIC, "视频 - " + RNAME))
                PATHS.append(os.path.join(DIC, "音频 - " + RNAME))
            elif "durl" in download_url.keys():
                now_file_name = _require_file_type(now_file_name, ".flv")

                new_download_url = sync(obj.get_download_url(download_p))
                video_audio_url = new_download_url["durl"][0]["url"]
                if now_file_name == "#default":
                    RNAME = (
                        vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}).flv"
                    )
                else:
                    RNAME = (
                        now_file_name.replace("{bvid}", obj.get_bvid())
                        .replace("{aid}", str(obj.get_aid()))
                        .replace("{owner}", vinfo["owner"]["name"])
                        .replace("{uid}", str(vinfo["owner"]["mid"]))
                        .replace("{title}", vinfo["title"])
                    )
                RPATH = os.path.join(DIC, RNAME)
                if not os.path.exists(DIC):
                    os.mkdir(DIC)
                print(Fore.GREEN + f"INF: 开始下载视频(P{download_p + 1})")
                video_path = _download(
                    video_audio_url,
                    RPATH,
                    vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1})",
                )
        print(Fore.GREEN + "INF: ---完成分 P---")
    return download_p1


def _download_episode(obj: bangumi.Episode, now_file_name: str):
    global VIDEO_CODECS, VIDEO_QUALITY, AUDIO_QUALITY, DIC, RPATH
    print(Fore.GREEN + "INF: 视频 AID: ", obj.get_aid())
    title = sync(obj.get_bangumi().get_meta())["media"]["title"]
    vinfo = {
        "title": sync(obj.get_episode_info())['h1Title']
    }
    epcnt = 0
    for ep in sync(obj.get_episode_info())["mediaInfo"]["episodes"]:
        if ep["id"] == obj.get_epid():
            epcnt = int(ep["title"])
    vtitle = vinfo["title"]
    print(Fore.GREEN + f"INF: {title} 第{epcnt}集 {vtitle}")
    print(Fore.GREEN + f"INF: 正在获取下载地址")
    download_url = sync(obj.get_download_url())

    if FFMPEG != "#none":
        if "dash" in download_url.keys():
            now_file_name = _require_file_type(now_file_name, ".mp4")

            data = download_url["dash"]

            videos_data = data["video"]
            video_qualities = []
            video_codecs = []
            for video_data in videos_data:
                if not video_data["id"] in video_qualities:
                    video_qualities.append(video_data["id"])
                for codename, description in VIDEO_CODECS.items():
                    if codename in video_data["codecs"]:
                        if not codename in video_codecs:
                            video_codecs.append(codename)
            print(Fore.GREEN + "INF: 视频清晰度：", end="|")
            for q in video_qualities:
                print(f"  {q}: {VIDEO_QUALITY[q]}", "  |", end="")
            print()
            qnum = _ask_settings_download(Fore.BLUE + "NUM: 请选择清晰度对应数字(默认为最大清晰度): ")
            VIDEO_QUALITY_NUMBER = int(qnum) if qnum != "" else max(video_qualities)
            print(Fore.GREEN + "INF: 视频编码：", end="|")
            for c in video_codecs:
                for codename, description in VIDEO_CODECS.items():
                    if codename in c:
                        print(f"  {codename}: {description}", "  |", end="")
            print()
            CODECS = _ask_settings_download(
                Fore.BLUE
                + f'STR: 请选择视频编码对应的号码(avc|av01|hev)(默认为 "{video_codecs[0]}"): '
            )
            CODECS = CODECS.lower()
            if CODECS == "":
                CODECS = video_codecs[0]

            audios_data = data["audio"]
            audio_qualities = []
            for audio_data in audios_data:
                if not audio_data["id"] in audio_qualities:
                    audio_qualities.append(audio_data["id"])
            print(Fore.GREEN + "INF: 音频音质：", end="|")
            for q in audio_qualities:
                print(f"  {q}: {AUDIO_QUALITY[q]}", "  |", end="")
            print()
            qnuma = _ask_settings_download(Fore.BLUE + "NUM: 请选择音质对应数字(默认为最好音质): ")
            AUDIO_QUALITY_NUMBER = int(qnuma) if qnuma != "" else max(audio_qualities)

            try:
                print(
                    Fore.GREEN
                    + f"INF: 选择的视频清晰度 {VIDEO_QUALITY[VIDEO_QUALITY_NUMBER]} | ({VIDEO_QUALITY_NUMBER})"
                )
                print(Fore.GREEN + f"INF: 选择的视频编码 {VIDEO_CODECS[CODECS]} | ({CODECS})")
                print(
                    Fore.GREEN
                    + f"INF: 选择的音频音质 {AUDIO_QUALITY[AUDIO_QUALITY_NUMBER]} | ({AUDIO_QUALITY_NUMBER})"
                )
            except KeyError:
                print(Fore.RED, "ERR: 没有目标清晰度/编码/音质")
                exit()
            except Exception as e:
                raise e

            print()
            download_url = sync(obj.get_download_url())
            video_url = None
            audio_url = None
            for video_data in download_url["dash"]["video"]:
                if (
                    video_data["id"] == VIDEO_QUALITY_NUMBER
                    and CODECS in video_data["codecs"]
                ):
                    video_url = video_data["baseUrl"]
            for audio_data in download_url["dash"]["audio"]:
                if audio_data["id"] == AUDIO_QUALITY_NUMBER:
                    audio_url = audio_data["baseUrl"]
            if video_url == None:
                print(Fore.RED + "ERR: 没有目标视频下载链接")
                exit()
            if audio_url == None:
                print(Fore.RED + "ERR: 没有目标音频下载链接")
                exit()
            print(Fore.GREEN + f"INF: 开始下载视频({title} 第{epcnt}集)")
            video_path = _download(
                video_url,
                "video_temp.m4s",
                vinfo["title"] + f" - {title}(第{epcnt}集) - 视频",
            )
            print(Fore.GREEN + f"INF: 开始下载音频({title} 第{epcnt}集)")
            audio_path = _download(
                audio_url,
                "audio_temp.m4s",
                vinfo["title"] + f" - {title}(第{epcnt}集) - 音频",
            )
            print(Fore.GREEN + "INF: 下载视频完成 开始混流")
            print(Fore.RESET)
            if now_file_name == "#default":
                RNAME = vinfo["title"] + f" - 番剧 EP{obj.get_epid()}({title}).mp4"
            else:
                RNAME = (
                    now_file_name.replace("{bvid}", obj.get_bvid())
                    .replace("{aid}", str(obj.get_aid()))
                    .replace("{title}", vinfo["title"])
                    .replace("{bangumi_id}", str(obj.get_bangumi().get_season_id()))
                    .replace(
                        "{bangumi_name}",
                        sync(obj.get_bangumi().get_meta())["media"]["title"],
                    )
                    .replace("{bangumi_ep}", str(epcnt))
                    .replace("{bangumi_epid}", str(obj.get_epid()))
                )
            RPATH = os.path.join(DIC, RNAME)
            if not os.path.exists(DIC):
                os.mkdir(DIC)
            if os.path.exists(RPATH):
                os.remove(RPATH)
            print(Fore.MAGENTA)
            os.system(
                f'{FFMPEG} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy "{RPATH}"'
            )
            os.remove("video_temp.m4s")
            os.remove("audio_temp.m4s")
            print(Fore.GREEN + f"INF: 混流完成(或用户手动取消)")
            PATHS.append(RPATH)
        elif "durl" in download_url.keys():
            now_file_name = _require_file_type(now_file_name, ".mp4")

            new_download_url = sync(obj.get_download_url())
            video_audio_url = new_download_url["durl"][0]["url"]
            if now_file_name == "#default":
                RNAME = vinfo["title"] + f" - 番剧 EP{obj.get_epid()}({title}).mp4"
            else:
                RNAME = (
                    now_file_name.replace("{bvid}", obj.get_bvid())
                    .replace("{aid}", str(obj.get_aid()))
                    .replace("{title}", vinfo["title"])
                    .replace("{bangumi_id}", str(obj.get_bangumi().get_season_id()))
                    .replace(
                        "{bangumi_name}",
                        sync(obj.get_bangumi().get_meta())["media"]["title"],
                    )
                    .replace("{bangumi_ep}", str(epcnt))
                    .replace("{bangumi_epid}", str(obj.get_epid()))
                )
            RPATH = os.path.join(DIC, RNAME)
            if not os.path.exists(DIC):
                os.mkdir(DIC)
            print(Fore.GREEN + f"INF: 开始下载视频({title} 第{epcnt}集)")
            video_path = _download(
                video_audio_url,
                PATH,
                vinfo["title"] + f" - {title}(第{epcnt}集)",
            )
            PATHS.append(RPATH)
    else:
        if "dash" in download_url.keys():
            now_file_name = _require_file_type(now_file_name, ".mp4")

            data = download_url["dash"]

            videos_data = data["video"]
            video_qualities = []
            video_codecs = []
            for video_data in videos_data:
                if not video_data["id"] in video_qualities:
                    video_qualities.append(video_data["id"])
                for codename, description in VIDEO_CODECS.items():
                    if codename in video_data["codecs"]:
                        if not codename in video_codecs:
                            video_codecs.append(codename)
            print(Fore.GREEN + "INF: 视频清晰度：", end="|")
            for q in video_qualities:
                print(f"  {q}: {VIDEO_QUALITY[q]}", "  |", end="")
            print()
            qnum = _ask_settings_download(Fore.BLUE + "NUM: 请选择清晰度对应数字(默认为最大清晰度): ")
            VIDEO_QUALITY_NUMBER = int(qnum) if qnum != "" else max(video_qualities)
            print(Fore.GREEN + "INF: 视频编码：", end="|")
            for c in video_codecs:
                for codename, description in VIDEO_CODECS.items():
                    if codename in c:
                        print(f"  {codename}: {description}", "  |", end="")
            print()
            CODECS = _ask_settings_download(
                Fore.BLUE
                + f'STR: 请选择视频编码对应的号码(avc|av01|hev)(默认为 "{video_codecs[0]}"): '
            )
            CODECS = CODECS.lower()
            if CODECS == "":
                CODECS = video_codecs[0]

            audios_data = data["audio"]
            audio_qualities = []
            for audio_data in audios_data:
                if not audio_data["id"] in audio_qualities:
                    audio_qualities.append(audio_data["id"])
            print(Fore.GREEN + "INF: 音频音质：", end="|")
            for q in audio_qualities:
                print(f"  {q}: {AUDIO_QUALITY[q]}", "  |", end="")
            print()
            qnuma = _ask_settings_download(Fore.BLUE + "NUM: 请选择音质对应数字(默认为最好音质): ")
            AUDIO_QUALITY_NUMBER = int(qnuma) if qnuma != "" else max(audio_qualities)

            print()
            try:
                print(
                    Fore.GREEN
                    + f"INF: 选择的视频清晰度 {VIDEO_QUALITY[VIDEO_QUALITY_NUMBER]} | ({VIDEO_QUALITY_NUMBER})"
                )
                print(Fore.GREEN + f"INF: 选择的视频编码 {VIDEO_CODECS[CODECS]} | ({CODECS})")
                print(
                    Fore.GREEN
                    + f"INF: 选择的音频音质 {AUDIO_QUALITY[AUDIO_QUALITY_NUMBER]} | ({AUDIO_QUALITY_NUMBER})"
                )
            except KeyError:
                print(Fore.RED, "ERR: 没有目标清晰度/编码/音质")
                exit()
            except Exception as e:
                raise e

            print()
            download_url = sync(obj.get_download_url())
            video_url = None
            audio_url = None
            for video_data in download_url["dash"]["video"]:
                if (
                    video_data["id"] == VIDEO_QUALITY_NUMBER
                    and CODECS in video_data["codecs"]
                ):
                    video_url = video_data["baseUrl"]
            for audio_data in download_url["dash"]["audio"]:
                if audio_data["id"] == AUDIO_QUALITY_NUMBER:
                    audio_url = audio_data["baseUrl"]
            if video_url == None:
                print(Fore.RED + "ERR: 没有目标视频下载链接")
                exit()
            if audio_url == None:
                print(Fore.RED + "ERR: 没有目标音频下载链接")
                exit()
            if now_file_name == "#default":
                RNAME = vinfo["title"] + f" - 番剧 EP{obj.get_epid()}({title}).mp4"
            else:
                RNAME = (
                    now_file_name.replace("{bvid}", obj.get_bvid())
                    .replace("{aid}", str(obj.get_aid()))
                    .replace("{title}", vinfo["title"])
                    .replace("{bangumi_id}", str(obj.get_bangumi().get_season_id()))
                    .replace(
                        "{bangumi_name}",
                        sync(obj.get_bangumi().get_meta())["media"]["title"],
                    )
                    .replace("{bangumi_ep}", str(epcnt))
                    .replace("{bangumi_epid}", str(obj.get_epid()))
                )
            if not os.path.exists(DIC):
                os.mkdir(DIC)
            print(Fore.GREEN + f"INF: 开始下载视频({title} 第{epcnt}集)")
            video_path = _download(
                video_url,
                os.path.join(DIC, "视频 - " + RNAME),
                vinfo["title"] + f" - {obj.get_bvid()}({title} 第{epcnt}集) - 视频",
            )
            print(Fore.GREEN + f"INF: 开始下载音频({title} 第{epcnt}集)")
            audio_path = _download(
                audio_url,
                os.path.join(DIC, "音频 - " + RNAME),
                vinfo["title"] + f" - {obj.get_bvid()}({title} 第{epcnt}集) - 音频",
            )
            PATHS.append(os.path.join(DIC, "视频 - " + RNAME))
            PATHS.append(os.path.join(DIC, "音频 - " + RNAME))
        elif "durl" in download_url.keys():
            now_file_name = _require_file_type(now_file_name, ".mp4")

            new_download_url = sync(obj.get_download_url())
            video_audio_url = new_download_url["durl"][0]["url"]
            if now_file_name == "#default":
                RNAME = vinfo["title"] + f" - 番剧 EP{obj.get_epid()}({title}).mp4"
            else:
                RNAME = (
                    now_file_name.replace("{bvid}", obj.get_bvid())
                    .replace("{aid}", str(obj.get_aid()))
                    .replace("{title}", vinfo["title"])
                    .replace("{bangumi_id}", str(obj.get_bangumi().get_season_id()))
                    .replace(
                        "{bangumi_name}",
                        sync(obj.get_bangumi().get_meta())["media"]["title"],
                    )
                    .replace("{bangumi_ep}", str(epcnt))
                    .replace("{bangumi_epid}", str(obj.get_epid()))
                )
            RPATH = os.path.join(DIC, RNAME)
            if not os.path.exists(DIC):
                os.mkdir(DIC)
            print(Fore.GREEN + f"INF: 开始下载视频({title} 第{epcnt}集)")
            video_path = _download(
                video_audio_url,
                RPATH,
                vinfo["title"] + f" - {obj.get_bvid()}({title} 第{epcnt}集)",
            )


def _download_cheese_video(obj: cheese.CheeseVideo, now_file_name: str):
    global VIDEO_CODECS, VIDEO_QUALITY, AUDIO_QUALITY, DIC, RPATH
    print(Fore.GREEN + "INF: 视频 AID: ", obj.get_aid())
    vinfo = sync(obj.get_cheese().get_meta())
    vmeta = obj.get_meta()
    vtitle = vmeta["title"]
    title = vinfo["title"]
    epcnt = (
        f"第{str(obj.get_meta()['index'] - 1)}课"
        if obj.get_meta()["index"] != 1
        else "宣导片"
    )
    print(Fore.GREEN + f"INF: {title} {epcnt} {vtitle}")
    print(Fore.GREEN + f"INF: 正在获取下载地址")
    download_url = sync(obj.get_download_url())

    if FFMPEG != "#none":
        if "dash" in download_url.keys():
            now_file_name = _require_file_type(now_file_name, ".mp4")

            data = download_url["dash"]

            videos_data = data["video"]
            video_qualities = []
            video_codecs = []
            for video_data in videos_data:
                if not video_data["id"] in video_qualities:
                    video_qualities.append(video_data["id"])
                for codename, description in VIDEO_CODECS.items():
                    if codename in video_data["codecs"]:
                        if not codename in video_codecs:
                            video_codecs.append(codename)
            for q in video_qualities:
                print(f"  {q}: {VIDEO_QUALITY[q]}", "  |", end="")
            print()
            qnum = _ask_settings_download(Fore.BLUE + "NUM: 请选择清晰度对应数字(默认为最大清晰度): ")
            VIDEO_QUALITY_NUMBER = int(qnum) if qnum != "" else max(video_qualities)
            print(Fore.GREEN + "INF: 视频编码：", end="|")
            for c in video_codecs:
                for codename, description in VIDEO_CODECS.items():
                    if codename in c:
                        print(f"  {codename}: {description}", "  |", end="")
            print()
            CODECS = _ask_settings_download(
                Fore.BLUE
                + f'STR: 请选择视频编码对应的号码(avc|av01|hev)(默认为 "{video_codecs[0]}"): '
            )
            CODECS = CODECS.lower()
            if CODECS == "":
                CODECS = video_codecs[0]

            audios_data = data["audio"]
            audio_qualities = []
            for audio_data in audios_data:
                if not audio_data["id"] in audio_qualities:
                    audio_qualities.append(audio_data["id"])
            print(Fore.GREEN + "INF: 音频音质：", end="|")
            for q in audio_qualities:
                print(f"  {q}: {AUDIO_QUALITY[q]}", "  |", end="")
            print()
            qnuma = _ask_settings_download(Fore.BLUE + "NUM: 请选择音质对应数字(默认为最好音质): ")
            AUDIO_QUALITY_NUMBER = int(qnuma) if qnuma != "" else max(audio_qualities)

            try:
                print(
                    Fore.GREEN
                    + f"INF: 选择的视频清晰度 {VIDEO_QUALITY[VIDEO_QUALITY_NUMBER]} | ({VIDEO_QUALITY_NUMBER})"
                )
                print(Fore.GREEN + f"INF: 选择的视频编码 {VIDEO_CODECS[CODECS]} | ({CODECS})")
                print(
                    Fore.GREEN
                    + f"INF: 选择的音频音质 {AUDIO_QUALITY[AUDIO_QUALITY_NUMBER]} | ({AUDIO_QUALITY_NUMBER})"
                )
            except KeyError:
                print(Fore.RED, "ERR: 没有目标清晰度/编码/音质")
                exit()
            except Exception as e:
                raise e

            print()
            download_url = sync(obj.get_download_url())
            video_url = None
            audio_url = None
            for video_data in download_url["dash"]["video"]:
                if (
                    video_data["id"] == VIDEO_QUALITY_NUMBER
                    and CODECS in video_data["codecs"]
                ):
                    video_url = video_data["base_url"]
            for audio_data in download_url["dash"]["audio"]:
                if audio_data["id"] == AUDIO_QUALITY_NUMBER:
                    audio_url = audio_data["base_url"]
            if video_url == None:
                print(Fore.RED + "ERR: 没有目标视频下载链接")
                exit()
            if audio_url == None:
                print(Fore.RED + "ERR: 没有目标音频下载链接")
                exit()
            print(Fore.GREEN + f"INF: 开始下载视频({title} {epcnt})")
            video_path = _download(
                video_url,
                "video_temp.m4s",
                vmeta["title"] + f" - {title}({epcnt}) - 视频",
            )
            print(Fore.GREEN + f"INF: 开始下载音频({title} {epcnt})")
            audio_path = _download(
                audio_url,
                "audio_temp.m4s",
                vmeta["title"] + f" - {title}({epcnt}) - 音频",
            )
            print(Fore.GREEN + "INF: 下载视频完成 开始混流")
            print(Fore.RESET)
            if now_file_name == "#default":
                RNAME = vmeta["title"] + f" - 课程 EP{obj.get_epid()}({title}).mp4"
            else:
                RNAME = (
                    now_file_name.replace("{bvid}", obj.get_bvid())
                    .replace("{aid}", str(obj.get_aid()))
                    .replace("{owner}", vinfo["up_info"]["uname"])
                    .replace("{uid}", str(vinfo["up_info"]["mid"]))
                    .replace("{title}", vmeta["title"])
                    .replace("{cheese_id}", str(obj.get_bangumi().get_season_id()))
                    .replace("{cheese_name}", vinfo["title"])
                    .replace("{cheese_ep}", str(epcnt))
                    .replace("{cheese_epid}", str(obj.get_epid()))
                )
            RPATH = os.path.join(DIC, RNAME)
            if not os.path.exists(DIC):
                os.mkdir(DIC)
            if os.path.exists(RPATH):
                os.remove(RPATH)
            print(Fore.MAGENTA)
            os.system(
                f'{FFMPEG} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy "{RPATH}"'
            )
            os.remove("video_temp.m4s")
            os.remove("audio_temp.m4s")
            print(Fore.GREEN + f"INF: 混流完成(或用户手动取消)")
            PATHS.append(RPATH)
        elif "durl" in download_url.keys():
            now_file_name = _require_file_type(now_file_name, ".mp4")

            new_download_url = sync(obj.get_download_url())
            video_audio_url = new_download_url["durl"][0]["url"]
            if now_file_name == "#default":
                RNAME = vmeta["title"] + f" - 课程 EP{obj.get_epid()}({title}).mp4"
            else:
                RNAME = (
                    now_file_name.replace("{bvid}", obj.get_bvid())
                    .replace("{aid}", str(obj.get_aid()))
                    .replace("{owner}", vinfo["up_info"]["uname"])
                    .replace("{uid}", str(vinfo["up_info"]["mid"]))
                    .replace("{title}", vmeta["title"])
                    .replace("{cheese_id}", str(obj.get_bangumi().get_season_id()))
                    .replace("{cheese_name}", vinfo["title"])
                    .replace("{cheese_ep}", str(epcnt))
                    .replace("{cheese_epid}", str(obj.get_epid()))
                )
            RPATH = os.path.join(DIC, RNAME)
            if not os.path.exists(DIC):
                os.mkdir(DIC)
            print(Fore.GREEN + f"INF: 开始下载视频({title} {epcnt})")
            video_path = _download(
                video_audio_url,
                RPATH,
                vmeta["title"] + f" - {title}({epcnt})",
            )
            PATHS.append(RPATH)
    else:
        if "dash" in download_url.keys():
            now_file_name = _require_file_type(now_file_name, ".mp4")

            data = download_url["dash"]

            videos_data = data["video"]
            video_qualities = []
            video_codecs = []
            for video_data in videos_data:
                if not video_data["id"] in video_qualities:
                    video_qualities.append(video_data["id"])
                for codename, description in VIDEO_CODECS.items():
                    if codename in video_data["codecs"]:
                        if not codename in video_codecs:
                            video_codecs.append(codename)
            print(Fore.GREEN + "INF: 视频清晰度：", end="|")
            for q in video_qualities:
                print(f"  {q}: {VIDEO_QUALITY[q]}", "  |", end="")
            print()
            qnum = _ask_settings_download(Fore.BLUE + "NUM: 请选择清晰度对应数字(默认为最大清晰度): ")
            VIDEO_QUALITY_NUMBER = int(qnum) if qnum != "" else max(video_qualities)
            print(Fore.GREEN + "INF: 视频编码：", end="|")
            for c in video_codecs:
                for codename, description in VIDEO_CODECS.items():
                    if codename in c:
                        print(f"  {codename}: {description}", "  |", end="")
            print()
            CODECS = _ask_settings_download(
                Fore.BLUE
                + f'STR: 请选择视频编码对应的号码(avc|av01|hev)(默认为 "{video_codecs[0]}"): '
            )
            CODECS = CODECS.lower()
            if CODECS == "":
                CODECS = video_codecs[0]

            audios_data = data["audio"]
            audio_qualities = []
            for audio_data in audios_data:
                if not audio_data["id"] in audio_qualities:
                    audio_qualities.append(audio_data["id"])
            print(Fore.GREEN + "INF: 音频音质：", end="|")
            for q in audio_qualities:
                print(f"  {q}: {AUDIO_QUALITY[q]}", "  |", end="")
            print()
            qnuma = _ask_settings_download(Fore.BLUE + "NUM: 请选择音质对应数字(默认为最好音质): ")
            AUDIO_QUALITY_NUMBER = int(qnuma) if qnuma != "" else max(audio_qualities)

            print()
            try:
                print(
                    Fore.GREEN
                    + f"INF: 选择的视频清晰度 {VIDEO_QUALITY[VIDEO_QUALITY_NUMBER]} | ({VIDEO_QUALITY_NUMBER})"
                )
                print(Fore.GREEN + f"INF: 选择的视频编码 {VIDEO_CODECS[CODECS]} | ({CODECS})")
                print(
                    Fore.GREEN
                    + f"INF: 选择的音频音质 {AUDIO_QUALITY[AUDIO_QUALITY_NUMBER]} | ({AUDIO_QUALITY_NUMBER})"
                )
            except KeyError:
                print(Fore.RED, "ERR: 没有目标清晰度/编码/音质")
                exit()
            except Exception as e:
                raise e

            print()
            download_url = sync(obj.get_download_url())
            video_url = None
            audio_url = None
            for video_data in download_url["dash"]["video"]:
                if (
                    video_data["id"] == VIDEO_QUALITY_NUMBER
                    and CODECS in video_data["codecs"]
                ):
                    video_url = video_data["base_url"]
            for audio_data in download_url["dash"]["audio"]:
                if audio_data["id"] == AUDIO_QUALITY_NUMBER:
                    audio_url = audio_data["base_url"]
            if video_url == None:
                print(Fore.RED + "ERR: 没有目标视频下载链接")
                exit()
            if audio_url == None:
                print(Fore.RED + "ERR: 没有目标音频下载链接")
                exit()
            if now_file_name == "#default":
                RNAME = vmeta["title"] + f" - 课程 EP{obj.get_epid()}({title}).mp4"
            else:
                RNAME = (
                    now_file_name.replace("{bvid}", obj.get_bvid())
                    .replace("{aid}", str(obj.get_aid()))
                    .replace("{owner}", vinfo["up_info"]["uname"])
                    .replace("{uid}", str(vinfo["up_info"]["mid"]))
                    .replace("{title}", vmeta["title"])
                    .replace("{cheese_id}", str(obj.get_bangumi().get_season_id()))
                    .replace("{cheese_name}", vinfo["title"])
                    .replace("{cheese_ep}", str(epcnt))
                    .replace("{cheese_epid}", str(obj.get_epid()))
                )
            if not os.path.exists(DIC):
                os.mkdir(DIC)
            print(Fore.GREEN + f"INF: 开始下载视频({title} {epcnt})")
            video_path = _download(
                video_url,
                os.path.join(DIC, "视频 - " + RNAME),
                vinfo["title"] + f" - {obj.get_bvid()}({title} {epcnt}) - 视频",
            )
            print(Fore.GREEN + f"INF: 开始下载音频({title} {epcnt})")
            audio_path = _download(
                audio_url,
                os.path.join(DIC, "音频 - " + RNAME),
                vinfo["title"] + f" - {obj.get_bvid()}({title} {epcnt}) - 音频",
            )
            PATHS.append(os.path.join(DIC, "视频 - " + RNAME))
            PATHS.append(os.path.join(DIC, "音频 - " + RNAME))
        elif "durl" in download_url.keys():
            now_file_name = _require_file_type(now_file_name, ".mp4")

            new_download_url = sync(obj.get_download_url())
            video_audio_url = new_download_url["durl"][0]["url"]
            if now_file_name == "#default":
                RNAME = vmeta["title"] + f" - 课程 EP{obj.get_epid()}({title}).mp4"
            else:
                RNAME = (
                    now_file_name.replace("{bvid}", obj.get_bvid())
                    .replace("{aid}", str(obj.get_aid()))
                    .replace("{owner}", vinfo["up_info"]["uname"])
                    .replace("{uid}", str(vinfo["up_info"]["mid"]))
                    .replace("{title}", vmeta["title"])
                    .replace("{cheese_id}", str(obj.get_bangumi().get_season_id()))
                    .replace("{cheese_name}", vinfo["title"])
                    .replace("{cheese_ep}", str(epcnt))
                    .replace("{cheese_epid}", str(obj.get_epid()))
                )
            RPATH = os.path.join(DIC, RNAME)
            if not os.path.exists(DIC):
                os.mkdir(DIC)
            print(Fore.GREEN + f"INF: 开始下载视频({title} {epcnt})")
            video_path = _download(
                video_audio_url,
                RPATH,
                vmeta["title"] + f" - {title}({epcnt})",
            )
            PATHS.append(RPATH)


def _download_danmakus(
    obj: Union[video.Video, bangumi.Episode, cheese.CheeseVideo],
    now_file_name: str,
    download_p1: int = -1,
):
    global PATHS, DOWNLOAD_DANMAKUS
    if DOWNLOAD_DANMAKUS == "ask":
        download_danmakus = input(Fore.BLUE + "Y/N: 此资源支持下载弹幕, 是否下载: ")
    else:
        if DOWNLOAD_DANMAKUS.upper() == "FALSE":
            download_danmakus = "N"
        else:
            download_danmakus = "Y"
    if download_danmakus.upper() == "N":
        return
    else:
        if isinstance(obj, bangumi.Episode):
            title = sync(obj.get_bangumi().get_meta())["media"]["title"]
            epcnt = 0
            vinfo = {
                "title": sync(obj.get_episode_info())['h1Title']
            }
            for ep in sync(obj.get_episode_info())["mediaInfo"]["episodes"]:
                if ep["id"] == obj.get_epid():
                    epcnt = int(ep["title"])
            if now_file_name == "#default":
                RNAME = vinfo["title"] + f" - 番剧 EP{obj.get_epid()}({title}).ass"
            else:
                RNAME = (
                    now_file_name.replace("{bvid}", obj.get_bvid())
                    .replace("{aid}", str(obj.get_aid()))
                    .replace("{title}", vinfo["title"])
                    .replace("{bangumi_id}", str(obj.get_bangumi().get_season_id()))
                    .replace(
                        "{bangumi_name}",
                        sync(obj.get_bangumi().get_meta())["media"]["title"],
                    )
                    .replace("{bangumi_ep}", str(epcnt))
                    .replace("{bangumi_epid}", str(obj.get_epid()))
                )
            now_name = _require_ass_for_danmakus(RNAME)
            RPATH = os.path.join(DIC, now_name)
            if not os.path.exists(DIC):
                os.mkdir(DIC)
            if os.path.exists(RPATH):
                os.remove(RPATH)
            print(Fore.GREEN + f"INF: 开始下载弹幕")
            sync(ass.make_ass_file_danmakus_xml(obj, out=RPATH))
            print(Fore.GREEN + f"INF: 下载弹幕完成")
            PATHS.append(RPATH)
        elif isinstance(obj, video.Video):
            pages_data = sync(obj.get_pages())
            if download_p1 > -1:
                r = [download_p1]
            else:
                r = range(len(pages_data))
            vinfo = sync(obj.get_info())
            for download_p in r:
                if now_file_name == "#default":
                    RNAME = (
                        vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}).ass"
                    )
                else:
                    RNAME = (
                        now_file_name.replace("{bvid}", obj.get_bvid())
                        .replace("{aid}", str(obj.get_aid()))
                        .replace("{owner}", vinfo["owner"]["name"])
                        .replace("{uid}", str(vinfo["owner"]["mid"]))
                        .replace("{title}", vinfo["title"])
                    )
                now_name = _require_ass_for_danmakus(RNAME)
                RPATH = os.path.join(DIC, now_name)
                if not os.path.exists(DIC):
                    os.mkdir(DIC)
                if os.path.exists(RPATH):
                    os.remove(RPATH)
                print(Fore.GREEN + f"INF: 开始下载弹幕(P{download_p + 1})")
                sync(ass.make_ass_file_danmakus_xml(obj, download_p, out=RPATH))
                print(Fore.GREEN + f"INF: 下载弹幕完成")
                PATHS.append(RPATH)
        elif isinstance(obj, cheese.CheeseVideo):
            vinfo = sync(obj.get_cheese().get_meta())
            vmeta = obj.get_meta()
            title = vinfo["title"]
            if now_file_name == "#default":
                RNAME = vmeta["title"] + f" - 课程 EP{obj.get_epid()}({title}).ass"
            else:
                RNAME = (
                    now_file_name.replace("{bvid}", obj.get_bvid())
                    .replace("{aid}", str(obj.get_aid()))
                    .replace("{owner}", vinfo["up_info"]["uname"])
                    .replace("{uid}", str(vinfo["up_info"]["mid"]))
                    .replace("{title}", vmeta["title"])
                    .replace("{cheese_id}", str(obj.get_bangumi().get_season_id()))
                    .replace("{cheese_name}", vinfo["title"])
                    .replace("{cheese_ep}", str(epcnt))
                    .replace("{cheese_epid}", str(obj.get_epid()))
                )
            now_name = _require_ass_for_danmakus(RNAME)
            RPATH = os.path.join(DIC, now_name)
            if not os.path.exists(DIC):
                os.mkdir(DIC)
            if os.path.exists(RPATH):
                os.remove(RPATH)
            print(Fore.GREEN + f"INF: 开始下载弹幕")
            sync(ass.make_ass_file_danmakus_xml(obj, out=RPATH))
            print(Fore.GREEN + f"INF: 下载弹幕完成")
            PATHS.append(RPATH)


def _download_bangumi(obj: bangumi.Bangumi, now_file_name: str):
    def __download_one_episode(obj: bangumi.Episode, now_file_name: str):
        if not DOWNLOAD_DANMAKUS.upper() == "ONLY":
            _download_episode(obj, now_file_name)
        _download_danmakus(obj, now_file_name)
    ep_list = sync(obj.get_episode_list())["main_section"]["episodes"]
    print(Fore.GREEN + f"INF: 番剧 media_id {obj.get_media_id()}")
    print(Fore.GREEN + f"INF: 番剧共 {len(ep_list)} 集")
    print()
    for ep in ep_list:
        epid = ep["id"]
        __download_one_episode(bangumi.Episode(epid, obj.credential), now_file_name)
        print()


def _download_cheese(obj: cheese.CheeseList, now_file_name: str):
    def __download_one_cheese(obj: cheese.CheeseVideo, now_file_name: str):
        if not DOWNLOAD_DANMAKUS.upper() == "ONLY":
            _download_cheese_video(obj, now_file_name)
        _download_danmakus(obj, now_file_name)
    print(Fore.GREEN + f"INF: 课程 season_id {obj.get_season_id()}")
    course_cnt = sync(obj.get_meta())["ep_count"]
    print(Fore.GREEN + f"INF: 课程共 {course_cnt} 课时")
    cheeses: List[cheese.CheeseVideo]
    cheeses = sync(obj.get_list())
    for c in cheeses:
        try:
            __download_one_cheese(c, now_file_name)
        except Exception as e:
            print(Fore.RED + "ERR: " + str(e))
        print()


def _parse_args():
    global _require_file_type, DIC, PATH, CREDENTIAL, FFMPEG, PROXY, DEFAULT_SETTINGS, DOWNLOAD_DANMAKUS, DOWNLOAD_LIST

    if "--default-settings" in sys.argv:
        DEFAULT_SETTINGS = True
        print(Fore.GREEN + "INF: 识别到下载时全部使用默认设置(适用于视频、专栏)")

    if "--download-list" in sys.argv:
        DOWNLOAD_LIST = True
        print(Fore.GREEN + "INF: 已开启下载全部列表的模式")

    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--danmakus-settings":
            DOWNLOAD_DANMAKUS = sys.argv[i + 1]
            print(Fore.GREEN + "INF: 识别到弹幕下载设置为 " + DOWNLOAD_DANMAKUS)

    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--out" or arg == "-o":
            PATH = sys.argv[i + 1]
            print(Fore.GREEN + "INF: 识别到文件名为 ", PATH)
            if PATH[-1] == "#":
                print(Fore.GREEN + "INF: 此为全局文件名设置")
        if arg == "--dic" or arg == "-d":
            DIC = sys.argv[i + 1]
            print(Fore.GREEN + "INF: 识别到文件输出地址为 ", DIC)
            if DIC == "#default":
                DIC = "."

    CREDENTIAL = Credential()
    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--sessdata":
            CREDENTIAL.sessdata = sys.argv[i + 1]
            print(Fore.GREEN + "INF: 识别到 SESSDATA = ", CREDENTIAL.sessdata)

    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--ffmpeg":
            FFMPEG = sys.argv[i + 1]
            print(Fore.GREEN + "INF: 识别到 FFmpeg 地址为 ", FFMPEG)
            if FFMPEG == "#none":
                print(Fore.YELLOW + "WRN: 用户选择不使用 FFmpeg, 会导致混流、转换格式无法自动执行")

    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--proxy":
            p = sys.argv[i + 1]
            print(Fore.GREEN + "INF: 查找到代理：", p)
            try:
                httpx.get("https://www.baidu.com", proxies={"all://": p}, timeout=1)
            except Exception:
                print(Fore.RED, "ERR: 无法成功连接代理。")
                print()
            else:
                PROXY = p
                print(Fore.GREEN + "INF: 使用代理：", PROXY)
                settings.proxy = PROXY

    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--disable-filetype-check":
            print(Fore.GREEN + "INF: 识别到 disable-filetype-check, 已禁用文件后缀自动检查")
            _require_file_type = lambda x, y: x


def _main():
    global PROXY, FFMPEG, PATH, PATHS, DIC, _require_file_type, CREDENTIAL, DOWNLOAD_DANMAKUS, DOWNLOAD_LIST
    # TODO: INFO
    _print_banner()
    print(Fore.LIGHTMAGENTA_EX + "BiliDown: 哔哩哔哩命令行下载器")
    print(Fore.LIGHTMAGENTA_EX + "Powered by Bilibili API")
    print(Fore.LIGHTMAGENTA_EX + "By Nemo2011<yimoxia@outlook.com>")

    if "-h" in sys.argv:
        _help()

    print("使用 -h 获取帮助。")

    if len(sys.argv) == 1:
        print(Fore.YELLOW + "WRN: 请提供参数")
        exit()

    print()

    # TODO: ARGS
    _parse_args()

    # TODO: START
    print(Fore.CYAN + "----------开始下载----------")
    print()

    links = sys.argv[1].split("|")
    cnt = 0
    for link in links:
        # TODO: PARSE
        print(Fore.GREEN + "INF: 链接 -> " + Fore.RED + f"{link}")
        print(Fore.GREEN + "INF: 正在获取链接信息")
        try:
            download_object = sync(parse_link(link, credential=CREDENTIAL))
        except Exception as e:
            raise e
        if download_object == -1:
            print(Fore.RED + "ERR: 无法获取链接信息。请检查是否有拼写错误。", Style.RESET_ALL)
            print(Fore.CYAN + "----------完成下载----------")
            cnt += 1
            continue
        obj = download_object[0]
        resource_type = download_object[1]
        if resource_type == ResourceType.VIDEO:
            print(Fore.GREEN + "INF: 解析结果：视频")
        elif resource_type == ResourceType.AUDIO:
            print(Fore.GREEN + "INF: 解析结果：音频")
        elif resource_type == ResourceType.EPISODE:
            print(Fore.GREEN + "INF: 解析结果：番剧剧集")
        elif resource_type == ResourceType.CHEESE_VIDEO:
            print(Fore.GREEN + "INF: 解析结果：课程视频")
        elif resource_type == ResourceType.ARTICLE:
            print(Fore.GREEN + "INF: 解析结果：专栏")
        elif resource_type == ResourceType.LIVE:
            print(Fore.GREEN + "INF: 解析结果：直播间")
        elif resource_type == ResourceType.BANGUMI:
            print(Fore.GREEN + "INF: 解析结果: 番剧")
        elif resource_type == ResourceType.AUDIO_LIST:
            print(Fore.GREEN + "INF: 解析结果: 歌单")
        else:
            print(Fore.YELLOW, "WRN: 资源不支持下载。", Style.RESET_ALL)
            continue
        print()

        # TODO: DOWNLOAD
        try:
            now_file_name = PATH.split("|")[cnt]
        except IndexError:
            now_file_name = "#default"
        if PATH[-1] == "#":
            now_file_name = PATH[:-1]
        if now_file_name == "":
            now_file_name = "#default"
        try:
            if resource_type == ResourceType.VIDEO:
                obj: video.Video
                if not DOWNLOAD_DANMAKUS.upper() == "ONLY":
                    video_download_p = _download_video(obj, now_file_name)
                else:
                    video_download_p = -1
                _download_danmakus(obj, now_file_name, video_download_p)
            elif resource_type == ResourceType.EPISODE:
                obj: bangumi.Episode
                if DOWNLOAD_LIST:
                    epcnt = 0
                    for ep in sync(obj.get_episode_info())["mediaInfo"]["episodes"]:
                        if ep["id"] == obj.get_epid():
                            epcnt = int(ep["title"])
                    if epcnt == 0:
                        if not DOWNLOAD_DANMAKUS.upper() == "ONLY":
                            _download_episode(obj, now_file_name)
                        _download_danmakus(obj, now_file_name)
                    print(Fore.CYAN + "----------完成下载----------")
                    _download_bangumi(obj.get_bangumi(), now_file_name)
                else:
                    if not DOWNLOAD_DANMAKUS.upper() == "ONLY":
                        _download_episode(obj, now_file_name)
                    _download_danmakus(obj, now_file_name)
            elif resource_type == ResourceType.CHEESE_VIDEO:
                obj: cheese.CheeseVideo
                if not DOWNLOAD_LIST:
                    if not DOWNLOAD_DANMAKUS.upper() == "ONLY":
                        _download_cheese_video(obj, now_file_name)
                    _download_danmakus(obj, now_file_name)
                else:
                    _download_cheese(obj.get_cheese(), now_file_name)
            elif resource_type == ResourceType.BANGUMI:
                obj: bangumi.Bangumi
                _download_bangumi(obj, now_file_name)
            else:
                print(Fore.YELLOW, "WRN: 资源不支持下载。", Style.RESET_ALL)
                continue
        except Exception as e:
            print(Fore.RED + "ERR: " + str(e))
            print(Fore.CYAN + "----------完成下载----------")
            cnt += 1
            continue

        print(Fore.CYAN + "----------完成下载----------")
        print()
        cnt += 1
    print()
    print(Fore.GREEN + "BiliDown 下载完成")
    for p in PATHS:
        print(Fore.RESET + p)


def main():
    if sys.version_info < (3, 8, 0):
        print(Fore.RED + "不支持的版本 BiliDown 需要 Python 版本大于 3.8.0")
        exit()
    if "--debug" in sys.argv:
        print(Fore.CYAN + Back.BLACK + "DEBUG MODE" + Style.RESET_ALL)
        return _main()
    try:
        _main()
    except Exception as e:
        print(Fore.RED + "ERR: " + str(e))
        print(Fore.RED + "详细信息可以使用 --debug 查询")


if __name__ == "__main__":
    main()
