/**
 * 搜索对象枚举。
 *
    + VIDEO : 视频

    + BANGUMI : 番剧

    + FT : 影视

    + LIVE : 直播

    + ARTICLE : 专栏

    + TOPIC : 话题
    
    + USER : 用户
 */
export declare enum SearchObjectType {
    VIDEO = "video",
    BANGUMI = "media_bangumi",
    FT = "media_ft",
    LIVE = "live",
    ARTICLE = "article",
    TOPIC = "topic",
    USER = "bili_user"
}
/**
 * 搜索
 *
 * params keyword(string): 搜索关键词
 *
 * params page(number)   : 页码
 *
 * @returns {Object} 调用 API 返回的结果
 */
export declare function web_search({ keyword, page }: {
    keyword: string;
    page?: number;
}): Promise<any>;
/**
 * 根据指定类型搜索
 *
 * param keyword(string):                      搜索关键词
 *
 * param search_type(SearchObjectType|string): 搜索类型
 *
 * param page(number):                         页码
 *
 * @returns {Object} 调用 API 返回的结果
 */
export declare function web_search_by_type({ keyword, search_type, page }: {
    keyword: string;
    search_type: SearchObjectType | string;
    page?: number;
}): Promise<any>;
/**
 * 获取默认搜索内容
 *
 * @returns {Object} 调用 API 返回的结果
 */
export declare function get_default_search_keyword({}: {}): Promise<any>;
/**
 * 获取热搜
 *
 * @returns {Object} 调用 API 返回的结果
 */
export declare function get_hot_search_keywords({}: {}): Promise<any>;
