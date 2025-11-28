import re
from enum import Enum
from inspect import isclass, iscoroutinefunction, isfunction, ismethod
from typing import Any, Dict, List, Optional, Union

import bilibili_api

SENTENCES = re.compile(r"\w+(?:\([^\)]*\))?\.?")  # 将一条长指令分解成若干语句
FUNC = re.compile(r"[^\.\(]+")  # 从语句中获取要调用的函数或方法名
ARGS = re.compile(r"[^,\(\)]*[,\)]")  # 从语句中获取参数值或指名参数值


class ParseError(Exception):
    """
    解析错误
    """

    def __init__(
        self, operations: List[Dict[str, Union[str, List[Any], Dict[str, Any]]]]
    ):
        super().__init__(operations[-1]["sentence"])
        self.operations = operations


async def parse(path: str, params: Optional[Dict[str, str]] = None) -> Any:
    """
    解析字符串

    Args:
        path (str): 需要解析的字符串

        params (Dict[str, str], Optional): 自定义参数

    Returns:
        Any: 解析结果
    """
    # 常规解析
    if params is None:
        params = {}
    v = params.get(path, None)
    if v is not None:
        return v
    elif path.startswith("'") and path.endswith("'"):
        return path[1:-1]
    elif path.startswith('"') and path.endswith('"'):
        return path[1:-1]
    elif path == "None":
        return None
    elif path == "True":
        return True
    elif path == "False":
        return False
    elif path.removeprefix("-").isdigit():
        return int(path)
    elif path.removeprefix("-").replace(".", "", 1).isdigit() and path.count(".") < 2:
        return float(path)

    # 当前解析到的位置
    position: Any = bilibili_api  # 起始点
    # 操作集
    operations: List[Dict[str, Union[str, List[Any], Dict[str, Any]]]] = []
    # 遍历指令
    for sentence in SENTENCES.findall(path):
        # 分解执行的函数名、参数、指名参数
        func: str = FUNC.findall(sentence)[0]
        flags: List[str] = ARGS.findall(sentence)
        args, kwargs = [], {}

        for flag in flags:
            # 去除句尾的逗号或小括号
            flag = flag[:-1]
            if flag == "":
                continue

            # 通过判断是否有等号存入参数列表或指名参数字典
            arg = flag.split("=")
            if len(arg) == 1:
                args.append(await parse(arg[0], params))
            else:
                kwargs[arg[0]] = await parse(arg[1], params)

        operations.append(
            {"sentence": sentence, "func": func, "args": args, "kwargs": kwargs}
        )

        # 开始转移
        if isinstance(position, dict):
            position = position.get(func, None)
        elif isinstance(position, list):
            position = position[int(func)]
        else:
            position = getattr(position, func, None)

        # 函数调用或创建对象
        if iscoroutinefunction(position):
            position = await position(*args, **kwargs)
        elif isfunction(position) or ismethod(position):
            position = position(*args, **kwargs)
        elif isclass(position) and not issubclass(position, Enum):
            position = position(*args, **kwargs)

        # 当前位置为空则抛出操作集
        if position is None:
            raise ParseError(operations)
    return position
