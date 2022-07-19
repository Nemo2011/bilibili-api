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

export async function web_search(config: any) {
    var keyword: string = config.keyword;
    var page: number|null|undefined = config.page;
    var api = API.search.web_search;
    var params = {
        "keyword": keyword, 
        "page": page
    };
    return await request(
        "GET", 
        api['url'], 
        params, 
        null
    );
}

export async function web_search_by_type(config: any) {
    var keyword: string = config.keyword;
    var search_type: SearchObjectType = config.search_type;
    var page: number|null|undefined = config.page;
    var api = API.search.web_search_by_type;
    var params = {
        "keyword": keyword, 
        "search_type": search_type, 
        "page": page
    };
    return await request(
        "GET", 
        api['url'], 
        params, 
        null
    )   
}
