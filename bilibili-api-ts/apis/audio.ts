export const AudioData = {
    "audio_info": {
        "info": {
        "url": "https://www.bilibili.com/audio/music-service-c/web/song/info",
        "method": "GET",
        "verify": false,
        "params": {
            "sid": "int: 音频 au 号"
        },
        "comment": "获取音频信息"
        },
        "tag": {
        "url": "https://www.bilibili.com/audio/music-service-c/web/tag/song",
        "method": "GET",
        "verify": false,
        "params": {
            "sid": "int: 音频 au 号"
        },
        "comment": "获取音频 tag"
        },
        "user": {
        "url": "https://www.bilibili.com/audio/music-service-c/web/stat/user",
        "method": "GET",
        "verify": false,
        "params": {
            "uid": "int: 用户 UID"
        },
        "comment": "获取用户数据（收听数，粉丝数等）"
        },
        "download_url": {
        "url": "https://www.bilibili.com/audio/music-service-c/web/url",
        "method": "GET",
        "verify": false,
        "params": {
            "sid": "int: 音频 au 号",
            "privilege": "const int: 2",
            "quality": "const int: 2"
        },
        "comment": "获取音频文件下载链接，目前音质貌似不可控"
        }
    },
    "audio_operate": {
        "coin": {
        "url": "https://www.bilibili.com/audio/music-service-c/web/coin/add",
        "method": "POST",
        "verify": true,
        "data": {
            "sid": "int: 歌单 ID",
            "multiply": "int: 硬币数量，最大 2"
        },
        "comment": "投币"
        }
    },
    "list_info": {
        "info": {
        "url": "https://www.bilibili.com/audio/music-service-c/web/menu/info",
        "method": "GET",
        "verify": false,
        "params": {
            "sid": "int: 歌单 ID"
        },
        "comment": "获取歌单信息"
        },
        "tag": {
        "url": "https://www.bilibili.com/audio/music-service-c/web/tag/menu",
        "method": "GET",
        "verify": false,
        "params": {
            "sid": "int: 歌单 ID"
        },
        "comment": "获取歌单 tag"
        },
        "song_list": {
        "url": "https://www.bilibili.com/audio/music-service-c/web/song/of-menu",
        "method": "GET",
        "verify": false,
        "params": {
            "sid": "int: 歌单 ID",
            "pn": "int: 页码",
            "ps": "const int: 100"
        },
        "comment": "获取歌单歌曲列表"
        }
    },
    "list_operate": {
        "set_favorite": {
        "url": "https://www.bilibili.com/audio/music-service-c/web/collect/menu",
        "method": "POST",
        "verify": true,
        "data": {
            "sid": "int: 歌单 ID"
        },
        "comment": "收藏歌单"
        },
        "del_favorite": {
        "url": "https://www.bilibili.com/audio/music-service-c/web/collect/menu",
        "method": "DELETE",
        "verify": true,
        "params": {
            "sid": "int: 歌单 ID"
        },
        "data": {
            "csrf": "csrf"
        },
        "comment": "取消收藏歌单"
        }
    }
}