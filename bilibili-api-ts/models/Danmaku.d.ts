export declare class Danmaku {
    text: string;
    dm_time: number;
    send_time: number;
    crc32_id: string;
    color: string;
    weight: number;
    id: number;
    id_str: string;
    action: number;
    mode: DmMode | number;
    font_size: DmFontSize | number;
    is_sub: boolean;
    pool: number;
    attr: number;
    constructor({ text, dm_time, send_time, crc32_id, color, weight, id, id_str, action, mode, font_size, is_sub, pool, attr }: {
        text: string;
        dm_time?: number;
        send_time?: number;
        crc32_id?: string;
        color?: string;
        weight?: number;
        id?: number;
        id_str?: string;
        action?: number;
        mode?: DmMode | number;
        font_size?: DmFontSize | number;
        is_sub?: boolean;
        pool?: number;
        attr?: number;
    });
}
export declare enum DmFontSize {
    EXTREME_SMAL = 12,
    SUPER_SMALL = 16,
    SMALL = 18,
    NORMAL = 25,
    BIG = 36,
    SUPER_BIG = 45,
    EXTREME_BIG = 64
}
export declare enum DmMode {
    FLY = 1,
    TOP = 5,
    BOTTOM = 4,
    REVERSE = 6
}
