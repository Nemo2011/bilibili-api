import { set_proxy, get_session } from "./utils/network";
import { aid2bvid, bvid2aid } from "./utils/aid2bvid";
import { Proxy } from "./models/Proxy";
import { Credential } from "./models/Credential";
import { Danmaku, DmFontSize, DmMode } from "./models/Danmaku";

let HEADERS = {
    "User-Agent": "Mozilla/5.0", 
    "Referer": "https://www.bilibili.com"
}

function help(...config: any[]) {
    console.log("欢迎来到 bilibili-api-ts，这个模块是 Python bilibili-api 的 Typescript 克隆，适用于 JS/TS。\n文档请前往 https://nemo2011.github.io/bilibili-api/#/README-ts 查看。")
}

export {
    set_proxy, get_session,
    aid2bvid, bvid2aid, 
    Proxy, Credential, Danmaku, DmFontSize, DmMode,
    HEADERS, 
    help
};
