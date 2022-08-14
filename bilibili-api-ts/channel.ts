import {ChannelData} from "./data/channel";
import {ChannelData as ChannelAPIData} from "./apis/channel";
import {Credential} from "./models/Credential";
import {request} from "./utils/network";

/**
 * 根据 tid 获取频道信息。
 * 
 * param tid(number): 频道 tid
 * 
 * @returns {Object[Object, Object]} 第一项是主分区，第二项是子分区，没有时返回 None。
 */
export function get_channel_info_by_tid({tid}: {tid: number}) {
    for (let channel of ChannelData) {
        if (channel.tid ? false : true) {
            continue;
        }

        if (tid === Number(channel.tid)) {
            return [channel, null]
        }

        for (let sub_channel of channel.sub) {
            if (sub_channel.tid ? false : true) {
                continue;
            }

            if (tid === Number(sub_channel.tid)) {
                return [channel, sub_channel];
            }
        }
    }

    return [null, null]
}

/**
 * 根据频道名称获取频道信息。
 * 
 * param name(string): 频道的名称
 * 
 * @returns {Object[Object, Object]} 第一项是主分区，第二项是子分区，没有时返回 None。
 */
export function get_channel_info_by_name({name}:{name: string}) {
    for (let main_ch of ChannelData) {
        if (main_ch.name.indexOf(name) !== -1) {
            return [main_ch, null];
        }

        for (let sub_ch of main_ch.sub) {
            if (sub_ch.name.indexOf(name) !== -1) {
                return [main_ch, sub_ch]
            }
        }
    }
}

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
export async function get_top10({tid, day, credential}: {tid: number, day?: number, credential?: Credential}) {
    if (credential === null || credential === undefined) {
        credential = new Credential({});
    }
    if (day === null || day === undefined) {
        day = 7;
    }
    if (day !== 3 && day !== 7) {
        throw "参数 day 只能是 3，7。";
    }

    var api = ChannelAPIData.ranking.get_top10;
    var params = {
        rid: tid, 
        day: day
    };
    return await request({
        method: "GET", 
        url: api.url,
        params: params, 
        credential: credential
    });
}

/**
 * 获取所有分区的数据
 * 
 * @returns {any[]} 所有分区的数据
 */
export function get_channel_list({}) {
    var channel_list = [];
    for (let channel_big of ChannelData) {
        var channel_big_copy = JSON.parse(JSON.stringify(channel_big));
        delete channel_big_copy['sub'];
        channel_list.push(channel_big_copy);
        for (let channel_sub of channel_big.sub) {
            var channel_sub_copy = JSON.parse(JSON.stringify(channel_sub));
            channel_sub_copy['father'] = channel_big_copy;
            channel_list.push(channel_sub_copy);
        }
    }
    return channel_list;
}

/**
 * 获取所有分区的数据
 * 含父子关系（即一层次只有主分区）
 * 
 * @returns {Object} 所有主分区的数据
 */
export function get_channel_list_sub({}) {
    return ChannelData;
}
