import { Credential } from "./models/Credential";
/**
 * 视频排序顺序。
 *
 * + PUBDATE : 上传日期倒序。
 *
 * + FAVORITE: 收藏量倒序。
 *
 * + VIEW    : 播放量倒序。
 */
export declare enum VideoOrder {
    PUBDATE = "pubdate",
    FAVORITE = "stow",
    VIEW = "click"
}
/**
 * 用户相关
 */
export declare class User {
    uid: number;
    credential: Credential;
    __self_info: Object;
    /**
     * uid(number)           : 用户 uid
     *
     * credential(Credential): 凭据类
     */
    constructor({ uid, credential }: {
        uid: number;
        credential?: Credential;
    });
    /**
     * 获取用户信息（昵称，性别，生日，签名，头像 URL，空间横幅 URL 等）
     *
     * @returns {Object} 调用 API 返回的结果
     */
    get_user_info({}: {}): Promise<any>;
    /**
     * 获取用户 uid
     *
     * @returns {number} 用户 uid
     */
    get_uid({}: {}): Promise<number>;
}
