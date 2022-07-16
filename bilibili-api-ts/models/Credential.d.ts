export declare class Credential {
    sessdata: string | null;
    bili_jct: string | null;
    dedeuserid: string | null;
    constructor(config?: any | null);
    raise_for_no_sessdata(): void;
    raise_for_no_bili_jct(): void;
    raise_for_no_dedeuserid(): void;
    get_cookies(): {
        SESSDATA: string;
        bili_jct: string;
        DedeUserID: string;
    };
}
