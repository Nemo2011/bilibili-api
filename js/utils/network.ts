import { CookieJar } from 'tough-cookie';
import { getSystemProxy } from 'os-proxy-config';
import crypto from 'crypto';
import axios from 'axios';
import { wrapper } from 'axios-cookiejar-support';
import { CookiesCredential } from '../models/Credential';
import { Proxy } from '../models/Proxy';

export const cookieJar = new CookieJar();

export async function getAxiosInstance(credential: CookiesCredential=new CookiesCredential(), proxy: any|Proxy=null) {
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

  return wrapper(
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
    })
  );
};
