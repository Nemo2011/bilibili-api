"""
bilibili_api

哔哩哔哩的各种 API 调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。

 (默认已导入所有子模块，例如 `bilibili_api.video`, `bilibili_api.user`)
"""

from .utils.sync import sync
from .utils.picture import Picture
from .utils.short import get_real_url
from .utils.parse_link import ResourceType, parse_link
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.danmaku import DmMode, Danmaku, DmFontSize, SpecialDanmaku
from .utils.network import (
    # settings
    request_settings,
    # log
    request_log,
    # session
    BiliAPIResponse,
    BiliWsMsgType,
    BiliAPIFile,
    BiliAPIClient,
    register_client,
    unregister_client,
    select_client,
    get_selected_client,
    get_available_settings,
    get_registered_clients,
    get_registered_available_settings,
    get_client,
    get_session,
    set_session,
    # anti spider
    recalculate_wbi,
    refresh_buvid,
    refresh_bili_ticket,
    # credential
    Credential,
    # api
    HEADERS,
    bili_simple_download,
)
from .utils.AsyncEvent import AsyncEvent
from .utils.geetest import Geetest, GeetestMeta, GeetestType
from .exceptions import (
    ApiException,
    ArgsException,
    CookiesRefreshException,
    CredentialNoAcTimeValueException,
    CredentialNoBiliJctException,
    CredentialNoBuvid3Exception,
    CredentialNoBuvid4Exception,
    CredentialNoDedeUserIDException,
    CredentialNoSessdataException,
    DanmakuClosedException,
    DynamicExceedImagesException,
    ExClimbWuzhiException,
    GeetestException,
    LiveException,
    LoginError,
    NetworkException,
    ResponseCodeException,
    ResponseException,
    StatementException,
    VideoUploadException,
    WbiRetryTimesExceedException,
)
from . import (
    activity,
    app,
    article_category,
    article,
    ass,
    audio_uploader,
    audio,
    bangumi,
    black_room,
    channel_series,
    cheese,
    client,
    comment,
    creative_center,
    dynamic,
    emoji,
    favorite_list,
    festival,
    game,
    homepage,
    hot,
    interactive_video,
    live_area,
    live,
    login_v2,
    manga,
    music,
    note,
    opus,
    rank,
    search,
    session,
    show,
    topic,
    user,
    video_tag,
    video_uploader,
    video_zone,
    video,
    vote,
    watchroom,
)


BILIBILI_API_VERSION = "17.2.1"


def __register_all_clients():
    import importlib
    from .clients import ALL_PROVIDED_CLIENTS
    for module, client, settings in ALL_PROVIDED_CLIENTS[::-1]:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            continue
        client_module = importlib.import_module(
            name=f".clients.{client}", package="bilibili_api"
        )
        client_class = eval(f"client_module.{client}")
        register_client(module, client_class, settings)


__register_all_clients()


__all__ = [
    "ApiException",
    "AsyncEvent",
    "ArgsException",
    "BILIBILI_API_VERSION",
    "BiliAPIClient",
    "BiliAPIFile",
    "BiliAPIResponse",
    "BiliWsMsgType",
    "CookiesRefreshException",
    "Credential",
    "CredentialNoAcTimeValueException",
    "CredentialNoBiliJctException",
    "CredentialNoBuvid3Exception",
    "CredentialNoBuvid4Exception",
    "CredentialNoDedeUserIDException",
    "CredentialNoSessdataException",
    "Danmaku",
    "DanmakuClosedException",
    "DmFontSize",
    "DmMode",
    "DynamicExceedImagesException",
    "ExClimbWuzhiException",
    "Geetest",
    "GeetestException",
    "GeetestMeta",
    "GeetestType",
    "HEADERS",
    "LiveException",
    "LoginError",
    "NetworkException",
    "Picture",
    "ResourceType",
    "ResponseCodeException",
    "ResponseException",
    "SpecialDanmaku",
    "StatementException",
    "VideoUploadException",
    "WbiRetryTimesExceedException",
    "aid2bvid",
    "activity",
    "app",
    "article",
    "article_category",
    "ass",
    "audio",
    "audio_uploader",
    "bangumi",
    "bili_simple_download",
    "black_room",
    "bvid2aid",
    "channel_series",
    "cheese",
    "client",
    "comment",
    "creative_center",
    "dynamic",
    "emoji",
    "favorite_list",
    "festival",
    "game",
    "get_available_settings",
    "get_client",
    "get_real_url",
    "get_registered_available_settings",
    "get_registered_clients",
    "get_selected_client",
    "get_session",
    "homepage",
    "hot",
    "interactive_video",
    "live",
    "live_area",
    "login_v2",
    "manga",
    "music",
    "note",
    "opus",
    "parse_link",
    "rank",
    "recalculate_wbi",
    "refresh_bili_ticket",
    "refresh_buvid",
    "register_client",
    "request_log",
    "request_settings",
    "search",
    "select_client",
    "session",
    "set_session",
    "show",
    "sync",
    "topic",
    "unregister_client",
    "user",
    "video",
    "video_tag",
    "video_uploader",
    "video_zone",
    "vote",
    "watchroom",
]
