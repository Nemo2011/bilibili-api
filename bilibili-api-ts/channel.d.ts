import { Credential } from "./models/Credential";
export declare function get_channel_info_by_tid({ tid }: {
    tid: number;
}): any[];
export declare function get_channel_info_by_name({ name }: {
    name: string;
}): any[];
export declare function get_top10({ tid, day, credential }: {
    tid: number;
    day?: number;
    credential?: Credential;
}): Promise<any>;
