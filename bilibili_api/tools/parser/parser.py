import re
from enum import Enum
from inspect import isclass
from inspect import iscoroutinefunction as isAsync
from inspect import isfunction as isFn
from typing import List, Tuple

import bilibili_api

FUNC = re.compile(r"[^\.\(]+")
ARGS = re.compile(r"[^,\(\)]*[,\)]")
SENTENCES = re.compile(r"\w+(?:\([^\)]*\))?\.?")


class Parser:

    Types = {
        ":int": int,
        ":float": float,
        ":bool": lambda s: s == "True",
    }

    def __init__(self, var: str):
        self.valid = True
        self.varDict = dict(v.split("<-") for v in var.split(";")) if var else dict()

    async def __aenter__(self):
        for key, val in self.varDict.items():
            msg, obj = await self.parse(val)
            if msg == "":
                if isinstance(obj, bilibili_api.Credential):
                    self.valid = await obj.check_valid()
                self.varDict[key] = obj
        return self

    async def __aexit__(self, type, value, trace):
        ...

    async def transform(self, arg: List[str]):
        "假设变量为键值形式 利用列表特性从 -1 读取值 即使没有键也能读到值"
        # 类型装换
        for key, fn in self.Types.items():
            if arg[-1].endswith(key):
                arg[-1] = fn(arg[-1].replace(key, ""))
                break
        else:
            if arg[-1].endswith(":parse"):
                msg, obj = await self.parse(arg[-1].replace(":parse", ""))
                if msg == "":
                    arg[-1] = obj

        # 将值与储存的变量替换
        arg[-1] = self.varDict.get(arg[-1], arg[-1])

    async def parse(self, path: str) -> Tuple[str, any]:
        "分析指令"

        # 指令列表
        sentences = SENTENCES.findall(path)
        # 起始点
        position: any = bilibili_api

        async def inner() -> str:
            "递归取值"

            nonlocal position
            # 分解执行的函数名、参数、指名参数
            sentence = sentences.pop(0)
            func: str = FUNC.findall(sentence)[0]
            flags: List[str] = ARGS.findall(sentence)
            args, kwargs = list(), dict()

            for flag in flags:
                # 去除句尾的逗号或小括号
                flag = flag[:-1]
                if flag == "":
                    continue
                arg = flag.split("=")
                await self.transform(arg)
                # 存入对应的参数、指名参数
                if len(arg) == 1:
                    args.append(arg[0])
                else:
                    kwargs[arg[0]] = arg[1]

            # 开始转移
            if isinstance(position, dict):
                position = position.get(func, None)
            elif isinstance(position, list):
                position = position[int(func)]
            else:
                position = getattr(position, func, None)

            # 赋值参数
            if isAsync(position):
                position = await position(*args, **kwargs)
            elif isFn(position):
                position = position(*args, **kwargs)
            elif isclass(position) and not issubclass(position, Enum):
                position = position(*args, **kwargs)

            # 为空返回出错语句
            # 否则检查是否分析完全部语句
            # 是则返回空字符 否继续递归
            if position is None:
                return sentence
            return "" if len(sentences) == 0 else await inner()

        return await inner(), position
