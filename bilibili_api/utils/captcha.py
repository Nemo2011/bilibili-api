"""
bilibili_api.utils.captcha

人机测试
"""
import os
import copy
import json
import time

from .utils import get_api
from .network import Api

validate = None
seccode = None
gt = None
challenge = None
key = None
server = None
thread = None

API = get_api("login")


def _geetest_urlhandler(url: str, content_type: str):
    """
    极验验证服务器 html 源获取函数
    """
    global gt, challenge, key
    url = url[1:]
    if url[:7] == "result/":
        global validate, seccode
        datas = url[7:]
        datas = datas.split("&")
        for data in datas:
            if data[:8] == "validate":
                validate = data[9:]
            elif data[:7] == "seccode":
                seccode = data[8:].replace("%7C", "|")
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
        api = API["password"]["captcha"]
        json_data = Api(**api).result_sync
        gt = json_data["geetest"]["gt"]
        challenge = json_data["geetest"]["challenge"]
        key = json_data["token"]
        with open(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), "..", "data", "geetest", "captcha.html"
                )
            ),
            encoding="utf8",
        ) as f:
            html_source_bytes = (
                f.read()
                .replace("{ Python_Interface: GT }", f'"{gt}"')
                .replace("{ Python_Interface: CHALLENGE }", f'"{challenge}"')
            )
        return html_source_bytes
    else:
        return ""


def _start_server(urlhandler, hostname, port):
    """Start an HTTP server thread on a specific port.

    Start an HTML/text server thread, so HTML or text documents can be
    browsed dynamically and interactively with a web browser.  Example use:

        >>> import time
        >>> import pydoc

        Define a URL handler.  To determine what the client is asking
        for, check the URL and content_type.

        Then get or generate some text or HTML code and return it.

        >>> def my_url_handler(url, content_type):
        ...     text = 'the URL sent was: (%s, %s)' % (url, content_type)
        ...     return text

        Start server thread on port 0.
        If you use port 0, the server will pick a random port number.
        You can then use serverthread.port to get the port number.

        >>> port = 0
        >>> serverthread = pydoc._start_server(my_url_handler, port)

        Check that the server is really started.  If it is, open browser
        and get first page.  Use serverthread.url as the starting page.

        >>> if serverthread.serving:
        ...    import webbrowser

        The next two lines are commented out so a browser doesn't open if
        doctest is run on this module.

        #...    webbrowser.open(serverthread.url)
        #True

        Let the server do its thing. We just need to monitor its status.
        Use time.sleep so the loop doesn't hog the CPU.

        >>> starttime = time.monotonic()
        >>> timeout = 1                    #seconds

        This is a short timeout for testing purposes.

        >>> while serverthread.serving:
        ...     time.sleep(.01)
        ...     if serverthread.serving and time.monotonic() - starttime > timeout:
        ...          serverthread.stop()
        ...          break

        Print any errors that may have occurred.

        >>> print(serverthread.error)
        None
    """
    import select
    import threading
    import http.server
    import email.message

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
            self.send_header("Content-Type", "%s; charset=UTF-8" % content_type)
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
                rd, wr, ex = select.select([self.socket.fileno()], [], [], 1)
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
            if self.docserver != None:
                self.docserver.quit = True
                self.join()
                # explicitly break a reference cycle: DocServer.callback
                # has indirectly a reference to ServerThread.
                self.docserver = None
                self.serving = False
                self.url = None

    thread = ServerThread(urlhandler, hostname, port)
    thread.start()
    # Wait until thread.serving is True to make sure we are
    # really up before returning.
    while not thread.error and not thread.serving:
        time.sleep(0.01)
    return thread


def start_server():
    """
    验证码服务打开服务器

    Returns:
        ServerThread: 服务进程

    返回值内函数及属性:
        - url   (str)     : 验证码服务地址
        - start (Callable): 开启进程
        - stop  (Callable): 结束进程
    """
    global thread
    thread = _start_server(_geetest_urlhandler, "127.0.0.1", 0)
    print("请打开 " + thread.url + " 进行验证。")  # type: ignore
    return thread


def close_server():
    """
    关闭服务器
    """
    global thread
    thread.stop()  # type: ignore


def get_result():
    """
    获取结果

    Returns:
        dict: 验证结果
    """
    global validate, seccode, challenge, gt, key
    if (
        validate is None
        or seccode is None
        or gt is None
        or challenge is None
        or key is None
    ):
        return -1
    else:
        dct = {
            "gt": copy.copy(gt),
            "challenge": copy.copy(challenge),
            "validate": copy.copy(validate),
            "seccode": copy.copy(seccode),
            "token": copy.copy(key),
        }
        return dct
