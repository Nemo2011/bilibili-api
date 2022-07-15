import { Credential } from "./models/Credential";
import { aid2bvid, bvid2aid } from "./utils/aid2bvid";
import { request } from "./utils/network"
import { VideoData } from "./apis/video";

const API: Record<any, any> = VideoData

export class Video {
    __info: Record<any, any>|null = null;
    __bvid: string = "";
    __aid: number = 0;
    credential: Credential = new Credential();

    constructor (config: any) {
        var bvid: string|null|undefined = config.bvid;
        var aid: number|null|undefined  = config.aid;
        var credential: Credential|null|undefined = config.credential;
        if (credential === null && credential === undefined) {
            credential = new Credential();
        }
        if (bvid !== null && bvid !== undefined) {
            this.set_bvid({bvid: bvid});
        }
        else if (aid !== null && aid !== undefined) {
            this.set_aid({aid: aid});
        }
        else {
            throw "请至少提供 bvid 和 aid 中的其中一个参数。";
        }
        this.credential = credential;
    }

    set_bvid(config: any) {
        var bvid: string = config.bvid;
        if (bvid.length !== 12) {
            throw "bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。";
        }
        if (bvid.indexOf("BV") !== 0) {
            throw "bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。";
        }
        this.__bvid = bvid;
        this.__aid = bvid2aid({bvid: bvid});
    }

    get_bvid() {
        return this.__bvid;
    }

    set_aid(config: any) {
        var aid: number = config.aid;

        if (aid <= 0) {
            throw "aid 不能小于或等于 0。";
        }
        this.__aid = aid;
        this.__bvid = aid2bvid({aid: aid});
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

    async __get_info_cached() {
        if (this.__info === null) {
            return await this.get_info()
        }
        return this.__info
    }

    async get_stat() {
        var api = API['info']['stat'];
        var params = {
            "bvid": this.get_bvid(), 
            "aid": this.get_aid()
        };
        return await request(
            "GET", 
            api['url'], 
            params, 
            null, 
            this.credential
        );
    }

    async get_tags() {
        var api = API['info']['tags'];
        var params = {
            "bvid": this.get_bvid(), 
            "aid": this.get_aid()
        };
        return await request(
            "GET", 
            api['url'], 
            params, 
            null, 
            this.credential
        )
    }

    async get_chargers() {
        var info = await this.__get_info_cached();
        var mid = info['owner']['mid'];
        var api = API['info']['chargers'];
        var params = {
            "aid": this.get_aid(), 
            "bvid": this.get_bvid(), 
            "mid": mid
        };
        return await request(
            "GET", 
            api['url'], 
            params, 
            null, 
            this.credential
        )
    }

    async get_pages() {
        var api = API["info"]["pages"];
        var params = {
            "aid": this.get_aid(), 
            "bvid": this.get_bvid()
        }
        return await request(
            "GET", 
            api['url'], 
            params, 
            null, 
            this.credential
        )
    }

    async __get_page_id_by_index(page_index: number) {
        if (page_index < 0) {
            throw "分 p 号必须大于或等于 0。";
        }
        var info = await this.__get_info_cached();
        var pages = info['pages'];

        if (pages.length <= 0) {
            throw "不存在该分 p。";
        }

        var page = pages[page_index];
        var cid = page['cid'];
        return cid
    }

    async get_download_url(
        config: any
    ) { 
        var page_index: number|null|undefined = config.page_index;
        var cid: number|null|undefined = config.cid;
        var html5: boolean|null|undefined = config.html5;
        if (cid === null || cid === undefined) {
            if (page_index === null || page_index === undefined) {
                throw "page_index 和 cid 至少提供一个。";
            }
            else {
                cid = await this.__get_page_id_by_index(page_index);
            }
        }
        var api = API['info']['playurl'];
        var params = {
            "avid": this.get_aid(), 
            "cid": cid, 
            "qn": "127", 
            "otype": "json", 
            "fnval": 4048, 
            "fourk": 1
        };
        if (html5 === true) {
            params['platform'] = 'html5';
        }
        return await request(
            "GET", 
            api['url'], 
            params, 
            null, 
            this.credential
        );
    }
}