# bilibili_api.login_func

from bilibili_api import login_func

login_key = ""


async def test_a_get_qrcode():
    global login_key
    qrcode_data = login_func.get_qrcode()
    login_key = qrcode_data[1]
    return qrcode_data


async def test_b_check_qrcode_status():
    global login_key
    return login_func.check_qrcode_events(login_key)


async def test_c_start_geetest_server():
    return login_func.start_geetest_server()


async def test_d_check_done_geetest():
    return login_func.done_geetest()


async def test_e_close_geetest_server():
    return login_func.close_geetest_server()
