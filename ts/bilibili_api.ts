import { getAxiosInstance, setAxiosInstance } from "./utils/network";
import { aid2bvid, bvid2aid } from "./utils/aid2bvid";

let HEADERS = {
    "User-Agent": "Mozilla/5.0", 
    "Referer": "https://www.bilibili.com"
}

export = {
    getAxiosInstance, 
    setAxiosInstance, 
    aid2bvid,
    bvid2aid, 
    HEADERS
}
