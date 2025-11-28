"""
bilibili_api

哔哩哔哩的各种 API 调用便捷整合（视频、动态、直播等），另外附加一些常用的功能。

 (默认已导入所有子模块，例如 `bilibili_api.video`, `bilibili_api.user`)
"""

from . import (
    activity,
    app,
    article,
    article_category,
    ass,
    audio,
    audio_uploader,
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
    garb,
    homepage,
    hot,
    interactive_video,
    live,
    live_area,
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
    video,
    video_tag,
    video_uploader,
    video_zone,
    vote,
    watchroom,
)
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
    InitialStateException,
    LiveException,
    LoginError,
    NetworkException,
    ResponseCodeException,
    ResponseException,
    StatementException,
    VideoUploadException,
    WbiRetryTimesExceedException,
)
from .utils.aid_bvid_transformer import aid2bvid, bvid2aid
from .utils.AsyncEvent import AsyncEvent
from .utils.danmaku import Danmaku, DmFontSize, DmMode, SpecialDanmaku
from .utils.geetest import Geetest, GeetestMeta, GeetestType
from .utils.network import (
    # api
    HEADERS,
    BiliAPIClient,
    BiliAPIFile,
    # session
    BiliAPIResponse,
    # filter
    BiliFilterFlags,
    BiliWsMsgType,
    # credential
    Credential,
    bili_simple_download,
    configure_dynamic_fingerprint,
    get_all_registered_post_filters,
    get_all_registered_pre_filters,
    get_available_settings,
    get_bili_ticket,
    # anti spider
    get_buvid,
    get_client,
    get_registered_available_settings,
    get_registered_clients,
    get_registered_post_filters,
    get_registered_pre_filters,
    get_selected_client,
    get_session,
    recalculate_wbi,
    register_client,
    register_post_filter,
    register_pre_filter,
    # log
    request_log,
    # settings
    request_settings,
    select_client,
    set_session,
    unregister_client,
    unregister_post_filter,
    unregister_pre_filter,
)
from .utils.parse_link import ResourceType, parse_link
from .utils.picture import Picture
from .utils.short import get_real_url
from .utils.sync import sync

BILIBILI_API_VERSION = "dev-dyn-fp"


def __register_all_clients():
    import importlib

    from .clients import ALL_PROVIDED_CLIENTS

    for module, client_name, settings in ALL_PROVIDED_CLIENTS[::-1]:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            continue
        client_module = importlib.import_module( # noqa: F841
            name=f".clients.{client_name}", package="bilibili_api"
        )
        client_class = eval(f"client_module.{client_name}")
        register_client(module, client_class, settings)


__register_all_clients()


__all__ = [
    "ApiException",
    "ArgsException",
    "AsyncEvent",
    "BiliAPIClient",
    "BiliAPIFile",
    "BiliAPIResponse",
    "BiliFilterFlags",
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
    "InitialStateException",
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
    "activity",
    "aid2bvid",
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
    "configure_dynamic_fingerprint",
    "creative_center",
    "dynamic",
    "emoji",
    "favorite_list",
    "festival",
    "game",
    "garb",
    "get_all_registered_post_filters",
    "get_all_registered_pre_filters",
    "get_available_settings",
    "get_bili_ticket",
    "get_buvid",
    "get_client",
    "get_real_url",
    "get_registered_available_settings",
    "get_registered_clients",
    "get_registered_post_filters",
    "get_registered_pre_filters",
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
    "register_client",
    "register_post_filter",
    "register_pre_filter",
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
    "unregister_post_filter",
    "unregister_pre_filter",
    "user",
    "video",
    "video_tag",
    "video_uploader",
    "video_zone",
    "vote",
    "watchroom",
]
