import asyncio
import datetime
import enum
import json
import logging
import time
from dataclasses import dataclass
from typing import Union

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .user import get_self_info
from .utils.AsyncEvent import AsyncEvent
from .utils.Credential import Credential
from .utils.network_httpx import request
from .utils.utils import get_api
from .video import Video

API = get_api("session")

# 消息类型
SESSION_TYPE = {1: "私聊", 2: "通知", 3: "应援团", 4: "全部"}


async def fetch_session_msgs(
    talker_id: int, credential: Credential, begin_seqno: int = 0
):
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
    params = {"talker_id": talker_id, "session_type": 1, "begin_seqno": begin_seqno}
    api = API["session"]["fetch"]

    return await request("GET", api["url"], params=params, credential=credential)


async def new_sessions(
    credential: Credential, begin_ts: int = int(time.time() * 1000000)
):
    """
    获取新消息

    Args:
        credential (Credential): Credential
        begin_ts   (int)       : 起始时间戳

    Returns:
        调用 API 返回结果
    """

    credential.raise_for_no_sessdata()
    params = {"begin_ts": begin_ts}
    api = API["session"]["new"]

    return await request("GET", api["url"], params=params, credential=credential)


async def get_sessions(credential: Credential, session_type: int = 4):
    """
    获取已有消息

    Args:
        credential   (Credential): Credential
        session_type (int)       : 会话类型 1: 私聊, 2: 通知, 3: 应援团, 4: 全部

    Returns:
        调用 API 返回结果
    """

    credential.raise_for_no_sessdata()
    params = {
        "session_type": session_type,
        "group_fold": 1,
        "unfollow_fold": 0,
        "sort_rule": 2,
        "build": 0,
        "mobi_app": "web",
    }
    api = API["session"]["get"]

    return await request("GET", api["url"], params=params, credential=credential)


