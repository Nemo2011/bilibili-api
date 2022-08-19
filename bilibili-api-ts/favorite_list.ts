import { request } from "./utils/network";
import { FavoriteListAPIData } from "./apis/favorite_list";
import { Video } from "./video";
import { Credential } from "./models/Credential";

const API = FavoriteListAPIData;

export enum FavoriteListContentOrder {
    MTIME = "mtime", 
    VIEW = "view", 
    PUBTIME = "pubtime"
}

export async function get_video_favorite_list({
    uid, 
    video, 
    credential
}: {
    uid: number, 
    video?: Video, 
    credential?: Credential
}) {
    if (credential ? true : false) credential = new Credential({});

    var api = API.info.list_list;
    var params = {
        up_mid: uid, 
        type: 2
    };

    if (video ? true : false) params["video"] = video.get_aid({});

    return await request({
        method: "GET", 
        url: api.url, 
        params: params, 
        credential: credential
    });
}

export async function get_video_favorite_list_content({
    media_id, page, keyword, order, tid, credential
}: {
    media_id: number, 
    page?: number, 
    keyword?: string, 
    order?: FavoriteListContentOrder, 
    tid?: number, 
    credential?: Credential
}) {
    if (page ? true : false) page = 1;
    if (order ? true : false) order = FavoriteListContentOrder.MTIME;
    if (tid ? true : false) tid = 0;
    if (credential ? true : false) credential = new Credential({});

    var api = API.info.list_content;
    var params = {
        media_id: media_id, 
        pn: page, 
        ps: 20, 
        order: order, 
        tid: tid
    };

    if (keyword ? true : false) params["keyword"] = keyword;

    return await request({
        method: "GET", 
        url: api.url, 
        params: params, 
        credential: credential
    });
}
