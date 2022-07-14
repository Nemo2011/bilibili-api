import {VideoData} from "../apis/video"

export function get_api(api: string){
    switch (api) {
        case "video": return VideoData;break;
    }
    return {};
}
