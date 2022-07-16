import { setProxy } from "./utils/network";
import { aid2bvid, bvid2aid } from "./utils/aid2bvid";
import { Proxy } from "./models/Proxy";
import { Credential } from "./models/Credential";
declare let HEADERS: {
    "User-Agent": string;
    Referer: string;
};
declare function help(...config: any[]): void;
export { setProxy, aid2bvid, bvid2aid, Proxy, Credential, HEADERS, help };
