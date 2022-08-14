import { Credential } from "./models/Credential";
import { get_session, request } from "./utils/network"
import { UserAPIData } from "./apis/user";

const API = UserAPIData;

/**
 * 视频排序顺序。
 *
 * + PUBDATE : 上传日期倒序。
 *
 * + FAVORITE: 收藏量倒序。
 *
 * + VIEW    : 播放量倒序。
 */
export enum VideoOrder {
    PUBDATE = "pubdate", 
    FAVORITE = "stow", 
    VIEW = "click"
}

/**
 * 合集视频排序顺序。
 * 
 * + DEFAULT: 默认排序
 * 
 * + CHANGE : 升序排序
 */
export enum ChannelOrder {
    DEFAULT = "false", 
    CHANGE = "true"
}

/**
 * 音频排序顺序。
 *
 * + PUBDATE : 上传日期倒序。
 *
 * + FAVORITE: 收藏量倒序。
 *
 * + VIEW    : 播放量倒序。
 */
export enum AudioOrder {
    PUBDATE = 1, 
    VIEW = 2, 
    FAVORITE = 3
}

/**
 * 用户相关
 */
export class User {
    uid: number;
    credential: Credential = new Credential({});
    __self_info: Object = null;
    /**
     * uid(number)           : 用户 uid
     * 
     * credential(Credential): 凭据类
     */
    constructor ({uid, credential=new Credential({})}: {uid: number, credential?: Credential}) {
        this.uid = uid;
        if (credential === null || credential === undefined) {
            credential = new Credential({});
        }
        this.credential = credential;
        this.__self_info = null;
    }

    /**
     * 获取用户信息（昵称，性别，生日，签名，头像 URL，空间横幅 URL 等）
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_user_info({}) {
        var api = API.info.info;
        var params = {
            mid: this.uid
        };
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }
    
    /**
     * 获取自己的信息。如果存在缓存则使用缓存。
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async __get_self_info({}){
        if (this.__self_info !== null) return this.__self_info;

        this.__self_info = await get_self_info({
            credential: this.credential
        });
        return this.__self_info;
    }

    /**
     * 获取用户 uid
     * 
     * @returns {number} 用户 uid
     */
    get_uid({}) {
        return this.uid;
    }

    /**
     * 获取用户关系信息（关注数，粉丝数，悄悄关注，黑名单数）
     * 
     * @returns {Object} 调用接口返回的内容。
     */
    async get_relation_info({}) {
        var api = API.info.relation;
        var params = {
            vmid: this.uid
        };
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }

    /**
     * 获取 UP 主数据信息（视频总播放量，文章总阅读量，总点赞数）
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_up_stat({}) {
        this.credential.raise_for_no_bili_jct({});

        var api = API.info.upstat;
        var params = {
            mid: this.uid
        };
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }

    /**
     * 获取用户直播间信息。
     * 
     * @returns 
     */
    async get_live_info({}) {
        var api = API.info.live;
        var params = {
            mid: this.uid
        };
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }

    /**
     * 获取用户投稿视频信息。
     * 
     * param tid(number, optional)      : 分区 ID. Defaults to 0(全部).
     * 
     * param pn(number, optional)       : 页码，从 1 开始. Defaults to 1. 
     * 
     * param ps(number, optional)       : 每一页的视频数. Defaults to 30. 
     * 
     * param keyword(string, optional)  : 搜索关键词. Defaults to "". 
     * 
     * param order(VideoOrder, optional): 排序方式. Defaults to VideoOrder.PUBDATE
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_videos({tid, pn, ps, keyword, order}: {
        tid?: number, 
        pn?: number, 
        ps?: number, 
        keyword?: string, 
        order?: VideoOrder
    }) {
        if (tid === null || tid === undefined) tid = 0;
        if (pn === null || pn === undefined) pn = 1;
        if (ps === null || ps === undefined) ps = 30;
        if (keyword === null || keyword === undefined) keyword = "";
        if (order === null || order === undefined) order = VideoOrder.PUBDATE;
        
        var api = API.info.video;
        var params = {
            mid: this.uid, 
            ps: ps, 
            tid: tid, 
            pn: pn, 
            keyword: keyword, 
            order: order
        }
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }

    /**
     * 获取用户投稿音频。
     * 
     * param pn(number, optional)       : 页码，从 1 开始. Defaults to 1. 
     * 
     * param ps(number, optional)       : 每一页的音频数. Defaults to 30. 
     * 
     * param order(AudioOrder, optional): 排序方式. Defaults to AudioOrder.PUBDATE
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_audios({order, pn, ps}: {
        order?: AudioOrder, 
        pn?: number, 
        ps?: number
    }) {
        if (pn === null || pn === undefined) pn = 1;
        if (ps === null || ps === undefined) ps = 30;
        if (order === null || order === undefined) order = AudioOrder.PUBDATE
        
        var api = API.info.audio;
        var params = {
            uid: this.uid, 
            ps: ps, 
            pn: pn, 
            order: order
        }
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }
}

/**
 * 获取自己的信息
 * 
 * param credential(Credential): 凭据类
 * 
 * @returns {Object} 调用 API 返回的结果
 */
export async function get_self_info({credential}: {credential: Credential}) {
    var api = API.info.my_info;
    credential.raise_for_no_sessdata({});

    return await request({
        method: "GET", 
        url: api.url, 
        credential: credential
    });
}

/**
 * 获取用户浏览历史记录
 * 
 * param page_num(number)      : 页码数
 * 
 * param per_page_item(number) : 每页多少条历史记录
 * 
 * param credential(Credential): Credential
 * 
 * @returns {Object} 返回当前页的指定历史记录列表
 */
export async function get_self_history({
    page_num, 
    per_page_item,
    credential
}:{
    page_num?: number, 
    per_page_item?: number, 
    credential: Credential
}) {
    if (page_num === null || page_num === undefined) {
        page_num = 1;
    }
    if (per_page_item === null || per_page_item === undefined) {
        per_page_item = 100;
    }

    credential.raise_for_no_sessdata({});

    var api = API.info.history;
    var params = {
        pn: page_num, 
        ps: per_page_item
    };

    return await request({
        method: "GET", 
        url: api.url, 
        params: params, 
        credential: credential
    });
}
