import { CookieJar } from 'tough-cookie';
import * as crypto from 'crypto';
import axios, { AxiosInstance } from 'axios';
import { wrapper } from 'axios-cookiejar-support';
import { Credential } from '../models/Credential';
import { Proxy } from '../models/Proxy';

const cookieJar = new CookieJar();

var sess: any = null;
var user_proxy: Proxy|null = null;

async function getAxiosInstance({credential=new Credential({}), proxy=null}: {credential?: Credential, proxy?: Proxy|null}) {
  if (credential.sessdata !== null) {
    cookieJar.setCookieSync(
      `SESSDATA=${credential.sessdata}; Domain=.bilibili.com`, 
      'https://www.bilibili.com'
    );
  }
  if (credential.bili_jct !== null) {
    cookieJar.setCookieSync(
      `bili_jct=${credential.bili_jct} Domain=.bilibili.com`, 
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
     'https://www.bilibili.com'
  );
  // console.log(cookieJar.getCookieString("https://api.bilibili.com"));
  sess = wrapper(
    axios.create({
      headers: {
        'user-agent': 'Mozilla/5.0',
        referer: 'https://www.bilibili.com/',
      },
      // withCredentials: true, 
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

async function setAxiosInstance(axios: AxiosInstance) {
  sess = axios;
}

export async function get_session({credential=new Credential({})}: {credential: Credential}) {
  if (credential === null || credential === undefined) {
    credential = new Credential({});
  }
  if (user_proxy !== null) {
    return await getAxiosInstance({credential: credential, proxy: user_proxy});
  }
  else {
    return await getAxiosInstance({credential: credential});
  }
}


export async function request(
  {
    method, url, params={}, data={}, credential=new Credential({}), no_csrf=false
  } : 
  {
    method: string, 
    url: string,
    params?: any, 
    data?: any, 
    credential?: Credential|null, 
    no_csrf?: boolean
  }
) {
  if (no_csrf === null || no_csrf === undefined) {
    no_csrf = false;
  }

  if (credential === null || credential === undefined) {
    credential = new Credential({});
  }

  method = method.toUpperCase();

  if (method !== "GET" && !no_csrf){
    credential.raise_for_no_bili_jct({})
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

  if (params === null) {
    params = {};
  }

  if (params['jsonp'] !== undefined) {
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

  // console.log(credential.get_cookies());

  if (user_proxy !== null) {
    await getAxiosInstance({credential: credential, proxy: user_proxy});
  }
  else {
    await getAxiosInstance({credential: credential});
  }
  var resp = await (await sess).request(config);

  // console.log(resp)

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
  if (code === null || code === undefined) {
    throw "API 返回数据未含 code 字段";
  }
  if (code !== 0) {
    var msg = resp_data['message'];
    if (msg === undefined) {
      msg = "接口未返回错误信息";
    }
    throw code + msg;
  }

  var real_data = resp_data['data'];
  if (real_data === undefined) {
    real_data = resp_data['result'];
  }
  return real_data;
}

export function set_proxy(config: any){
  user_proxy = config.proxy;
}
