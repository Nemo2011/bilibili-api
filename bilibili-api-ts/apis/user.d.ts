export declare const UserAPIData: {
    info: {
        my_info: {
            url: string;
            method: string;
            verify: boolean;
            comment: string;
        };
        info: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                mid: string;
            };
            comment: string;
        };
        relation: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                vmid: string;
            };
            comment: string;
        };
        upstat: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                mid: string;
            };
            comment: string;
        };
        live: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                mid: string;
            };
            comment: string;
        };
        video: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                mid: string;
                ps: string;
                tid: string;
                pn: string;
                keyword: string;
                order: string;
            };
            comment: string;
        };
        audio: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                uid: string;
                ps: string;
                pn: string;
                order: string;
            };
            comment: string;
        };
        article: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                mid: string;
                ps: string;
                pn: string;
                sort: string;
            };
            comment: string;
        };
        article_lists: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                mid: string;
                sort: string;
            };
            comment: string;
        };
        dynamic: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                host_uid: string;
                offset_dynamic_id: string;
                need_top: string;
            };
            comment: string;
        };
        bangumi: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                vmid: string;
                pn: string;
                ps: string;
                type: string;
            };
            comment: string;
        };
        followings: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                vmid: string;
                ps: string;
                pn: string;
                order: string;
            };
            comment: string;
        };
        followers: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                vmid: string;
                ps: string;
                pn: string;
                order: string;
            };
            comment: string;
        };
        overview: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                mid: string;
                jsonp: string;
            };
            comment: string;
        };
        self_subscribe_group: {
            url: string;
            method: string;
            verify: boolean;
            params: {};
            comment: string;
        };
        get_user_in_which_subscribe_groups: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                fid: string;
            };
            comment: string;
        };
        history: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                pn: string;
                ps: string;
            };
            comment: string;
        };
        channel_list: {
            url: string;
            method: string;
            verity: boolean;
            params: {
                mid: string;
                page_num: string;
                page_size: string;
            };
            comment: string;
        };
        channel_video_series: {
            url: string;
            method: string;
            verity: boolean;
            params: {
                mid: string;
                series_id: string;
                pn: string;
                ps: string;
            };
            comment: string;
        };
        channel_video_season: {
            url: string;
            method: string;
            verity: boolean;
            params: {
                mid: string;
                season_id: string;
                sort_reverse: string;
                page_num: string;
                page_size: string;
            };
            comment: string;
        };
        pugv: {
            url: string;
            method: string;
            verity: boolean;
            params: {
                mid: string;
            };
            comment: string;
        };
        get_coins: {
            url: string;
            method: string;
            verify: boolean;
            comment: string;
        };
    };
    operate: {
        modify: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                fid: string;
                act: string;
                re_src: string;
            };
            comment: string;
        };
        send_msg: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                "msg[sender_uid]": string;
                "msg[receiver_id]": string;
                "msg[receiver_type]": string;
                "msg[msg_type]": string;
                "msg[msg_status]": string;
                "msg[content]": {
                    content: string;
                };
            };
            comment: string;
        };
        del_channel_aids_series: {
            url: string;
            method: string;
            verity: boolean;
            params: {
                mid: string;
                series_id: string;
                aids: string;
            };
        };
        del_channel_series: {
            url: string;
            method: string;
            verity: boolean;
            query: {
                mid: string;
                series_id: string;
                aids: string;
                csrf: string;
            };
        };
        create_subscribe_group: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                tag: string;
            };
            comment: string;
        };
        del_subscribe_group: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                tagid: string;
            };
            comment: string;
        };
        rename_subscribe_group: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                tagid: string;
                name: string;
            };
            comment: string;
        };
        set_user_subscribe_group: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                fids: string;
                tagids: string;
            };
            comment: string;
        };
    };
};
