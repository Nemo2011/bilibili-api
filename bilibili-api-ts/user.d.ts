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
 * 合集视频排序顺序。
 *
 * + DEFAULT: 默认排序
 *
 * + CHANGE : 升序排序
 */
export declare enum ChannelOrder {
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
export declare enum AudioOrder {
    PUBDATE = 1,
    VIEW = 2,
    FAVORITE = 3
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
     * 获取自己的信息。如果存在缓存则使用缓存。
     *
     * @returns {Object} 调用 API 返回的结果
     */
    __get_self_info({}: {}): Promise<Object>;
    /**
     * 获取用户 uid
     *
     * @returns {number} 用户 uid
     */
    get_uid({}: {}): number;
    /**
     * 获取用户关系信息（关注数，粉丝数，悄悄关注，黑名单数）
     *
     * @returns {Object} 调用接口返回的内容。
     */
    get_relation_info({}: {}): Promise<any>;
    /**
     * 获取 UP 主数据信息（视频总播放量，文章总阅读量，总点赞数）
     *
     * @returns {Object} 调用 API 返回的结果
     */
    get_up_stat({}: {}): Promise<any>;
    /**
     * 获取用户直播间信息。
     *
     * @returns
     */
    get_live_info({}: {}): Promise<any>;
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
    get_videos({ tid, pn, ps, keyword, order }: {
        tid?: number;
        pn?: number;
        ps?: number;
        keyword?: string;
        order?: VideoOrder;
    }): Promise<any>;
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
    get_audios({ order, pn, ps }: {
        order?: AudioOrder;
        pn?: number;
        ps?: number;
    }): Promise<any>;
}
/**
 * 获取自己的信息
 *
 * param credential(Credential): 凭据类
 *
 * @returns {Object} 调用 API 返回的结果
 */
export declare function get_self_info({ credential }: {
    credential: Credential;
}): Promise<any>;
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
export declare function get_self_history({ page_num, per_page_item, credential }: {
    page_num?: number;
    per_page_item?: number;
    credential: Credential;
}): Promise<any>;
