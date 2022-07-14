import { setProxy } from "./utils/network";
import { aid2bvid, bvid2aid } from "./utils/aid2bvid";
import { Proxy } from "./models/Proxy";
import { Credential } from "./models/Credential";

let HEADERS = {
    "User-Agent": "Mozilla/5.0", 
    "Referer": "https://www.bilibili.com"
}

export {setProxy, aid2bvid, bvid2aid, Proxy, Credential};
