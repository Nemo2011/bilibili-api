import { Credential } from "./models/Credential";
/**
 * 音频相关
 */
export declare class Audio {
    auid: number;
    credential: Credential;
    /**
     * param auid(int)                       : 音频 AU 号
     *
     * param credential(Credential, optional): 凭据. Defaults to None
     */
    constructor({ auid, credential }: {
        auid: number;
        credential?: Credential;
    });
    /**
     * 获取 auid
     *
     * @returns
     */
    get_auid({}: {}): number;
    /**
     * 获取音频信息
     *
     * @returns {Object} 调用 API 返回的结果
     */
    get_info({}: {}): Promise<any>;
    /**
     * 获取音频 tags
     *
     * @returns {Object} 调用 API 返回的结果
     */
    get_tags({}: {}): Promise<any>;
    /**
     * 获取音频下载链接
     *
     * @returns {Object} 调用 API 返回的结果
     */
    get_download_url({}: {}): Promise<any>;
}
