from . import video, user, dynamic, bangumi, live, article, exceptions, tools, audio, channel, utils
from .utils import aid2bvid, bvid2aid, upload_image, Verify, Danmaku, Color, request_settings
from .common import get_vote_info

META = {
    "version": "2.0.3"
}


def check_update():
    """
    检查更新
    :return:
    """
    from pkg_resources import parse_version
    from requests import get, RequestException
    now_ver = parse_version(META["version"])
    print("正在检查更新中，请稍等...")
    try:
        resp = get("https://api.github.com/repos/Passkou/bilibili_api/releases")
        resp.raise_for_status()
    except RequestException as e:
        print("\033[1;31m检查更新失败：", str(e))
    else:
        data = resp.json()
        if len(data) == 0:
            print("当前版本：", META["version"])
            print("远程服务器无Releases，无法检查更新")
        else:
            # 最新版本
            latest = parse_version(data[0]["tag_name"])
            if now_ver < latest:
                # 有更新
                print("检查到可用的更新！")
                print("当前版本：", META["version"])
                print("最新版本：", data[0]["tag_name"])
                print("更新内容：")
                print(data[0]["body"])
                print(data[0]["html_url"])
                print("使用命令：\npip install --upgrade bilibili_api==%s" % str(latest))
                if latest.is_prerelease:
                    print("\033[1;33m请注意，当前版本为预发布版本，可能存在不稳定的情况，请慎重升级。")
                else:
                    print("\033[1;32m当前版本为稳定版，建议升级至最新版本。")
            else:
                print("当前版本已是最新")


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