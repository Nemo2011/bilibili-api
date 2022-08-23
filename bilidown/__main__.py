import os
from bilibili_api import *
from bilibili_api.exceptions import *
import sys
import httpx
import requests
import signal
from colorama import Fore, Style, init

PROXY = None
PATH = "#default"
FFMPEG = "ffmpeg"
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


def _exit(*args, **kwargs):
    print(Style.RESET_ALL)
    exit()


signal.signal(signal.SIGINT, _exit)

init(autoreset=True)


def _download(url: str, out: str, description: str):
    global PROXY
    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"},
        proxies={"all://": PROXY},
    )
    resp.raise_for_status()

    if os.path.exists(out):
        os.remove(out)

    print(Fore.BLUE + f"DWN: 开始下载 {description} 至 {out}")

    
    cnt = 0
    print(Fore.BLUE + "DWN: " + str(cnt) + "\r", end="")

    with open(out, "wb") as f:
        for chunk in resp.iter_content(1024):
            cnt += 1
            print(Fore.BLUE + "DWN: ", cnt, "\r", end="")
            f.write(chunk)
    print()
    print(Fore.BLUE + "DWN: 完成下载")
    return out


def main():
    try:
        _main()
    except Exception as e:
        print(Fore.RED, "ERR: ", e)


def _main():
    global PROXY, FFMPEG, PATH
    # TODO: INFO
    print("BiliDown: 哔哩哔哩命令行下载器")
    print("Powered by Bilibili API")

    if "-h" in sys.argv:
        print('使用方法: python -m bilidown "https://bilibili.com/.../"')
        print(
            '参数:   --proxy    代理                                          "https://user:password@your-proxy.com"'
        )
        print('参数:   --out      下载地址(默认为 "#default")                   "~/Desktop/a.mp4"')
        print('参数:   --ffmpeg   ffmpeg 地址(如果没有 ffmpeg 可以使用 "none")   "ffmpeg"')
        print("参数:   -h         帮助")
        exit()

    print("使用 -h 获取帮助。")

    if len(sys.argv) == 1:
        print(Fore.YELLOW, "WRN: 请提供参数。", Style.RESET_ALL)
        exit()

    # TODO: OUT
    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--out":
            OUT = sys.argv[i + 1]
            print(Fore.GREEN + "INF: 识别到文件输出地址为 ", OUT)

    # TODO: FFMPEG
    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--ffmpeg":
            FFMPEG = sys.argv[i + 1]
            print(Fore.GREEN + "INF: 识别到 FFmpeg 地址为 ", FFMPEG)
            if FFMPEG == "#none":
                print(Fore.YELLOW + "WRN: 用户选择不使用 FFmpeg, 会导致混流、转换格式无法自动执行")

    # TODO: PROXY
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
                print()

    # TODO: PARSE
    print(Fore.GREEN + "INF: 正在获取链接信息")
    try:
        download_object = sync(parse_link(sys.argv[1]))
    except Exception as e:
        print(Fore.RED + "ERR", e, Style.RESET_ALL)
        exit()
    if download_object == -1:
        print(Fore.RED + "ERR: 无法获取链接信息。请检查是否有拼写错误。", Style.RESET_ALL)
        exit()
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
    else:
        print(Fore.YELLOW, "WRN: 资源不支持下载。", Style.RESET_ALL)
        exit()
    print()

    # TODO: DOWNLOAD
    if resource_type == ResourceType.VIDEO:
        obj: video.Video
        print(Fore.GREEN + "INF: 视频 AID: ", obj.get_aid())
        pages_data = sync(obj.get_pages())
        print(Fore.GREEN + "INF: 视频分 P 数: ", len(pages_data))
        print()
        if len(pages_data) > 1:
            download_p = None
            while download_p == None:
                p = input(
                    Fore.BLUE + "NUM: 请输入想要下载的分 P 【或者在数字两边扩上括号，获取此分 P 的信息，如 P(2)】: P"
                )
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
                    download_p = int(p)
            print(Fore.GREEN + f"INF: 已选择 {p}, 分 p 编号 {sync(obj.get_cid(int(p) - 1))}")
        else:
            download_p = 0
        print(Fore.GREEN + "INF: 正在获取下载地址")
        download_url = sync(obj.get_download_url(download_p))
        vinfo = sync(obj.get_info())
        if FFMPEG != "#none":
            if "dash" in download_url.keys():
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
                qnum = input(Fore.BLUE + "NUM: 请选择清晰度对应数字(默认为最大清晰度): ")
                VIDEO_QUALITY_NUMBER = int(qnum) if qnum != "" else max(video_qualities)
                print(Fore.GREEN + "INF: 视频编码：", end="|")
                for c in video_codecs:
                    for codename, description in VIDEO_CODECS.items():
                        if codename in c:
                            print(f"  {codename}: {description}", "  |", end="")
                print()
                CODECS = input(Fore.BLUE + 'STR: 请选择视频编码对应的号码(默认为 "hev"): ')
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
                qnuma = input(Fore.BLUE + "NUM: 请选择音质对应数字(默认为最好音质): ")
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
                download_url = sync(obj.get_download_url(download_p))
                video_url = None
                audio_url = None
                for video_data in download_url["dash"]["video"]:
                    if video_data["id"] == VIDEO_QUALITY_NUMBER and CODECS in video_data["codecs"]:
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
                print(Fore.GREEN + "INF: 开始下载视频")
                video_path = _download(video_url, "video_temp.m4s", vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}) - 视频")
                print(Fore.GREEN + "INF: 开始下载音频")
                audio_path = _download(audio_url, "audio_temp.m4s", vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}) - 音频")
                print(Fore.GREEN + "INF: 下载视频完成 开始混流")
                print(Fore.RESET)
                if PATH == "#default":
                    PATH = vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}).mp4"
                os.system(f'{FFMPEG} -i video_temp.m4s -i audio_temp.m4s -vcodec copy -acodec copy "{PATH}"')
                os.remove("video_temp.m4s")
                os.remove("audio_temp.m4s")
                print(Fore.GREEN + f"INF: 混流完成(或用户手动取)")
            elif "durl" in download_url.keys():
                new_download_url = sync(obj.get_download_url(download_p))
                video_audio_url = new_download_url["durl"][0]["url"]
                if PATH == "#default":
                    PATH = vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}).mp4"
                PATH_FLV = PATH.rstrip(".mp4")
                print(Fore.GREEN + "INF: 开始下载视频")
                video_path = _download(video_audio_url, PATH_FLV, vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1})")
                turn_format = input(Fore.BLUE + "Y/N: 是否转换成 MP4 视频(默认转换): ")
                if turn_format.upper() == "N":
                    pass
                else:
                    print(Fore.GREEN + "INF: 下载视频完成 正在转换格式")
                    os.system(f'{FFMPEG} -i "{PATH_FLV}" "{PATH}"')
                    print(Fore.GREEN + "INF: 格式转换完成(或用户手动取)")
                    delete_flv = input(Fore.BLUE + "Y/N: 是否删除 FLV 文件(默认删除): ")
                    if delete_flv.upper() == "N":
                        pass
                    else:
                        os.remove(PATH_FLV)
        else:
            if "dash" in download_url.keys():
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
                qnum = input(Fore.BLUE + "NUM: 请选择清晰度对应数字(默认为最大清晰度): ")
                VIDEO_QUALITY_NUMBER = int(qnum) if qnum != "" else max(video_qualities)
                print(Fore.GREEN + "INF: 视频编码：", end="|")
                for c in video_codecs:
                    for codename, description in VIDEO_CODECS.items():
                        if codename in c:
                            print(f"  {codename}: {description}", "  |", end="")
                print()
                CODECS = input(Fore.BLUE + 'STR: 请选择视频编码对应的号码(默认为 "hev"): ')
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
                qnuma = input(Fore.BLUE + "NUM: 请选择音质对应数字(默认为最好音质): ")
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
                download_url = sync(obj.get_download_url(download_p))
                video_url = None
                audio_url = None
                for video_data in download_url["dash"]["video"]:
                    if video_data["id"] == VIDEO_QUALITY_NUMBER and CODECS in video_data["codecs"]:
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
                if PATH == "#default":
                    PATH = vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}).mp4"
                print(Fore.GREEN + "INF: 开始下载视频")
                video_path = _download(video_url, "视频 - " + PATH, vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}) - 视频")
                print(Fore.GREEN + "INF: 开始下载音频")
                audio_path = _download(audio_url, "音频 - " + PATH, vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}) - 音频")
                print(Fore.GREEN + "INF: BiliDown 下载完成")
                print(Fore.GREEN + "视频地址：(" + "视频 - " + PATH + ")")
                print(Fore.GREEN + "音频地址：(" + "音频 - " + PATH + ")")
                exit()
            elif "durl" in download_url.keys():
                new_download_url = sync(obj.get_download_url(download_p))
                video_audio_url = new_download_url["durl"][0]["url"]
                if PATH == "#default":
                    PATH = vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1}).mp4"
                PATH_FLV = PATH.rstrip(".mp4") + ".flv"
                print(Fore.GREEN + "INF: 开始下载视频")
                video_path = _download(video_audio_url, PATH_FLV, vinfo["title"] + f" - {obj.get_bvid()}(P{download_p + 1})")
                print(Fore.GREEN + "INF: BiliDown 下载完成")
                print(Fore.GREEN + f"({PATH_FLV})")
                exit()
    else:
        pass
    print(Fore.GREEN + "INF: BiliDown 下载完成")
    print(Fore.GREEN + f"({PATH})")

if __name__ == "__main__":
    _main()
