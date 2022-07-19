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

    /**
     * @param bvid Bvid(可选)
     * @param aid  Aid(可选)
     * @param credential 凭据类(可选)
     */
    constructor (bvid?: string, aid?:number, credential?: Credential) {
        if (credential === null && credential === undefined) {
            credential = new Credential();
        }
        if (bvid !== null && bvid !== undefined) {
            this.set_bvid(bvid);
        }
        else if (aid !== null && aid !== undefined) {
            this.set_aid(aid);
        }
        else {
            throw "请至少提供 bvid 和 aid 中的其中一个参数。";
        }
        this.credential = credential;
    }

    /**
     * 设置 bvid
     * 
     * @param bvid Bvid
     */
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

    /**
     * 获取 bvid
     * 
     * @returns Bvid
     */
    get_bvid() {
        return this.__bvid;
    }

    /**
     * 设置 aid
     * 
     * @param aid Aid
     */
    set_aid(aid: number) {
        if (aid <= 0) {
            throw "aid 不能小于或等于 0。";
        }
        this.__aid = aid;
        this.__bvid = aid2bvid(aid);
    }

    /**
     * 获取 aid
     * 
     * @returns aid
     */
    get_aid() {
        return this.__aid;
    }

    /**
     * 获取视频详细信息
     * 
     * @returns 调用 API 返回的结果
     */
    async get_info() {
        var api = API["info"]["detail"];
        var params = {
            "bvid": this.get_bvid(), 
            "aid": this.get_aid()
        }
        var resp = await request(
            "GET", 
            api['url'], 
            params, 
            null, 
            this.credential
        )
        this.__info = resp;
        return resp;
    }

    /**
     * 获取视频详细信息的内存中的缓存数据
     * 
     * @returns 调用 API 返回的结果
     */
    async __get_info_cached() {
        if (this.__info === null) {
            return await this.get_info()
        }
        return this.__info
    }

    /**
     * 获取视频统计数据
     * 
     * @returns 调用 API 返回的结果
     */
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

    /**
     * 获取视频标签
     * 
     * @returns 调用 API 返回的结果
     */
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

    /**
     * 获取视频充电信息
     * 
     * @returns 调用 API 返回的结果
     */
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

    /**
     * 获取视频分 P 信息
     * 
     * @returns 调用 API 返回的结果
     */
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

    /**
     * 获取分 P 对应的 cid
     * 
     * @param page_index 
     * @returns number: cid
     */
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

    /**
     * 获取分 P 对应的 cid
     * 
     * @param page_index 
     * @returns number: cid
     */
    async get_cid(page_index) {
        return await this.__get_page_id_by_index(page_index);
    }

    /**
     * 获取视频播放流（下载地址）
     * 
     * @param page_index 分 P 序号
     * @param cid 分 P 编号
     * @param html5 是否以 html5 端获取（这样子可以直接在网页中显示，但是视频源单一）
     * @returns 调用 API 返回的结果
     */
    async get_download_url(
        page_index?: number, 
        cid?: number, 
        html5: boolean=false
    ) { 
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
