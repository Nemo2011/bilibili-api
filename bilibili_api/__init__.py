from . import video, user, dynamic, bangumi, live, article, exceptions, tools, audio
from .utils import aid2bvid, bvid2aid, upload_image, Verify, Danmaku, Color, get_channel_info_by_name, \
    get_channel_info_by_tid, request_settings


META_VERSION = "2.0.0-beta.1"


def get_setu():
    raise utils.exceptions.BilibiliApiException("404 NOT FOUND")


def do_not_stop():
    t = """\033[1;31mₘₙⁿ
▏n
█▏　､⺍
█▏ ⺰ʷʷｨ
█◣▄██◣
◥██████▋
　◥████ █▎
　　███▉ █▎
　◢████◣⌠ₘ℩
　　██◥█◣\≫
　　██　◥█◣
　　█▉　　█▊
　　█▊　　█▊
　　█▊　　█▋
　　 █▏　　█▙
　　 █"""
    print(t)
    print("\033[1;33m不要停下来啊！")