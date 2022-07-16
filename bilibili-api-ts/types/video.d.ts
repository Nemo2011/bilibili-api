import { Credential } from "./models/Credential";
export declare class Video {
    __info: Record<any, any> | null;
    __bvid: string;
    __aid: number;
    credential: Credential;
    constructor(config: any);
    set_bvid(config: any): void;
    get_bvid(): string;
    set_aid(config: any): void;
    get_aid(): number;
    get_info(): Promise<any>;
    __get_info_cached(): Promise<any>;
    get_stat(): Promise<any>;
    get_tags(): Promise<any>;
    get_chargers(): Promise<any>;
    get_pages(): Promise<any>;
    __get_page_id_by_index(page_index: number): Promise<any>;
    get_cid(config: any): Promise<any>;
    get_download_url(config: any): Promise<any>;
}
