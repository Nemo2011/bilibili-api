"""
bilibili_api.utils.aid_bvid_transformer

av 号和 bv 号互转，代码来源：https://www.zhihu.com/question/381784377/answer/1099438784。

此部分代码以 WTFPL 开源。
"""


def bvid2aid(bvid: str) -> int:
    """
    BV 号转 AV 号。

    Args:
        bvid (str):  BV 号。

    Returns:
        int: AV 号。
    """
    table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    def dec(x):
        r = 0
        for i in range(6):
            r += tr[x[s[i]]] * 58**i
        return (r - add) ^ xor

    return dec(bvid)


def aid2bvid(aid: int) -> str:
    """
    AV 号转 BV 号。

    Args:
        aid (int):  AV 号。

    Returns:
        str: BV 号。
    """
    table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
    tr = {}
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    def enc(x):
        x = (x ^ xor) + add
        r = list("BV1  4 1 7  ")
        for i in range(6):
            r[s[i]] = table[x // 58**i % 58]
        return "".join(r)

    return enc(aid)
