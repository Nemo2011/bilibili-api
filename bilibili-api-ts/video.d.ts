import { Credential } from "./models/Credential";
export declare class Video {
    __info: Record<any, any> | null;
    __bvid: string;
    __aid: number;
    credential: Credential;
    /**
     * param bvid(int)              Bvid(可选)
     *
     * param aid(int)               Aid(可选)
     *
     * param credential(Credential) 凭据类(可选)
     */
    constructor({ bvid, aid, credential }: {
        bvid?: string | null;
        aid?: number | null;
        credential?: Credential;
    });
    /**
     * 设置 bvid
     *
     * param bvid(string) Bvid
     */
    set_bvid({ bvid }: {
        bvid: string;
    }): void;
    /**
     * 获取 bvid
     *
     * @returns Bvid
     */
    get_bvid({}: {}): string;
    /**
     * 设置 aid
     *
     * param aid(number) Aid
     */
    set_aid({ aid }: {
        aid: number;
    }): void;
    /**
     * 获取 aid
     *
     * @returns aid
     */
    get_aid({}: {}): number;
    /**
     * 获取视频详细信息
     *
     * @returns 调用 API 返回的结果
     */
    get_info({}: {}): Promise<any>;
    /**
     * 获取视频详细信息的内存中的缓存数据
     *
     * @returns 调用 API 返回的结果
     */
    __get_info_cached({}: {}): Promise<any>;
    /**
     * 获取视频统计数据
     *
     * @returns 调用 API 返回的结果
     */
    get_stat({}: {}): Promise<any>;
    /**
     * 获取视频标签
     *
     * @returns 调用 API 返回的结果
     */
    get_tags({}: {}): Promise<any>;
    /**
     * 获取视频充电信息
     *
     * @returns 调用 API 返回的结果
     */
    get_chargers(): Promise<any>;
    /**
     * 获取视频分 P 信息
     *
     * @returns 调用 API 返回的结果
     */
    get_pages({}: {}): Promise<any>;
    /**
     * 获取分 P 对应的 cid
     *
     * param page_index(int) 分 P 序号
     *
     * @returns number: cid
     */
    __get_page_id_by_index(page_index: number): Promise<any>;
    /**
     * 获取分 P 对应的 cid
     *
     * param page_index(number) 分 P 序号
     *
     * @returns number: cid
     */
    get_cid({ page_index }: {
        page_index?: number;
    }): Promise<any>;
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
    get_download_url({ page_index, cid, html5 }: {
        page_index?: number | null;
        cid?: number | null;
        html5?: boolean;
    }): Promise<any>;
}
