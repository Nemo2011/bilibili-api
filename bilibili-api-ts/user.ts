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
    async get_uid({}) {
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
