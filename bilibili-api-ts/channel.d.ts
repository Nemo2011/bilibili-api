import { Credential } from "./models/Credential";
/**
 * 根据 tid 获取频道信息。
 *
 * param tid(number): 频道 tid
 *
 * @returns {Object[Object, Object]} 第一项是主分区，第二项是子分区，没有时返回 None。
 */
export declare function get_channel_info_by_tid({ tid }: {
    tid: number;
}): any[];
/**
 * 根据频道名称获取频道信息。
 *
 * param name(string): 频道的名称
 *
 * @returns {Object[Object, Object]} 第一项是主分区，第二项是子分区，没有时返回 None。
 */
export declare function get_channel_info_by_name({ name }: {
    name: string;
}): any[];
/**
 * 获取分区前十排行榜。
 *
 * param tid(number)                     : 频道的 tid
 *
 * param day(number, optional)           : 3 天排行还是 7 天排行，defaults to 7
 *
 * param credential(Credential, optional): 凭据类
 * @returns
 */
export declare function get_top10({ tid, day, credential }: {
    tid: number;
    day?: number;
    credential?: Credential;
}): Promise<any>;
