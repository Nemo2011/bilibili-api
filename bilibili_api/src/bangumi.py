from . import exception, utils
import requests
import json
from xml.dom.minidom import parseString
import math
from .utils import Danmaku, Verify, Get, Post
import re

headers = utils.default_headers
apis = utils.get_apis()


class bangumiInfo():
    def __init__(self,mid: str = "",sid: str = "",verify: Verify = Verify()):
        self.info = None
        self.media_id = mid
        self.season_id = sid
        self.verify = verify
        # TODO：add get danmuku info

    def get_bangumi_info(self):
        if self.media_id == "":
            raise exception.bilibiliApiException("请传入media_id")
        api = apis['bangumi']['bangumi_info']
        params = {
            'media_id':self.media_id
        }
        if self.verify.has_sess():
            get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        else:
            get = Get(url=api["url"], params=params)
        self.info = get()
        return self.info
    def get_bangumi_stat(self):
        if self.season_id == "":
            raise exception.bilibiliApiException('请自行设置season_id')
        api = apis['bangumi']['bangumi_status']
        params = {
            'season_id':self.season_id
        }
        if self.verify.has_sess():
            get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        else:
            get = Get(url=api["url"], params=params)
        self.info = get()
        return self.info
    def get_bangumi_list(self):
        if self.season_id == "":
            raise exception.bilibiliApiException('请自行设置season_id')
        api = apis['bangumi']['bangumi_list']
        params = {
            'season_id':self.season_id
        }
        if self.verify.has_sess():
            get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        else:
            get = Get(url=api["url"], params=params)
        self.info = get()
        return self.info
        pass