async def send_msg(credential: Credential, receiver_id: int, text: str):
    """
    给用户发送私聊信息。目前仅支持纯文本。

    Args:
        credential (Credential): 凭证
        receiver_id (int): 接收者 UID
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
    return await request("POST", url=api["url"], data=data, credential=credential)


class Picture:
    height: int
    imageType: str
    original: int
    size: str
    url: str
    width: int

    async def download(self, filepath: str = ""):
        if not filepath:
            filepath = self.url.replace("https://message.biliimg.com/bfs/im/", "")
        async with httpx.AsyncClient() as session:
            r = await session.get(self.url)
            with open(filepath, "wb") as fp:
                fp.write(r.content)


class Event:
    """
    事件参数:
    + receiver_id:   收信人 UID
    + receiver_type: 收信人类型，1: 私聊, 2: 应援团通知, 3: 应援团
    + sender_uid:    发送人 UID
    + talker_id:     对话人 UID
    + msg_seqno:     事件 Seqno
    + msg_type:      事件类型
    + msg_key:       事件唯一编号
    + timestamp:     事件时间戳
    + content:       事件内容

    事件类型:
    + TEXT:           纯文字消息
    + PICTURE:        图片消息
    + WITHDRAW:       撤回消息
    + GROUPS_PICTURE: 应援团图片
    + SHARE_VIDEO:    分享视频
    + NOTICE:         系统通知
    + PUSHED_VIDEO:   UP主推送的视频
    + WELCOME:        新成员加入应援团欢迎
    """

    receiver_id: int
    receiver_type: int
    sender_uid: int
    talker_id: int
    msg_seqno: int
    msg_type: int
    msg_key: int
    timestamp: int
    content: Union[str, int, Picture, Video]

    TEXT = "1"
    PICTURE = "2"
    WITHDRAW = "5"
    GROUPS_PICTURE = "6"
    SHARE_VIDEO = "7"
    NOTICE = "10"
    PUSHED_VIDEO = "11"
    WELCOME = "306"

    def __init__(self, data: dict, self_uid: int):
        """
        信息事件类型:
            data: 接收到的事件详细信息
            self_uid: 用户自身 UID
        """
        self.__dict__.update(data)
        self.uid = self_uid

        try:
            self.__content()
        except AttributeError:
            print(data)

    def __str__(self):
        if self.receiver_type == 1:
            if self.receiver_id == self.uid:
                msg_type = "收到"
                user_id = self.sender_uid
            elif self.sender_uid == self.uid:
                msg_type = "发送"
                user_id = self.receiver_id

        elif self.receiver_type == 2:
            user_id = self.receiver_id
            if self.sender_uid == self.uid:
                msg_type = "发送应援团"
            elif self.sender_uid == 0:
                msg_type = "系统提示"
            else:
                msg_type = "收到应援团"

        return f"{msg_type} {user_id} 信息 {self.content}({self.timestamp})"

    def __content(self):
        "更新消息内容"

        content: dict = json.loads(self.content)
        mt = str(self.msg_type)

        if mt == Event.TEXT:
            self.content = content.get("content")

        elif mt == Event.WELCOME:
            self.content = content.get("content") + str(content.get("group_id"))

        elif mt == Event.WITHDRAW:
            self.content = str(content)

        elif mt == Event.PICTURE or mt == Event.GROUPS_PICTURE:
            self.content = Picture(**content)

        elif mt == Event.SHARE_VIDEO or mt == Event.PUSHED_VIDEO:
            self.content = Video(bvid=content.get("bvid"), aid=content.get("id"))

        elif mt == Event.NOTICE:
            self.content = content["title"] + " " + content["text"]

        else:
            print(mt, content)


class Session(AsyncEvent):
    def __init__(self, credential: Credential, debug=False):
        super().__init__()
        # 会话状态
        self.__status = 0

        # 已获取会话中最大的时间戳 默认当前时间
        self.maxTs = int(time.time() * 1000000)

        # 会话UID为键 会话中最大Seqno位置值
        self.maxSeqno = dict()

        # 凭证
        self.credential = credential

        # 异步定时任务框架
        self.sched = AsyncIOScheduler(timezone="Asia/Shanghai")

        # 已接收的所有事件 用于撤回时找回
        self.events = dict()

        # logging
        self.logger = logging.getLogger("Session")
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s][%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S"
                )
            )
            self.logger.addHandler(handler)

    def get_status(self):
        """
        获取连接状态

        Returns:
            int: 0 初始化，1 已连接，2 断开连接中，3 已断开，4 错误
        """
        return self.__status

    async def run(self, except_self: bool = True):
        """
        非阻塞异步爬虫 定时发送请求获取消息

        Args:
            except_self: bool 是否排除自己发出的消息，默认是
        """

        # 获取自身UID 用于后续判断消息是发送还是接收
        self_info = await get_self_info(self.credential)
        self.uid = self_info["mid"]

        # 初始化 只接收开始运行后的新消息
        js = await get_sessions(self.credential)
        self.maxSeqno = {
            _session["talker_id"]: _session["max_seqno"]
            for _session in js.get("session_list", [])
        }

        # 间隔 6 秒轮询消息列表 之前设置 3 秒询一次 跑了一小时给我账号冻结了
        @self.sched.scheduled_job(
            "interval",
            id="query",
            seconds=6,
            max_instances=3,
            next_run_time=datetime.datetime.now(),
        )
        async def qurey():
            js: dict = await new_sessions(self.credential, self.maxTs)
            if js.get("session_list") is None:
                return

            pending = set()
            for session in js["session_list"]:
                self.maxTs = max(self.maxTs, session["session_ts"])
                pending.add(
                    asyncio.create_task(
                        fetch_session_msgs(
                            session["talker_id"],
                            self.credential,
                            self.maxSeqno.get(session["talker_id"]),
                        )
                    )
                )
                self.maxSeqno[session["talker_id"]] = session["max_seqno"]

            while pending:
                done, pending = await asyncio.wait(pending)
                for done_task in done:
                    result: dict = await done_task
                    if result is None or result.get("messages") is None:
                        continue
                    for message in result.get("messages", [])[::-1]:
                        event = Event(message, self.uid)
                        if str(event.msg_type) == Event.WITHDRAW:
                            self.logger.info(
                                str(
                                    self.events.get(
                                        event.content, f"key={event.content}"
                                    )
                                )
                                + f"被撤回({event.timestamp})"
                            )
                        else:
                            self.logger.info(event)

                        # 自己发出的消息不派发任务
                        if event.sender_uid != self.uid or not except_self:
                            self.dispatch(str(event.msg_type), event)

                        self.events.update({str(event.msg_key): event})

            self.logger.debug(f"maxTs = {self.maxTs}")

        self.sched.start()
        self.logger.info("开始轮询")

    async def start(self, except_self: bool = True):
        """
        阻塞异步启动 通过调用 self.close() 后可断开连接

        Args:
            except_self: bool 是否排除自己发出的消息，默认是
        """

        await self.run(except_self)
        while self.get_status() < 2:
            await asyncio.sleep(1)

        if self.get_status() == 2:
            self.__status = 3

    async def reply(self, event: Event, text: str):
        """
        快速回复消息

        Args:
            event: Event 要回复的消息
            text:  str   要回复的文字内容
        Returns:
            dict: 调用接口返回的内容。
        """

        return await send_msg(self.credential, event.sender_uid, text)

    def close(self):
        "结束轮询"
        self.sched.remove_job("query")
        self.__status = 2
