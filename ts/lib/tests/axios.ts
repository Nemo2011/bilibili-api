import { getConstantValue } from "typescript";
import { getAxiosInstance } from "../utils/network"

const axios = getAxiosInstance();

var func = {
    async getInfo(): Promise<any> {
        return (await (await axios).get(
            "https://api.bilibili.com/x/web-interface/view", 
            {
                params: {
                    bvid: "BV19U4y1V7MV"
                }
            }
        )).data as any;
    }
}

export var request = async function() {
    var data = (await func.getInfo())['data'];
}
