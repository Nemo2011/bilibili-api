from . import test_video
import asyncio
from colorama import Fore, init, Style
import datetime, time
import traceback

def collect_test_function(module):
    names = []
    for name in dir(module):
        if name.startswith("test"):
            n: str = module.__name__
            n = ".".join(n.split('.')[1:])
            names.append(f"{n}.{name}")
    return names
 

async def test(module):
    print(Fore.YELLOW + f"=========== 开始测试 {module.__name__} ===========")
    funcs = collect_test_function(module)
    print(Fore.CYAN + '执行 before_all()')
    await module.before_all()
    result = {
        "passed": 0,
        "failed": 0
    }
    for func in funcs:
        print(f"{Fore.YELLOW}测试：{Fore.RESET}{func}   ", end="")
        func = eval(func)
        try:
            res = await func()
            print(Fore.GREEN + "[PASSED]")
            if (res is not None):
                print(Fore.MAGENTA + str(res)[:100])
            result["passed"] += 1
        except Exception as e:
            print(Fore.RED + "[FAILED]")
            print(Fore.BLUE)
            print(traceback.format_exc())
            result["failed"] += 1
    print(Fore.CYAN + '执行 after_all()')
    await module.after_all()
    print(Fore.YELLOW + f"=========== 结束测试 {module.__name__} ===========\n")
    return result

def mixin(source, target):
    target["failed"] += source["failed"]
    target["passed"] += source["passed"]


async def main():
    start = time.time()
    init(True)
    all_result = {
        "passed": 0,
        "failed": 0
    }
    result = await test(test_video)
    mixin(result, all_result)

    # 打印结果
    elapsed = str(datetime.timedelta(seconds=time.time() - start))
    print(f"{Fore.WHITE}{all_result['passed']} {Fore.GREEN}passed, {Fore.WHITE}{all_result['failed']} {Fore.RED}failed.")
    print(f"耗时 {Fore.YELLOW}{elapsed}")
    if all_result["failed"] > 0:
        exit(1)
    else:
        exit(0)

asyncio.get_event_loop().run_until_complete(main())
