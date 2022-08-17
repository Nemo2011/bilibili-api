export const FavoriteListAPIData = {
    "info": {
        "list_list": {
        "url": "https://api.bilibili.com/x/v3/fav/folder/created/list-all",
        "method": "GET",
        "verify": false,
        "params": {
            "up_mid": "int: 用户 UID",
            "type": "int?: 资源类型，2 视频。",
            "rid": "int?: 资源 ID"
        },
        "comment": "获取收藏夹列表。提供 type 和 rid 时会同时提供对该资源收藏情况。"
        },
        "list_content": {
        "url": "https://api.bilibili.com/x/v3/fav/resource/list",
        "method": "GET",
        "verify": false,
        "params": {
            "media_id": "int: 收藏夹 ID",
            "pn": "int: 页码。",
            "ps": "int: 每页数量，固定 20。",
            "keyword": "str?: 关键词搜索。",
            "order": "str: 排序方式。mtime 最近收藏，view 最多播放，pubtime 最新投稿。",
            "type": "int: 收藏夹类型。目前固定 0。",
            "tid": "int: 分区 ID。0 为全部分区。"
        },
        "comment": "获取收藏夹列表内容。"
        },
        "list_topics": {
        "url": "https://api.bilibili.com/x/v2/fav/topic",
        "method": "GET",
        "verify": true,
        "params": {
            "pn": "int: 页码。",
            "ps": "int: 每页数量，固定 16。"
        },
        "comment": "获取自己的话题收藏夹内容。"
        },
        "list_articles": {
        "url": "https://api.bilibili.com/x/article/favorites/list/all",
        "method": "GET",
        "verify": true,
        "params": {
            "pn": "int: 页码。",
            "ps": "int: 每页数量，固定 16。"
        },
        "comment": "获取自己的专栏收藏夹内容。"
        },
        "list_albums": {
        "url": "https://api.vc.bilibili.com/user_plus/v1/Fav/getMyFav",
        "method": "GET",
        "verify": true,
        "params": {
            "page": "int: 页码。",
            "pagesize": "int: 每页数量，固定 30。",
            "biz_type": "const int: 2"
        },
        "comment": "获取自己的相簿收藏夹内容。"
        },
        "list_courses": {
        "url": "https://api.bilibili.com/pugv/app/web/favorite/page",
        "method": "GET",
        "verify": true,
        "params": {
            "pn": "int: 页码。",
            "ps": "int: 每页数量，固定 10。",
            "mid": "int: 自己的 UID。"
        },
        "comment": "获取自己的课程收藏夹内容。"
        },
        "list_notes": {
        "url": "https://api.bilibili.com/x/note/list",
        "method": "GET",
        "verify": true,
        "params": {
            "pn": "int: 页码。",
            "ps": "int: 每页数量，固定 10。"
        },
        "comment": "获取自己的笔记收藏夹内容。"
        }
    },
    "operate": {
        "new": {
        "url": "https://api.bilibili.com/x/v3/fav/folder/add",
        "method": "POST",
        "verify": true,
        "data": {
            "title": "str: 收藏夹标题。",
            "intro": "str: 收藏夹简介。",
            "privacy": "int bool: 是否为私有。",
            "cover": "str: 暂时为空"
        },
        "comment": "新建收藏夹。"
        },
        "modify": {
        "url": "https://api.bilibili.com/x/v3/fav/folder/edit",
        "method": "POST",
        "verify": true,
        "data": {
            "title": "str: 收藏夹标题。",
            "intro": "str: 收藏夹简介。",
            "privacy": "int bool: 是否为私有。",
            "cover": "str: 暂时为空",
            "media_id": "int: 收藏夹 ID。"
        },
        "comment": "修改收藏夹信息。"
        },
        "delete": {
        "url": "https://api.bilibili.com/x/v3/fav/folder/del",
        "method": "POST",
        "verify": true,
        "data": {
            "media_ids": "commaSeparatedList[int]: 收藏夹 ID。"
        },
        "comment": "删除收藏夹。"
        },
        "content_copy": {
        "url": "https://api.bilibili.com/x/v3/fav/resource/copy",
        "method": "POST",
        "verify": true,
        "data": {
            "src_media_id": "int: 源收藏夹 ID。",
            "tar_media_id": "int: 目标收藏夹 ID。",
            "mid": "int: 自己的 UID。",
            "resources": "commaSeparatedList[str]: 要操作的资源，格式：'资源 ID:资源类型'。视频类型为 2。如：'83051349:2'"
        },
        "comment": "复制资源到另一收藏夹。"
        },
        "content_move": {
        "url": "https://api.bilibili.com/x/v3/fav/resource/move",
        "method": "POST",
        "verify": true,
        "data": {
            "src_media_id": "int: 源收藏夹 ID。",
            "tar_media_id": "int: 目标收藏夹 ID。",
            "resources": "commaSeparatedList[str]: 要操作的资源，格式：'资源 ID:资源类型'。视频类型为 2。如：'83051349:2'"
        },
        "comment": "移动资源到另一收藏夹。"
        },
        "content_rm": {
        "url": "https://api.bilibili.com/x/v3/fav/resource/batch-del",
        "method": "POST",
        "verify": true,
        "data": {
            "media_id": "int: 收藏夹 ID。",
            "resources": "commaSeparatedList[str]: 要操作的资源，格式：'资源 ID:资源类型'。视频类型为 2。如：'83051349:2'"
        },
        "comment": "删除收藏夹中的资源。"
        },
        "content_clean": {
        "url": "https://api.bilibili.com/x/v3/fav/resource/clean",
        "method": "POST",
        "verify": true,
        "data": {
            "media_id": "int: 收藏夹 ID。"
        },
        "comment": "清理失效内容。"
        }
    }
}
