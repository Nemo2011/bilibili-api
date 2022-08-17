import { Credential } from "./models/Credential";
import { aid2bvid, bvid2aid } from "./utils/aid2bvid";
import { get_session, request } from "./utils/network"
import { VideoData } from "./apis/video";

const API: Record<any, any> = VideoData

/**
 * 视频相关
 */
export class Video {
    __info: Record<any, any> | null = null;
    __bvid: string = "";
    __aid: number = 0;
    credential: Credential = new Credential({});

    /**
     * param bvid(int)              Bvid(可选)
     * 
     * param aid(int)               Aid(可选)
     * 
     * param credential(Credential) 凭据类(可选)
     */
    constructor({ bvid = null, aid = null, credential = new Credential({}) }: { bvid?: string | null, aid?: number | null, credential?: Credential }) {
        if (credential === null && credential === undefined) {
            credential = new Credential({});
        }
        if (bvid !== null && bvid !== undefined) {
            this.set_bvid({ bvid: bvid });
        }
        else if (aid !== null && aid !== undefined) {
            this.set_aid({ aid: aid });
        }
        else {
            throw "请至少提供 bvid 和 aid 中的其中一个参数。";
        }
        this.credential = credential;
    }

    /**
     * 设置 bvid
     * 
     * param bvid(string) Bvid
     */
    set_bvid({ bvid }: { bvid: string }) {
        if (bvid.length !== 12) {
            throw "bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。";
        }
        if (bvid.indexOf("BV") !== 0) {
            throw "bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。";
        }
        this.__bvid = bvid;
        this.__aid = bvid2aid({ bvid: bvid });
    }

    /**
     * 获取 bvid
     * 
     * @returns Bvid
     */
    get_bvid({ }) {
        return this.__bvid;
    }

    /**
     * 设置 aid
     * 
     * param aid(number) Aid
     */
    set_aid({ aid }: { aid: number }) {
        if (aid <= 0) {
            throw "aid 不能小于或等于 0。";
        }
        this.__aid = aid;
        this.__bvid = aid2bvid({ aid: aid });
    }

    /**
     * 获取 aid
     * 
     * @returns aid
     */
    get_aid({ }) {
        return this.__aid;
    }

    /**
     * 获取视频详细信息
     * 
     * @returns 调用 API 返回的结果
     */
    async get_info({ }) {
        var api = API["info"]["detail"];
        var params = {
            "bvid": this.get_bvid({}),
            "aid": this.get_aid({})
        }
        var resp = await request(
            {
                method: "GET",
                url: api['url'],
                params: params,
                credential: this.credential
            }
        )
        this.__info = resp;
        return resp;
    }

    /**
     * 获取视频详细信息的内存中的缓存数据
     * 
     * @returns 调用 API 返回的结果
     */
    async __get_info_cached({ }) {
        if (this.__info === null) {
            return await this.get_info({})
        }
        return this.__info
    }

    /**
     * 获取视频统计数据
     * 
     * @returns 调用 API 返回的结果
     */
    async get_stat({ }) {
        var api = API['info']['stat'];
        var params = {
            "bvid": this.get_bvid({}),
            "aid": this.get_aid({})
        };
        return await request(
            {
                method: "GET",
                url: api['url'],
                params: params,
                credential: this.credential
            }
        );
    }

    /**
     * 获取视频标签
     * 
     * @returns 调用 API 返回的结果
     */
    async get_tags({ }) {
        var api = API['info']['tags'];
        var params = {
            "bvid": this.get_bvid({}),
            "aid": this.get_aid({})
        };
        return await request(
            {
                method: "GET",
                url: api['url'],
                params: params,
                credential: this.credential
            }
        )
    }

    /**
     * 获取视频充电信息
     * 
     * @returns 调用 API 返回的结果
     */
    async get_chargers() {
        var info = await this.__get_info_cached({});
        var mid = info['owner']['mid'];
        var api = API['info']['chargers'];
        var params = {
            "aid": this.get_aid({}),
            "bvid": this.get_bvid({}),
            "mid": mid
        };
        return await request(
            {
                method: "GET",
                url: api['url'],
                params: params,
                credential: this.credential
            }
        )
    }

    /**
     * 获取视频分 P 信息
     * 
     * @returns 调用 API 返回的结果
     */
    async get_pages({ }) {
        var api = API["info"]["pages"];
        var params = {
            "aid": this.get_aid({}),
            "bvid": this.get_bvid({})
        }
        return await request(
            {
                method: "GET",
                url: api['url'],
                params: params,
                credential: this.credential
            }
        )
    }

    /**
     * 获取分 P 对应的 cid
     * 
     * param page_index(int) 分 P 序号
     * 
     * @returns number: cid
     */
    async __get_page_id_by_index(page_index: number) {
        if (page_index < 0) {
            throw "分 p 号必须大于或等于 0。";
        }
        var info = await this.__get_info_cached({});
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
     * param page_index(number) 分 P 序号
     *
     * @returns number: cid
     */
    async get_cid({ page_index }: { page_index?: number }) {
        if (page_index === null || page_index === undefined) {
            page_index = 0;
        }
        return await this.__get_page_id_by_index(page_index);
    }

    /**
     * 获取视频播放流（下载地址）
     * 
     * param page_index(number) 分 P 序号(可选)
     * 
     * param cid(number)        分 P 编号(可选)
     * 
     * param html5(boolean)     是否以 html5 端获取（这样子可以直接在网页中显示，但是视频源单一）(可选)
     * 
     * page_index 和 cid 请务必提供一个。
     * 
     * @returns 调用 API 返回的结果
     */
    async get_download_url(
        { page_index = null, cid = null, html5 = false }:
            {
                page_index?: number | null,
                cid?: number | null,
                html5?: boolean
            }
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
            "avid": this.get_aid({}),
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
            {
                method: "GET",
                url: api['url'],
                params: params,
                credential: this.credential
            }
        );
    }

