import { getConstantValue } from "typescript";
import { request } from "../utils/network"

export async function test_request() {
    return await request(
        "GET", 
        "https://api.bilibili.com/x/web-interface/archive/stat", 
        {
            aid: 2
        }
    )
}