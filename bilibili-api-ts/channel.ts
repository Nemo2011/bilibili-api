import {ChannelData} from "./data/channel";
import {ChannelData as ChannelAPIData} from "./apis/channel";
import {Credential} from "./models/Credential";
import {request} from "./utils/network";

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
