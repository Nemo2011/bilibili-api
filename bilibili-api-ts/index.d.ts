import { set_proxy, get_session } from "./utils/network";
import { aid2bvid, bvid2aid } from "./utils/aid2bvid";
import { Proxy } from "./models/Proxy";
import { Credential } from "./models/Credential";
import { Danmaku, DmFontSize, DmMode } from "./models/Danmaku";
declare let HEADERS: {
    "User-Agent": string;
    Referer: string;
};
declare function help(...config: any[]): void;
export { set_proxy, get_session, aid2bvid, bvid2aid, Proxy, Credential, Danmaku, DmFontSize, DmMode, HEADERS, help };
