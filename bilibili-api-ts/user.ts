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
     * 获取用户 uid
     * 
     * @returns {number} 用户 uid
     */
    async get_uid({}) {
        return this.uid;
    }
}