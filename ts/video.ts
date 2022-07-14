import { Credential } from "./models/Credential";
import { aid2bvid, bvid2aid } from "./utils/aid2bvid";
import { get_api } from "./utils/utils";
import { request } from "./utils/network"

const API: Record<any, any> = get_api("video")

export class Video {
    __info: Record<any, any> = {};
    __bvid: string = "";
    __aid: number = 0;
    credential: Credential = new Credential();

    constructor (bvid: string|null=null, aid: number|null=null, credential: Credential=new Credential()) {
        if (bvid !== null) {
            this.set_bvid(bvid);
        }
        else if (aid !== null) {
            this.set_aid(aid);
        }
        else {
            throw "请至少提供 bvid 和 aid 中的其中一个参数。";
        }
        this.credential = credential;
    }

    set_bvid(bvid: string) {
        if (bvid.length !== 12) {
            throw "bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。";
        }
        if (bvid.indexOf("BV") !== 0) {
            throw "bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。";
        }
        this.__bvid = bvid;
        this.__aid = bvid2aid(bvid);
    }

    get_bvid() {
        return this.__bvid;
    }

    set_aid(aid: number) {
        if (aid <= 0) {
            throw "aid 不能小于或等于 0。";
        }
        this.__aid = aid;
        this.__bvid = aid2bvid(aid);
    }

    get_aid() {
        return this.__aid;
    }

    async get_info() {
        var api = API["info"]["detail"];
        var params = {
            "bvid": this.get_bvid(), 
            "aid": this.get_aid()
        }
        var resp = await request(
            "GET", 
            api["url"], 
            params, 
            null, 
            this.credential
        )
        this.__info = resp;
        return resp;
    }
}