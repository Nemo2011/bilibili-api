"""
代码自动化测试工具

Usage:
    python -m tests.main [options]

Options:
    -m <模块名>:    运行指定测试脚本
    -a:            运行所有测试脚本（以 test_ 开头的）

Environment:
    BILI_SESSDATA
    BILI_CSRF
    BILI_BUVID3
    BILI_DEDEUSERID
    BILI_RATELIMIT

"""
import asyncio
from colorama import Fore, init, Style
import os
import sys
import getopt
import datetime, time
import traceback
import os
import importlib

def collect_test_function(module):
    names = []
    for name in dir(module):
        if name.startswith("test"):
            names.append(f"{name}")
    return names

RATELIMIT = float(os.getenv('BILI_RATELIMIT')) if os.getenv('BILI_RATELIMIT') is not None else 0


async def test(module):
    print(Fore.YELLOW + f"::group::=========== 开始测试 {module.__name__} ===========")
    funcs = collect_test_function(module)

    result = {
        "passed": 0,
        "failed": 0,
        "failed_items": []
    }

    if "before_all" in dir(module):
        print(Fore.CYAN + '执行 before_all()')
        try:
            await module.before_all()
            result["passed"] += 1
        except Exception as e:
            print(f"{Fore.RED} before_all() 报错：{Fore.RESET}")
            print(traceback.format_exc())
            result["failed_items"].append(f"{module.__name__}.before_all")
            result["failed"] += 1
            return result

    for func_name in funcs:
        print(f"{Fore.YELLOW}测试：{Fore.RESET}{func_name}   ", end="")
        func = eval("module." + func_name)
        try:
            res = await func()
            print(Fore.GREEN + "[PASSED]")
            if (res is not None):
                print(Fore.MAGENTA + str(res)[:100])
            result["passed"] += 1
        except Exception as e:
            print(Fore.RED + "[FAILED]")
            print(Fore.BLUE)
            print(str(e))
            print(traceback.format_exc())
            result["failed"] += 1
            result["failed_items"].append(f"{module.__name__}.{func_name}")

        await asyncio.sleep(RATELIMIT)

    if "after_all" in dir(module):
        print(Fore.CYAN + '执行 after_all()')
        try:
            await module.after_all()
            result["passed"] += 1
        except Exception as e:
            print(f"{Fore.RED} after_all() 报错：{Fore.RESET}")
            print(traceback.format_exc())
            result["failed_items"].append(f"{module.__name__}.after_all")
            result["failed"] += 1
            return result

    print(Fore.YELLOW + f"=========== 结束测试 {module.__name__} ===========\n::endgroup::")
    return result

def mixin(source, target):
    target["failed"] += source["failed"]
    target["passed"] += source["passed"]
    target["failed_items"].extend(source["failed_items"])


def get_should_test_module():
    """
    获取将被测试的模块，仅寻找 tests 根目录下的模块
    """
    def get_all_modules():
        modules = []
        base_path = os.path.join(os.path.dirname(__file__), '.')
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.startswith('test_') and file.endswith(".py"):
                    module_name = file[:-3]
                    modules.append(importlib.import_module("tests." + module_name))
            break
        return modules

    def find_module(name: str):
        try:
            m = importlib.import_module("tests." + name)
            return m
        except Exception as e:
            print(e)
            print("找不到模块：" + name)
            return None

    modules = []
    opts, args = getopt.getopt(sys.argv[1:], 'am:')

    for opt, arg in opts:
        if opt == "-a":
            # 测试所有模块
            modules = get_all_modules()
        elif opt == "-m":
            m = find_module(arg)
            if m is None:
                exit(1)
            else:
                modules.append(m)
    return modules


async def main():
    start = time.time()
    init(True)
    all_result = {
        "passed": 0,
        "failed": 0,
        "failed_items": []
    }

    modules = get_should_test_module()
    for module in modules:
        result = await test(module)
        mixin(result, all_result)
    # 打印结果
    elapsed = str(datetime.timedelta(seconds=time.time() - start))
    print(f"{Fore.WHITE}{all_result['passed']} {Fore.GREEN}passed, {Fore.WHITE}{all_result['failed']} {Fore.RED}failed.")
    print(f"耗时 {Fore.YELLOW}{elapsed}")
    if all_result["failed"] > 0:
        print(f"{Fore.RED} 出错测试项目：{Fore.RESET}")
        for item in all_result["failed_items"]:
            print(f"- {item}")
        exit(1)
    else:
        exit(0)

asyncio.run(main())
