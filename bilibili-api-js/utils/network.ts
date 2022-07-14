import { CookieJar } from 'tough-cookie';
import { getSystemProxy } from 'os-proxy-config';
import * as crypto from 'crypto';
import axios, { AxiosInstance } from 'axios';
import { wrapper } from 'axios-cookiejar-support';
import { Credential } from '../models/Credential';
import { Proxy } from '../models/Proxy';

export const cookieJar = new CookieJar();

var sess: any = null;
var user_proxy: Proxy|null = null;

export async function getAxiosInstance(credential: Credential=new Credential(), proxy: any|Proxy=null) {
  if (credential.sessdata !== null) {
    cookieJar.setCookieSync(
      `sessdata=${credential.sessdata}; Domain=.bilibili.com`, 
      'https://www.bilibili.com'
    );
  }
  if (credential.bili_jct !== null) {
    cookieJar.setCookieSync(
      `bili_jct=${credential.bili_jct}; Domain=.bilibili.com`, 
      'https://www.bilibili.com'
    );
  }
  if (credential.dedeuserid !== null) {
    cookieJar.setCookieSync(
      `DedeUserID=${credential.dedeuserid}; Domain=.bilibili.com`, 
      'https://www.bilibili.com'
    );
  }
  cookieJar.setCookieSync(
    `buvid3=${crypto.randomUUID()}; Domain=.bilibili.com`,
    'https://www.bilibili.com/'
  );

  sess = wrapper(
    axios.create({
      headers: {
        'user-agent': 'Mozilla/5.0',
        referer: 'https://www.bilibili.com/',
      },
      jar: cookieJar,
      responseType: 'json',
      proxy: proxy
        ? {
          host: proxy.hostname,
          port: parseInt(proxy.port),
          auth:
              proxy.username && proxy.password
                ? {
                  username: proxy.username,
                  password: proxy.password,
                }
                : undefined,
        }
        : false,
    }));

    return sess;
};

export async function setAxiosInstance(axios: AxiosInstance) {
  sess = axios;
}

export async function request(
  method: string,
  url: string, 
  params: any={},
  data: any={},
  credential: Credential=new Credential(), 
  no_csrf: boolean=false
) {
  method = method.toUpperCase();

  if (method !== "GET" && !no_csrf){
    credential.raise_for_no_bili_jct()
  }

  const DEFAULT_HEADERS = {
    "Referer": "https://www.bilibili.com",
    "User-Agent": "Mozilla/5.0",
  };
  var headers = DEFAULT_HEADERS;

  if (!no_csrf && method in ["POST", "DELETE", "PATCH"]){
    if (data === null){
      data = {};
    }
    data["csrf"] = credential.bili_jct;
    data["csrf_token"] = credential.bili_jct;
  }

  var jsonp = params['jsonp'] ? true : false;
  if (jsonp) {
    params["callback"] = "callback"
  }

  var cookies = credential.get_cookies();

  var config: Record<string, any> = {
    "method": method, 
    "url": url, 
    "params": params, 
    "data": data, 
    "headers": headers, 
    "cookies": cookies
  }

  if (user_proxy !== null) {
    await getAxiosInstance(credential, user_proxy);
  }
  else {
    await getAxiosInstance(credential);
  }

  var resp = await (await sess).request(config);

  // console.log(resp.headers)

  var has_content_type = resp.headers['content-type'] ? true : false;
  if (!has_content_type) return;
  if (resp.headers['content-type'].toLowerCase().indexOf("application/json") === -1){
    throw "响应不是 application/json 类型";
  }

  var resp_data = resp['data'];
  // console.log(resp_data);
  // console.log(JSON.stringify(raw_data))
  var code = resp_data['code'];
  if (code === null) {
    throw "API 返回数据未含 code 字段";
  }
  if (code !== 0) {
    var msg = resp_data['message'];
    if (msg === undefined) {
      msg = "接口未返回错误信息";
    }
    throw msg;
  }

  var real_data = resp_data['data'];
  if (real_data === undefined) {
    real_data = resp_data['result'];
  }
  return real_data;
}

export function setProxy(proxy: Proxy){
  user_proxy = proxy;
}