    /**
     * 获取相关视频信息
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_related({}) {
        var api = API.info.related;
        var params = {
            aid: this.get_aid({}), 
            bvid: this.get_bvid({})
        };
        return await request({
            method: "GET", 
            url: api["url"], 
            params: params, 
            credential: this.credential
        })
    }

    /**
     * 视频是否点赞过
     * 
     * @returns {bool} 视频是否点赞过
     */
    async has_liked({}) {
        this.credential.raise_for_no_sessdata({});
        var api = API.info.has_liked;
        var params = {
            bvid: this.get_bvid({}), 
            aid: this.get_aid({})
        }
        return (await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        })) === 1;
    }

    /**
     * 获取视频已投币数量
     * 
     * @returns {number} 视频已投币数量
     */
    async get_pay_coins({}) {
        this.credential.raise_for_no_sessdata({});
        var api = API.info.get_pay_coins;
        var params = {
            bvid: this.get_bvid({}), 
            aid: this.get_aid({})
        }
        return (await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        }))['multiply']
    }

    /**
     * 是否已收藏
     * 
     * @returns {bool} 视频是否已收藏
     */
    async has_favoured({}) {
        this.credential.raise_for_no_sessdata({});
        var api = API.info.has_favoured;
        var params = {
            bvid: this.get_bvid({}), 
            aid: this.get_aid({})
        }
        return (await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        }))['favoured'];
    }

    /**
     * 获取收藏夹列表信息，用于收藏操作，含各收藏夹对该视频的收藏状态。
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_media_list({}) {
        this.credential.raise_for_no_sessdata({});
        var info = await this.__get_info_cached({});
        var api = API.info.media_list;
        var params = {
            type: 2, 
            rid: this.get_aid({}),
            up_mid: info.owner.mid
        }
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        })
    }

    /**
     * 获取高能进度条
     * 
     * param page_index(number) 分 P 序号(可选)
     * 
     * param cid(number)        分 P 编号(可选)
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_pbp({page_index=null, cid=null}: {page_index?: number|null, cid?: number|null}) {
        if (cid === null || cid === undefined) {
            if (page_index === null || page_index === undefined) {
                throw "page_index 和 cid 至少提供一个。";
            }
            else {
                cid = await this.__get_page_id_by_index(page_index);
            }
        }

        var api = API.info.pbp;
        var params = {
            cid: cid
        };
        var sess = await get_session({credential: this.credential});
        return (await (await sess).request({
            url: api.url, 
            method: "GET", 
            params: params
        })).data
    }

    /**
     * 点赞视频。
     * 
     * param status (bool, optional): 点赞状态。Defaults to True.
     * 
     * @returns {null} 调用 API 返回的结果。
     */
    async like({status}: {status: boolean}) {
        if (status === undefined || status == null) {
            status = true;
        }
        this.credential.raise_for_no_sessdata({});
        this.credential.raise_for_no_bili_jct({});
        var api = API.operate.like;
        var datas = {
            aid: this.get_aid({}), 
            like: status ? 1 : 2, 
            csrf: this.credential.bili_jct, 
            csrf_token: this.credential.bili_jct
        }
        return await request({
            method: "POST", 
            url: api.url, 
            params: datas,
            credential: this.credential
        })
    }

    /**
     * 投币
     * 
     * param num(number)  : 投币数量，1 ~ 2, default to 1
     * 
     * param like(boolean): 是否同时点赞，default to false
     * 
     * @returns {null} 调用 API 返回的结果。
     */
    async pay_coin({num=1, like=false}: {num: number, like: boolean}) {
        if (like === undefined || like === null) like = false;

        this.credential.raise_for_no_sessdata({});
        this.credential.raise_for_no_bili_jct({});

        if (num !== 1 && num !== 2) {
            throw "投币数量只能是 1 ~ 2 个。";
        }
        var api = API.operate.coin;
        var datas = {
            "aid": this.get_aid({}),
            "bvid": this.get_bvid({}),
            "multiply": num,
            "like": like ? 1 : 0,
            "csrf": this.credential.bili_jct, 
            "csrf_token": this.credential.bili_jct
        }
        return await request({
            method: "POST", 
            url: api.url,
            params: datas, 
            credential: this.credential
        })
    }

    async set_favorite({add_media_ids, del_media_ids}: {
        add_media_ids?: Object[], 
        del_media_ids?: Object[]
    }) {
        add_media_ids = add_media_ids ? add_media_ids : [];
        del_media_ids = del_media_ids ? del_media_ids : [];
        if (add_media_ids.length + del_media_ids.length === 0) {
            throw "对收藏夹无修改。请至少提供 add_media_ids 和 del_media_ids 中的其中一个。";
        }
        add_media_ids = add_media_ids.map(value => value.toString());
        del_media_ids = del_media_ids.map(value => value.toString())
        
        this.credential.raise_for_no_sessdata({});
        this.credential.raise_for_no_bili_jct({});

        var api = API.operate.favorite;
        var data = {
            rid: this.get_aid({}), 
            type: 2, 
            "add_media_ids": add_media_ids.join(","), 
            "del_media_ids": del_media_ids.join(","), 
            csrf: this.credential.bili_jct, 
            csrf_token: this.credential.bili_jct
        };
        return await request({
            method: "POST", 
            url: api.url, 
            params: data, 
            credential: this.credential
        });
    }
}
