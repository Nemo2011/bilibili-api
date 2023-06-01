import re
from enum import Enum
from inspect import isclass
from inspect import iscoroutinefunction as isAsync
from inspect import isfunction as isFn
from typing import Any, Dict, List, Optional, Tuple

import bilibili_api

FUNC = re.compile(r"[^\.\(]+")
ARGS = re.compile(r"[^,\(\)]*[,\)]")
SENTENCES = re.compile(r"\w+(?:\([^\)]*\))?\.?")
OPS = {
    ":int": int,
    ":float": float,
    ":bool": lambda s: s == "True",
}


class Parser:
    """
    解析器
    """

    def __init__(self, params: Dict[str, str]):
        self.valid = True
        self.params = params

    async def __aenter__(self):
        """
        解析前准备

        把 params 中的参数先解析了
        """
        for key, val in self.params.items():
            obj, err = await self.parse(val)
            if err is None:
                if isinstance(obj, bilibili_api.Credential):
                    self.valid = await bilibili_api.check_valid(obj)
                self.params[key] = obj
        return self

    async def __aexit__(self, type, value, trace):
        ...

    async def transform(self, var: str) -> Any:
        """
        类型装换函数
        
        通过在字符串后加上 `:int` `:float` `:bool` `:parse` 等操作符来实现

        Args:
            var (str): 需要转换的字符串
        
        Returns:
            Any: 装换结果
        """
        for key, fn in OPS.items():
            if var.endswith(key):
                return fn(var.replace(key, ""))
        if var.endswith(":parse"):
            obj, err = await self.parse(var.replace(":parse", ""))
            if err is None:
                return obj

        # 是请求时 params 中定义的变量 获取出来 不是的话返回原字符
        return self.params.get(var, var)

    async def parse(self, path: str) -> Tuple[Any, Optional[str]]:
        """
        分析指令
        
        Args:
            path (str): 需要解析的 token 对应库中的路径
        
        Returns:
            Any: 最终数据 若解析失败为 None

            str: 错误信息 若解析成功为 None
        """
        # 纯数字
        if path.replace(":int", "").replace(":float", "").replace(".", "").replace("-", "").isdigit():
            return await self.transform(path), None

        # 指令列表
        sentences = SENTENCES.findall(path)
        # 起始点
        position: Any = bilibili_api

        async def inner() -> Optional[str]:
            """
            递归取值
            
            Returns:
                str: 错误信息 若解析成功为 None
            """
            nonlocal position
            # 分解执行的函数名、参数、指名参数
            sentence = sentences.pop(0)
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
                    args.append(await self.transform(arg[0]))
                else:
                    kwargs[arg[0]] = await self.transform(arg[1])

            # print(position, func, args, kwargs)

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
            # 是则返回 None 否继续递归
            if position is None:
                return sentence
            if len(sentences) == 0:
                return None
            return await inner()

        msg = await inner()
        return position, msg
