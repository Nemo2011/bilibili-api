export class Danmaku {
    text: string
    dm_time: number
    send_time: number
    crc32_id: string
    color: string
    weight: number
    id: number
    id_str: string
    action: number
    mode: DmMode|number
    font_size: DmFontSize|number
    is_sub: boolean
    pool: number
    attr: number

    constructor (config: any) {
        var text: string = config.text,
            dm_time: number = config.dm_time ? config.dm_time : 0,
            send_time: number = config.send_time ? config.send_time : 0,
            crc32_id: string = config.crc32_id ? config.crc32_id : "",
            color: string = config.color ? config.color : "", 
            weight: number = config.weight ? config.weight : -1, 
            id: number = config.id_ ? config.id_ : -1,
            id_str: string = config.id_str ? config.id_str : "", 
            action: number = config.action ? config.action : "", 
            mode: DmMode|number = config.mode ? config.mode : DmMode.FLY,
            font_size: DmFontSize|number = config.font_size ? config.font_size : DmFontSize.NORMAL,
            is_sub: boolean = config.is_sub ? config.is_sub : false, 
            pool: number = config.pool ? config.pool : 0,
            attr: number = config.attr ? config.attr : -1;
        this.text = text;
        this.dm_time = dm_time;
        this.send_time = send_time;
        this.crc32_id = crc32_id;
        this.color = color;
        this.weight = weight;
        this.id = id;
        this.id_str = id_str; 
        this.action = action;
        this.mode = mode;
        this.font_size = font_size;
        this.is_sub = is_sub;
        this.pool = pool;
        this.attr = attr;
    }

    
}

export enum DmFontSize {
    EXTREME_SMAL = 12,
    SUPER_SMALL = 16,
    SMALL = 18,
    NORMAL = 25,
    BIG = 36,
    SUPER_BIG = 45,
    EXTREME_BIG = 64
}

export enum DmMode {
    FLY = 1,
    TOP = 5, 
    BOTTOM = 4,
    REVERSE = 6
}
