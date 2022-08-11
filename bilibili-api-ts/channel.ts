import {ChannelData} from "./data/channel";

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