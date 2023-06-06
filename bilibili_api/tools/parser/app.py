from typing import Any, Dict

from fastapi import FastAPI, Request, Response

from .parser import Parser


def Result(code: int, data: Any) -> dict:
    """
    请求结果

    Args:
        code (int): 状态码

        data (Any): 返回数据

    Result:
        dict: 返回体
    """
    return {
        "code": code,
        "data" if code == 0 else "error": data
    }


async def bilibili_api_web(
    request: Request,
    response: Response,
    path: str,
) -> dict:
    """
    网络接口

    Args:
        request (request): 请求

        response (Response): 响应

        path (str): 请求路径 例如 `user.User(434334701).get_user_info()`

        max_age (int, Optional): 请求头 `Cache-Control` 中的 `max-age`

        params (str, Optional): 可选变量 如果 path 中多次用到某个值可保存

            例如 `?uid=434334701&roomid=21452505`
    
    Returns:
        dict: 解析结果
    """
    # 返回头设置
    vars: Dict[str, str] = dict(request.query_params)
    max_age = vars.pop("max_age", None)
    if max_age is not None:
        response.headers["Cache-Control"] = f"max-age={max_age}"
    response.headers["Access-Control-Allow-Origin"] = "*"

    # 先判断是否有效 再分析
    try:
        async with Parser(vars) as parser:
            if not parser.valid:
                return Result(1, "Credential 验证失败")
            obj, err = await parser.parse(path)  # 什么 golang 写法
            if err is None:
                return Result(0, obj)
            return Result(2, f"解析语句 {err} 错误")
    except Exception as e:
        return Result(3, f"未知错误 {e}")


def get_fastapi(app_run_path: str = "/{path}") -> FastAPI:
    app = FastAPI()
    app_run_path = app_run_path if "{path}" in app_run_path else "/{path}"
    app.add_api_route(app_run_path, bilibili_api_web, methods=["GET"])
    return app