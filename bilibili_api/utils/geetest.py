"""
bilibili_api.utils.geetest

极验
"""

from dataclasses import dataclass
import email.message
import enum
import http.server
import os
import select
import threading

from ..exceptions import GeetestException
from .network import Api
from .utils import get_api

API = get_api("login")


class GeetestType(enum.Enum):
    """
    极验验证码类型

    - LOGIN: 登录
    - VERIFY: 登录验证
    """

    LOGIN = "password"
    VERIFY = "safecenter"


@dataclass
class GeetestMeta:
    """
    极验验证码完成信息

    NOTE: `gt`, `challenge`, `token` 为验证码基本字段。`seccode`, `validate` 为完成验证码后可得字段。
    """

    gt: str
    challenge: str
    token: str
    seccode: str = ""
    validate: str = ""


class DocHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Process a request from an HTML browser.

        The URL received is in self.path.
        Get an HTML page from self.urlhandler and send it.
        """
        if self.path.endswith(".css"):
            content_type = "text/css"
        else:
            content_type = "text/html"
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=UTF-8")
        self.end_headers()
        self.wfile.write(self.urlhandler(self.path, content_type).encode("utf-8"))  # type: ignore

    def log_message(self, *args):
        # Don't log messages.
        pass


class DocServer(http.server.HTTPServer):
    def __init__(self, host, port, callback):
        self.host = host
        self.address = (self.host, port)
        self.callback = callback
        self.base.__init__(self, self.address, self.handler)  # type: ignore
        self.quit = False

    def serve_until_quit(self):
        while not self.quit:
            rd, _wr, _ex = select.select([self.socket.fileno()], [], [], 1)
            if rd:
                self.handle_request()
        self.server_close()

    def server_activate(self):
        self.base.server_activate(self)  # type: ignore
        if self.callback:
            self.callback(self)


class ServerThread(threading.Thread):
    def __init__(self, urlhandler, host, port):
        self.urlhandler = urlhandler
        self.host = host
        self.port = int(port)
        threading.Thread.__init__(self)
        self.serving = False
        self.error = None

    def run(self):
        """Start the server."""
        try:
            DocServer.base = http.server.HTTPServer  # type: ignore
            DocServer.handler = DocHandler  # type: ignore
            DocHandler.MessageClass = email.message.Message  # type: ignore
            DocHandler.urlhandler = staticmethod(self.urlhandler)  # type: ignore
            docsvr = DocServer(self.host, self.port, self.ready)
            self.docserver = docsvr
            docsvr.serve_until_quit()
        except Exception as e:
            self.error = e

    def ready(self, server):
        self.serving = True
        self.host = server.host
        self.port = server.server_port
        self.url = "http://%s:%d/" % (self.host, self.port)

    def stop(self):
        """Stop the server and this thread nicely"""
        if self.docserver is not None:
            self.docserver.quit = True
            self.join()
            # explicitly break a reference cycle: DocServer.callback
            # has indirectly a reference to ServerThread.
            self.docserver = None
            self.serving = False
            self.url = None


class Geetest:
    """
    极验验证类
    """

    def __init__(self) -> None:
        self.gt = ""
        self.validate = ""
        self.seccode = ""
        self.challenge = ""
        self.key = ""
        self.thread = None
        self.done = False
        self.test_type = None

    async def generate_test(self, type_: GeetestType = GeetestType.LOGIN) -> None:
        """
        创建验证码

        Args:
            type_ (GeetestType): 极验验证码类型。登录为 LOGIN，登录验证为 VERIFY. Defaults to GeetestType.LOGIN.
        """
        api = API[type_.value]["captcha"]
        json_data = await Api(**api, no_csrf=True).result
        if type_ == GeetestType.LOGIN:
            self.gt = json_data["geetest"]["gt"]
            self.challenge = json_data["geetest"]["challenge"]
            self.key = json_data["token"]
        else:
            self.gt = json_data["gee_gt"]
            self.challenge = json_data["gee_challenge"]
            self.key = json_data["recaptcha_token"]
        self.validate = None
        self.seccode = None
        self.done = False
        self.test_type = type_

    def get_test_type(self) -> GeetestType:
        """
        获取测试类型

        Returns:
            GeetestType: 测试类型
        """
        if not self.test_generated():
            raise GeetestException("未生成过测试。请调用 `generate_test`")
        return self.test_type

    def test_generated(self) -> bool:
        """
        当前是否有创建的测试

        Returns:
            bool: 是否有创建的测试
        """
        return self.key is not None

    def get_info(self) -> GeetestMeta:
        """
        获取验证码信息

        Returns:
            GeetestMeta: 验证码信息
        """
        return GeetestMeta(gt=self.gt, challenge=self.challenge, token=self.key)

    def has_done(self) -> bool:
        """
        是否完成

        Returns:
            bool: 是否完成
        """
        return self.done

    def get_result(self) -> GeetestMeta:
        """
        获取结果

        Returns:
            GeetestMeta: 验证结果
        """
        if self.done:
            return GeetestMeta(
                gt=self.gt,
                challenge=self.challenge,
                token=self.key,
                validate=self.validate,
                seccode=self.seccode,
            )
        else:
            raise GeetestException(
                "未完成验证。请调用 `complete_test` 或来到 `get_geetest_server_url` 页面完成验证码。"
            )

    def complete_test(self, validate: str, seccode: str) -> None:
        """
        作答测试

        Args:
            validate (str): 作答结果的 validate
            seccode  (str): 作答结果的 seccode
        """
        self.validate = validate
        self.seccode = seccode
        self.done = True

    def _geetest_urlhandler(self, url: str, content_type: str) -> str:
        """
        极验验证服务器 html 源获取函数
        """
        url = url[1:]
        if url[:7] == "result/":
            datas = url[7:]
            datas = datas.split("&")
            for data in datas:
                if data[:8] == "validate":
                    self.validate = data[9:]
                elif data[:7] == "seccode":
                    self.seccode = data[8:].replace("%7C", "|")
                self.done = True
            with open(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__), "..", "data", "geetest", "done.html"
                    )
                ),
                encoding="utf8",
            ) as f:
                html_source_bytes = f.read()
            return html_source_bytes
        elif url[:7] == "":
            with open(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "data",
                        "geetest",
                        "captcha.html",
                    )
                ),
                encoding="utf8",
            ) as f:
                html_source_bytes = (
                    f.read()
                    .replace("{ Python_Interface: GT }", f'"{self.gt}"')
                    .replace("{ Python_Interface: CHALLENGE }", f'"{self.challenge}"')
                )
            return html_source_bytes
        else:
            return ""

    def start_geetest_server(self) -> None:
        """
        开启本地极验验证码服务
        """
        if self.thread is not None:
            raise GeetestException("验证码服务已创建。")
        self.thread = ServerThread(self._geetest_urlhandler, "127.0.0.1", 0)
        self.thread.start()
        while not self.thread.error and not self.thread.serving:
            pass

    def get_geetest_server_url(self) -> str:
        """
        获取本地极验验证码服务链接

        Returns:
            str: 链接
        """
        if not self.thread:
            return GeetestException("未创建验证码服务。请调用 `start_geetest_server`")
        return self.thread.url

    def close_geetest_server(self) -> None:
        """
        关闭本地极验验证码服务
        """
        self.thread.stop()
        self.thread = None
