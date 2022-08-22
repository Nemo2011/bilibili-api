from calendar import c
from bilibili_api import *
import sys
import httpx
import signal

def _exit(*args, **kwargs):
    exit()

signal.signal(signal.SIGINT, _exit)

PROXY = None

def main():
    try:
        _main()
    except Exception as e:
        print("ERR: ", e)

def _main():
    # TODO: INFO
    print("BiliDown: 哔哩哔哩命令行下载器")
    print("Powered by Bilibili API")

    if "-h" in sys.argv:
        print("使用方法：python -m bilidown \"https://bilibili.com/.../\" --proxy \"https://user:password@your-proxy.com\"")
        exit()

    print("使用 -h 获取帮助。")

    if len(sys.argv) == 1:
        print("请提供参数。")
        exit()

    print()

    # TODO: PROXY
    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--proxy":
            p = sys.argv[i + 1]
            print("INF: 查找到代理：", p)
            try:
                httpx.get("https://www.baidu.com", proxies={"all://": p}, timeout=1)
            except Exception:
                print("ERR: 无法成功连接代理。")
                print()
            else:
                PROXY = p
                print("INF: 使用代理：", PROXY)
                settings.proxy = PROXY
                print()

    # TODO: PARSE
    print("INF: 正在获取链接信息")
    try:
        download_object = sync(parse_link(sys.argv[1]))
    except Exception as e:
        print("ERR", e)
        exit()
    if download_object == -1:
        print("ERR: 无法获取链接信息。请检查是否有拼写错误。")
        exit()
    obj = download_object[0]
    resource_type = download_object[1]
    if resource_type == ResourceType.VIDEO:
        print("INF: 解析结果：视频")
    elif resource_type == ResourceType.AUDIO:
        print("INF: 解析结果：音频")
    elif resource_type == ResourceType.EPISODE:
        print("INF: 解析结果：番剧剧集")
    elif resource_type == ResourceType.CHEESE_VIDEO:
        print("INF: 解析结果：课程视频")
    elif resource_type == ResourceType.ARTICLE:
        print("INF: 解析结果：专栏")
    elif resource_type == ResourceType.USER:
        print("INF: 解析结果：用户")
    elif resource_type == ResourceType.CHANNEL_SERIES:
        print("INF: 解析结果：合集与列表")
    elif resource_type == ResourceType.BANGUMI:
        print("INF: 解析结果：番剧")
    elif resource_type == ResourceType.AUDIO_LIST:
        print("INF: 解析结果：歌单")
    elif resource_type == ResourceType.FAVORITE_LIST:
        print("INF: 解析结果：收藏夹")
    elif resource_type == ResourceType.LIVE:
        print("INF: 解析结果：直播间")
    else:
        print("资源不支持下载。")
    print()

    # TODO: DOWNLOAD
    if resource_type == ResourceType.VIDEO:
        obj: video.Video
        print("INF: 视频 AID: ", obj.get_aid())
        pages_data = sync(obj.get_pages())
        print("INF: 视频分 P 数: ", len(pages_data))
        if len(pages_data) > 1:
            download_p = None
            while download_p == None:
                p = input("NUM: 请输入想要下载的分 P 【或者在数字两边扩上括号，获取此分 P 的信息，如 P(2)】: P")
                if (p[0] == "(" or p[0] == "（") and (p[-1] == ")" or p[-1] == "）"):
                    p = p.replace("(", "").replace(")", "").replace("）", "").replace("（", "")
                    data = pages_data[int(p) - 1]
                    print(f"INF: P{int(p)}", ": ", data["part"])
                else:
                    download_p = int(p)
            print(f"INF: 已选择 {p}, 分 p 编号 {sync(obj.get_cid(int(p) - 1))}")

if __name__ == "__main__":
    main()
