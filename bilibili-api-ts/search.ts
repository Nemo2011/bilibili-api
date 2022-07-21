import { SearchData } from "./apis/search";
import { request, getAxiosInstance } from "./utils/network";

const API = SearchData;

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
 * param keyword 搜索关键词
 * 
 * param page 页数
 * 
 * @returns 
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
 * 搜索
 * 
 * param keyword 搜索关键词看
 * 
 * param search_type 搜索类型（SearchObjectType）
 * 
 * param page 页数
 * 
 * @returns 
 */
export async function web_search_by_type({keyword, search_type, page=1}: {keyword: string, search_type: SearchObjectType|string, page?: number}) {
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
