"""
此处为测试 credential 维护 buvid / bili_ticket 专用。

Credential 维护 buvid / bili_ticket 遵循以下规则：
1. `global` 为模块初始化时定义的独一无二的凭据类。
2. `blank` 为 `get_core_cookies` 字段全为 `None` 的凭据类，即 `Credential()`。可通过 `check_blank()` 检查凭据类是否为 `blank`。
3. 其余凭据类均为 `normal`，即使传入 `sessdata="", bili_jct=""` 亦视为 `normal`。
4. `get_xxx` 函数拆分为 `ensure_xxx` 和 `obtain_xxx`，接受凭据类传入。
    1. `ensure` 保证 `buvid` / `bili_ticket` 存在且可用，只有凭据类中的 `buvid` 和 `bili_ticket` 不可用才进行 `obtain`。`ensure` 在已有 cookies 情况下不会修改 cookies。
    2. `obtain` 总是发起网络请求获取新的 `buvid` / `bili_ticket`。
5. `blank` 或在 `global_persistence` 下，凭据类进行 `ensure` 或 `obtain` 将先 `ensure global` 或 `obtain global`，再复制 `global` 相关字段，称此复制过程为同步。
6. `get_cookies` 中直接调用 `ensure`，不会直接调用 `obtain`。在禁用 `buvid` 与 `bili_ticket` 自动获取时只同步不请求。
7. `ensure` 与 `obtain` 若没有传入凭据类，将创建一个新的 `blank` 作为凭据类带入。因此获取 `global` 字段直接不带参调用 `ensure`，更新 `global` 字段直接不带参调用 `obtain`。
"""

from bilibili_api import Credential, ensure_buvid, request_settings, sync
from bilibili_api.utils import network

CNT = 0


async def _get_spi_buvid():
    global CNT
    CNT += 1
    return {"b_3": str(CNT), "b_4": str(CNT)}, ""


async def _active_buvid(*args, **kwargs):
    pass


async def _gen_buvid_fp(*args, **kwargs):
    return "", ""


network._get_spi_buvid = _get_spi_buvid
network._active_buvid = _active_buvid
network._gen_buvid_fp = _gen_buvid_fp


async def main():
    # Credential 维护 buvid / bili_ticket 遵循以下规则：
    # 1、blank 总是与 global 保持一致 (get_cookies / ensure / obtain)
    # 2、normal 第一次赋值 buvid / bili_ticket 后非必要不变更 (除 bili_ticket 刷新)
    # 3、ensure 需要保证 buvid / bili_ticket 可用，尽量避免修改 credential 与 obtain
    # 4、obtain 总是发起网络请求获取新的 buvid / bili_ticket
    # 5、get_cookies 正常情况调用 ensure，在禁用 buvid 与 bili_ticket 时只同步不请求。
    cred1 = Credential(sessdata="")  # normal 1
    cred2 = Credential(sessdata="")  # normal 2
    cred3 = Credential()  # blank -> global 3
    cred4 = Credential(sessdata="")  # normal 4
    cred5 = Credential()  # blank -> global 3
    assert (await cred1.get_cookies())["buvid3"] == "1"
    assert (await cred2.get_cookies())["buvid3"] == "2"
    assert (await cred3.get_cookies())["buvid3"] == "3"
    assert (await cred4.get_cookies())["buvid3"] == "4"
    assert (await cred5.get_cookies())["buvid3"] == "3"
    request_settings.set_enable_buvid_global_persistence(True)
    cred6 = Credential(sessdata="")  # normal -> global 3
    cred7 = Credential()  # blank -> global 3
    cred8 = Credential(sessdata="")  # normal -> global 3
    assert (await cred6.get_cookies())["buvid3"] == "3"
    assert (await cred7.get_cookies())["buvid3"] == "3"
    assert (await cred8.get_cookies())["buvid3"] == "3"
    assert (await cred1.get_cookies())["buvid3"] == "1"
    assert (await cred2.get_cookies())["buvid3"] == "2"
    request_settings.set_enable_buvid_global_persistence(False)
    cred9 = Credential()  # blank -> global 3
    cred10 = Credential(sessdata="")  # normal 5
    assert (await cred9.get_cookies())["buvid3"] == "3"
    assert (await cred10.get_cookies())["buvid3"] == "5"
    await network.obtain_buvid()  # obtain global -> global 6
    assert (await cred9.get_cookies())["buvid3"] == "3"
    await network.obtain_buvid(cred9)  # obtain blank -> global -> global 7
    assert (await cred9.get_cookies())["buvid3"] == "7"
    await network.obtain_buvid(cred10)  # obtain normal -> normal 8
    assert (await cred9.get_cookies())["buvid3"] == "7"
    assert (await cred10.get_cookies())["buvid3"] == "8"
    request_settings.set_enable_buvid_global_persistence(True)
    assert (await cred10.get_cookies())["buvid3"] == "8"
    await network.obtain_buvid(cred10)  # obtain normal -> global -> global 9
    assert (await ensure_buvid())[0] == "9"
    assert (await cred10.get_cookies())["buvid3"] == "9"
    assert (await cred1.get_cookies())["buvid3"] == "1"
    request_settings.set_enable_auto_buvid(False)
    cred = Credential()  # blank -> global 9
    assert (await cred.get_cookies())["buvid3"] == "9"
    cred0 = Credential(sessdata="")  # normal -> global 9
    assert (await cred0.get_cookies())["buvid3"] == "9"
    assert (await cred1.get_cookies())["buvid3"] == "1"
    cred1.clear_buvid()  # normal 1 clear, upd -> global 9
    assert (await cred1.get_cookies())["buvid3"] == "9"
    request_settings.set_enable_buvid_global_persistence(False)
    credn = Credential(sessdata="")  # normal without request
    assert not (await credn.get_cookies()).get("buvid3")


sync(main())
