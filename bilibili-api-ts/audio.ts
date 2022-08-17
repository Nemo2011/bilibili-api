import {AudioData} from "./apis/audio";
import {Credential} from "./models/Credential";
import {request} from "./utils/network";

const API = AudioData;

/**
 * 音频相关
 */
export class Audio {
    auid: number
    credential: Credential

    /**
     * param auid(int)                       : 音频 AU 号
     * 
     * param credential(Credential, optional): 凭据. Defaults to None
     */
    constructor({auid, credential}: {
        auid: number, 
        credential?: Credential
    }) {
        this.credential = credential ? credential : new Credential({});
        this.auid = auid;
    }

    /**
     * 获取 auid
     * 
     * @returns 
     */
    get_auid({}) {
        return this.auid;
    }

    /**
     * 获取音频信息
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_info({}) {
        var api = API.audio_info.info;
        var params = {
            sid: this.auid
        };
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }

    /**
     * 获取音频 tags
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_tags({}) {
        var api = API.audio_info.tag;
        var params = {
            sid: this.auid
        };
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }

    /**
     * 获取音频下载链接
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_download_url({}) {
        var api = API.audio_info.download_url;
        var params = {
            sid: this.auid, 
            privilege: 2, 
            quality: 2
        }
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }
}

export class AudioList {
    amid: number
    credential: Credential

    /**
     * param amid(number)                    : 歌单 ID
     * 
     * param credential(Credential, optional): 凭据。
     */
    constructor({amid, credential}: {amid: number, credential: Credential}) {
        if (credential === null || credential === undefined) credential = new Credential({});
        this.credential = credential;
        this.amid = amid;
    }

    /**
     * 获取歌单信息
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_info({}) {
        var api = API.list_info.info;
        var params = {
            sid: this.amid
        };
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }

    /**
     * 获取歌单 tags
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_tags({}) {
        var api = API.list_info.tag;
        var params = {
            sid: this.amid
        };
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }

    /**
     * 获取歌单歌曲列表
     * 
     * param pn(number, optional): 页码,defaults to 1
     * 
     * @returns {Object} 调用 API 返回的结果
     */
    async get_song_list({
        pn
    }: {
        pn: number
    }) {
        if (pn === null || pn === undefined) pn = 1;

        var api = API.list_info.song_list;
        var params = {
            sid: this.amid, 
            pn: pn, 
            ps: 100
        }
        return await request({
            method: "GET", 
            url: api.url, 
            params: params, 
            credential: this.credential
        });
    }
}
