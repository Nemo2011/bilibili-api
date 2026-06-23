import tempfile
import textwrap
import time
from pathlib import Path

from bilibili_api import Credential


def _write_cookie_file(content: str) -> Path:
    fd, path = tempfile.mkstemp()
    cookie_path = Path(path)
    with open(fd, "w", encoding="utf-8") as file:
        file.write(textwrap.dedent(content).lstrip())
    return cookie_path


async def test_a_from_cookie_file_filters_and_maps_bilibili_cookies():
    future = int(time.time()) + 86400
    cookie_path = _write_cookie_file(
        f"""
        # Netscape HTTP Cookie File
        .bilibili.com\tTRUE\t/\tFALSE\t{future}\tbuvid3\tbuvid3-value
        .bilibili.com\tTRUE\t/\tFALSE\t{future}\tbuvid4\tbuvid4-value
        #HttpOnly_.bilibili.com\tTRUE\t/\tFALSE\t{future}\tSESSDATA\tsessdata-value
        www.bilibili.com\tFALSE\t/\tFALSE\t{future}\tbili_jct\tcsrf-value
        .bilibili.com\tTRUE\t/\tFALSE\t{future}\tDedeUserID\t123456
        .bilibili.com\tTRUE\t/\tFALSE\t{future}\tac_time_value\trefresh-token
        .bilibili.com\tTRUE\t/\tFALSE\t{future}\tb_nut\tbnut-value
        .youtube.com\tTRUE\t/\tFALSE\t{future}\tSESSDATA\tignored-value
        .notbilibili.com\tTRUE\t/\tFALSE\t{future}\tbili_jct\tignored-value
        """
    )

    try:
        credential = Credential.from_cookie_file(cookie_path)
    finally:
        cookie_path.unlink()

    cookies = credential.get_cookies()
    assert credential.sessdata == "sessdata-value"
    assert credential.bili_jct == "csrf-value"
    assert credential.buvid3 == "buvid3-value"
    assert credential.buvid4 == "buvid4-value"
    assert credential.dedeuserid == "123456"
    assert credential.ac_time_value == "refresh-token"
    assert cookies["b_nut"] == "bnut-value"
    assert "ignored-value" not in cookies.values()


async def test_b_from_cookie_file_keeps_session_cookies_and_ignores_expired():
    future = int(time.time()) + 86400
    cookie_path = _write_cookie_file(
        f"""
        # Netscape HTTP Cookie File
        .bilibili.com\tTRUE\t/\tFALSE\t0\tsid\tsession-cookie
        .bilibili.com\tTRUE\t/\tFALSE\t1\told_cookie\texpired-cookie
        .bilibili.com\tTRUE\t/\tFALSE\t{future}\tbuvid3\tbuvid3-value
        """
    )

    try:
        credential = Credential.from_cookie_file(str(cookie_path))
    finally:
        cookie_path.unlink()

    cookies = credential.get_cookies()
    assert cookies["sid"] == "session-cookie"
    assert cookies["buvid3"] == "buvid3-value"
    assert "old_cookie" not in cookies
