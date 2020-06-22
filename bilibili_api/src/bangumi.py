from . import exception, utils
from .utils import Verify, Get

headers = utils.default_headers
apis = utils.get_apis()


class BangumiInfo:
    def __init__(self, media_id: int = 0, season_id: int = 0, verify: Verify = Verify()):
        self.info = None
        self.media_id = media_id
        self.season_id = season_id
        self.verify = verify
        # TODO：add get danmuku info

    def get_bangumi_info(self):
        if self.media_id == 0:
            raise exception.bilibiliApiException("请传入media_id")
        api = apis['bangumi']['bangumi_info']
        params = {
            'media_id': self.media_id
        }
        if self.verify.has_sess():
            get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        else:
            get = Get(url=api["url"], params=params)
        self.info = get()
        return self.info

    def get_bangumi_stat(self):
        if self.season_id == 0:
            raise exception.bilibiliApiException('请传入season_id')
        api = apis['bangumi']['bangumi_status']
        params = {
            'season_id': self.season_id
        }
        if self.verify.has_sess():
            get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        else:
            get = Get(url=api["url"], params=params)
        self.info = get()
        return self.info

    def get_bangumi_list(self):
        if self.season_id == 0:
            raise exception.bilibiliApiException('请传入season_id')
        api = apis['bangumi']['bangumi_list']
        params = {
            'season_id': self.season_id
        }
        if self.verify.has_sess():
            get = Get(url=api["url"], params=params, cookies=self.verify.get_cookies())
        else:
            get = Get(url=api["url"], params=params)
        self.info = get()
        return self.info
