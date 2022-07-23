import { Credential } from '../models/Credential';
export declare function get_session({ credential }: {
    credential: Credential;
}): Promise<any>;
export declare function request({ method, url, params, data, credential, no_csrf }: {
    method: string;
    url: string;
    params?: any;
    data?: any;
    credential?: Credential | null;
    no_csrf?: boolean;
}): Promise<any>;
export declare function set_proxy(config: any): void;
