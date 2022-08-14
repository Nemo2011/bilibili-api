export declare const AudioData: {
    audio_info: {
        info: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                sid: string;
            };
            comment: string;
        };
        tag: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                sid: string;
            };
            comment: string;
        };
        user: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                uid: string;
            };
            comment: string;
        };
        download_url: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                sid: string;
                privilege: string;
                quality: string;
            };
            comment: string;
        };
    };
    audio_operate: {
        coin: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                sid: string;
                multiply: string;
            };
            comment: string;
        };
    };
    list_info: {
        info: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                sid: string;
            };
            comment: string;
        };
        tag: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                sid: string;
            };
            comment: string;
        };
        song_list: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                sid: string;
                pn: string;
                ps: string;
            };
            comment: string;
        };
    };
    list_operate: {
        set_favorite: {
            url: string;
            method: string;
            verify: boolean;
            data: {
                sid: string;
            };
            comment: string;
        };
        del_favorite: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                sid: string;
            };
            data: {
                csrf: string;
            };
            comment: string;
        };
    };
};
