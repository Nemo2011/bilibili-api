import json

from fastapi import FastAPI, Request, Response

import bilibili_api

from .parser import ParseError, parse


def format_error(e: Exception) -> str:
    return e.__class__.__name__ + (f": {e}" if str(e) else "")


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
        dict: 响应体
    """
    vars: dict[str, str] = dict(request.query_params)
    max_age = vars.pop("max_age", None)
    if max_age is not None:
        response.headers["Cache-Control"] = f"max-age={max_age}"
    response.headers["Access-Control-Allow-Origin"] = "*"

    for key, val in vars.items():
        try:
            obj = await parse(val)
        except ParseError as e:
            return {
                "code": 1,
                "error": f"参数 {key} 解析出错: {format_error(e)}",
                "operations": e.operations,
            }
        except Exception as e:
            return {
                "code": 2,
                "error": f"参数 {key} 未知错误: {format_error(e)}",
            }
        if isinstance(obj, bilibili_api.Credential):
            try:
                if not await obj.check_valid():
                    return {
                        "code": 3,
                        "error": f"参数 {key} 凭证失效",
                    }
            except Exception as e:
                return {
                    "code": 4,
                    "error": f"参数 {key} 凭证验证出错: {format_error(e)}",
                }
        vars[key] = obj
    try:
        obj = await parse(path, vars)
    except ParseError as e:
        return {
            "code": 5,
            "error": f"指令解析出错: {format_error(e)}",
            "operations": e.operations,
        }
    except Exception as e:
        return {
            "code": 6,
            "error": f"指令未知错误: {format_error(e)}",
        }
    try:
        json.dumps(obj)  # 尝试序列化
        return {
            "code": 0,
            "data": obj,
        }
    except Exception as e:
        return {
            "code": 7,
            "error": f"序列化响应体出错: {format_error(e)}",
        }


def get_fastapi(app_run_path: str = "/{path}") -> FastAPI:
    app = FastAPI()
    app_run_path = app_run_path if "{path}" in app_run_path else "/{path}"
    app.add_api_route(app_run_path, bilibili_api_web, methods=["GET"])
    return app
