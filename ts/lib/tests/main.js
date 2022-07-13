"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const network_1 = require("../utils/network");
const axios = (0, network_1.getAxiosInstance)();
var func = {
    async getInfo() {
        return (await (await axios).get("https://api.bilibili.com/x/web-interface/view", {
            params: {
                bvid: "BV19U4y1V7MV"
            }
        })).data;
    }
};
var print = async function () {
    console.log((await func.getInfo())['data']);
};
print();
