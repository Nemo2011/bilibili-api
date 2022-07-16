export declare var VideoData: {
    info: {
        stat: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                aid: string;
            };
            comment: string;
        };
        detail: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                aid: string;
            };
            comment: string;
        };
        tags: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                aid: string;
            };
            comment: string;
        };
        chargers: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                aid: string;
                mid: string;
            };
            comment: string;
        };
        pages: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                aid: string;
            };
            comment: string;
        };
        playurl: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                avid: string;
                cid: string;
                qn: string;
                otype: string;
                fnval: string;
                platform: string;
            };
            comment: string;
        };
        related: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                aid: string;
            };
            comment: string;
        };
        has_liked: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                aid: string;
            };
            comment: string;
        };
        get_pay_coins: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                aid: string;
            };
            comment: string;
        };
        has_favoured: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                aid: string;
            };
            comment: string;
        };
        media_list: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                rid: string;
                up_mid: string;
                type: string;
            };
            comment: string;
        };
        pbp: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                cid: string;
                bvid: string;
                aid: string;
            };
        };
    };
    operate: {
        like: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                aid: string;
                like: string;
            };
            comment: string;
        };
        coin: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                aid: string;
                multiply: string;
                select_like: string;
            };
            comment: string;
        };
        add_tag: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                aid: string;
                tag_name: string;
            };
            comment: string;
        };
        del_tag: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                aid: string;
                tag_id: string;
            };
            comment: string;
        };
        subscribe_tag: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                tag_id: string;
            };
            comment: string;
        };
        unsubscribe_tag: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                tag_id: string;
            };
            comment: string;
        };
        favorite: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                rid: string;
                type: string;
                add_media_ids: string;
                del_media_ids: string;
            };
            comment: string;
        };
        submit_subtitle: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                type: number;
                oid: string;
                lan: string;
                data: {
                    font_size: string;
                    font_color: string;
                    background_alpha: string;
                    background_color: string;
                    Stroke: string;
                    body: {
                        from: string;
                        to: string;
                        location: string;
                        content: string;
                    }[];
                };
                submit: string;
                sign: string;
                bvid: string;
            };
            comment: string;
        };
    };
    danmaku: {
        get_danmaku: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                oid: string;
                type: string;
                segment_index: string;
                pid: string;
            };
            comment: string;
        };
        get_history_danmaku: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                oid: string;
                type: string;
                date: string;
            };
            comment: string;
        };
        view: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                type: number;
                oid: string;
                pid: string;
            };
            comment: string;
        };
        get_history_danmaku_index: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                oid: string;
                type: string;
                month: string;
            };
            comment: string;
        };
        has_liked_danmaku: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                oid: string;
                ids: string;
            };
            comment: string;
        };
        send_danmaku: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                type: string;
                oid: string;
                msg: string;
                bvid: string;
                progress: string;
                color: string;
                fontsize: string;
                pool: string;
                mode: string;
                plat: string;
            };
            comment: string;
        };
        like_danmaku: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                dmid: string;
                oid: string;
                op: string;
                platform: string;
            };
            comment: string;
        };
        edit_danmaku: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                type: string;
                dmids: string;
                oid: string;
                state: string;
            };
            comment: string;
        };
        snapshot: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                aid: string;
            };
            comment: string;
        };
        recall: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                dmid: string;
                cid: string;
                csrf: string;
            };
            comment: string;
        };
    };
};
