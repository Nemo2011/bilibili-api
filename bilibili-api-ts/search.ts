import { SearchData } from "./apis/search";
import { request } from "./utils/network";

const API = SearchData;

/**
 * 搜索对象枚举。
    + VIDEO : 视频
    + BANGUMI : 番剧
    + FT : 影视
    + LIVE : 直播
    + ARTICLE : 专栏
    + TOPIC : 话题
    + USER : 用户
 */
export enum SearchObjectType {
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
export async function web_search({keyword, page=1}: {keyword: string, page?: number}) {
    var api = API.search.web_search;
    var params = {
        "keyword": keyword, 
        "page": page
    };
    return await request(
        {
            method: "GET", 
            url: api['url'], 
            params: params
        }
    );
}

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
export async function web_search_by_type({keyword, search_type, page=1}: {keyword: string, search_type: SearchObjectType|string, page?: number}){
    var api = API.search.web_search_by_type;
    var params = {
        "keyword": keyword, 
        "search_type": search_type, 
        "page": page
    };
    return await request(
        {
            method: "GET", 
            url: api['url'], 
            params: params
        }
    )   
}
