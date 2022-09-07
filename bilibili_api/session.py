import asyncio
import datetime
import json
import logging
import os
import time

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .user import get_self_info
from .utils.Credential import Credential
from .utils.network_httpx import request
from .utils.utils import get_api
from .video import Video

API = get_api("session")
    

async def fetch_session_msgs(talker_id: int, credential: Credential, begin_seqno: int = 0):
    """
    获取指定用户的近三十条消息

    Args:
        talker_id   (int)       : 用户 UID
        credential  (Credential): Credential
        begin_seqno (int)       : 起始 Seqno

    Returns:
        调用 API 返回结果
    """

    credential.raise_for_no_sessdata()
    params = {
        'talker_id': talker_id,
        'session_type': 1,
        'begin_seqno': begin_seqno
    }
    api = API["session"]["fetch"]

    return await request("GET", api["url"], params=params,credential=credential)

async def new_sessions(credential: Credential, begin_ts: int = int(time.time()*1000000)):
    """
    获取新消息

    Args:
        credential (Credential): Credential
        begin_ts   (int)       : 起始时间戳

    Returns:
        调用 API 返回结果
    """

    credential.raise_for_no_sessdata()
    params = {'begin_ts': begin_ts}
    api = API["session"]["new"]

    return await request("GET", api["url"], params=params,credential=credential)

async def send_msg(credential: Credential, receiver_id: int, text: str):
    """
    给用户发送私聊信息。目前仅支持纯文本。

    Args:
        text (str): 信息内容。

    Returns:
        dict: 调用接口返回的内容。
    """
    credential.raise_for_no_sessdata()
    credential.raise_for_no_bili_jct()

    api = API["operate"]["send_msg"]
    self_info = await get_self_info(credential)
    sender_uid = self_info["mid"]

    data = {
        "msg[sender_uid]": sender_uid,
        "msg[receiver_id]": receiver_id,
        "msg[receiver_type]": 1,
        "msg[msg_type]": 1,
        "msg[msg_status]": 0,
        "msg[content]": json.dumps({"content": text}),
        "msg[dev_id]": "B9A37BF3-AA9D-4076-A4D3-366AC8C4C5DB",
        "msg[new_face_version]": "0",
        "msg[timestamp]": int(time.time()),
        "from_filework": 0,
        "build": 0,
        "mobi_app": "web",
    }
    return await request(
        "POST", url=api["url"], data=data, credential=credential
    )

class Picture:  # 我老想用 TypedDict 了 但是 TypedDict 太高级了 低版本没有
    height:     int
    imageType:  str
    original:   int
    size:       str
    url:        str
    width:      int

    def __init__(self, kwargs: dict):
        self.__dict__.update(kwargs)
    
    def __str__(self):
        return str(self.__dict__)

    async def download(self, filepath: str = ''):
        if not filepath:
            filepath = self.url.replace('https://message.biliimg.com/bfs/im/', '')
        async with httpx.AsyncClient() as session:
            r = await session.get(self.url)
            with open(filepath, 'wb') as fp:
                fp.write(r.content)

class Event:
    """
    事件参数:
    + receiver_id: 收信人 UID
    + sender_uid:  发送人 UID
    + msg_type:    事件类型
    + msg_key:     事件唯一编号
    + content:     事件内容

    事件类型:
    + TEXT:        纯文字消息
    + PICTURE:     图片消息
    + WITHDRAW:    撤回消息
    + SHARE_VIDEO: 分享视频
    """

    receiver_id: int
    sender_uid:  int
    msg_type:    int
    msg_key:     int
    content:     int | str | Picture | Video

    TEXT = 1
    PICTURE = 2
    WITHDRAW = 5
    SHARE_VIDEO = 7

    def __init__(self, data: dict, self_uid: int):
        """
        信息事件类型:
            data: 接收到的事件详细信息
            self_uid: 用户自身 UID
        """
        self.__dict__.update(data)
        self.uid = self_uid

        self.__content()
    
    def __str__(self):
        if self.receiver_id == self.uid:
            msg_type = '收到'
            user_id = self.sender_uid
        else:
            msg_type = '发送'
            user_id = self.receiver_id
        return f'{msg_type} {user_id} 信息: {self.content}'

    def __content(self):
        '更新消息内容'

        content: dict = json.loads(self.content)

        if self.msg_type == Event.TEXT:
            self.content = content.get('content')

        elif self.msg_type == Event.PICTURE:
            self.content = Picture(content)
        
        elif self.msg_type == Event.SHARE_VIDEO:
            self.content = Video(bvid=content.get('bvid'), aid=content.get('id'))

class Session:
    def __init__(self, credential: Credential, debug=False):
        self.maxSeqno = 0
        self.maxTs = int(time.time()*1000000)
        self.credential = credential
        self.__status = 0
        self.sched = AsyncIOScheduler(timezone="Asia/Shanghai")
        self.events = dict()

        # logging
        self.logger = logging.getLogger("Session")
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)s]: %(message)s", '%Y-%m-%d %H:%M:%S'))
            self.logger.addHandler(handler)        

    def get_status(self):
        """
        获取连接状态
        Returns:
            int: 0 初始化，1 已连接，2 断开连接中，3 已断开，4 错误
        """
        return self.__status

    async def run(self):
        self_info = await get_self_info(self.credential)
        self.uid = self_info["mid"]

        # 间隔 3 秒轮询消息列表
        @self.sched.scheduled_job('interval', seconds=3, max_instances=3, next_run_time=datetime.datetime.now())
        async def qurey():
            js = await new_sessions(self.credential, self.maxTs)
            if js.get('session_list') is None:
                return

            pending = set()
            for session in js['session_list']:
                self.maxTs = max(self.maxTs, session['session_ts'])
                self.logger.info(f"获取到 UID: {session['talker_id']} 最新消息 {session['last_msg']}")
                pending.add(
                    asyncio.create_task(
                        fetch_session_msgs(session['talker_id'], self.credential, self.maxSeqno)
                    )
                )

            while pending:
                done, pending = await asyncio.wait(pending)
                for done_task in done:
                    js = await done_task
                    if js['messages']:
                        self.maxSeqno = max(self.maxSeqno, js['messages'][0]['msg_seqno'])
                    for message in js.get('messages', [])[::-1]:
                        event = Event(message, self.uid)
                        if event.msg_type == Event.WITHDRAW:
                            print(self.events.get(str(event.content)), '被撤回')
                        elif event.msg_type == Event.PICTURE:
                            await event.content.download()
                        else:
                            print(event)
                        self.events.update({str(event.msg_key): event})

            self.logger.debug(f'maxTs = {self.maxTs}')

        self.sched.start()

    async def start(self):
        await self.run()
        while self.get_status() < 2:
            await asyncio.sleep(1)
        
        if self.get_status() == 2:
            self.__status = 3

    async def close(self):
        self.__status = 2
