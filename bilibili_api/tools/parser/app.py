from fastapi import FastAPI, Response

from .parser import Parser


def get_fastapi(app_run_path: str = "/{path}") -> FastAPI:
    app = FastAPI()
    app_run_path = app_run_path if "{path}" in app_run_path else "/{path}"

    @app.get(app_run_path)
    async def bilibili_api_web(response: Response, path: str, var: str = "", max_age: int = -1):
        # 返回头设置
        response.headers["Access-Control-Allow-Origin"] = "*"
        if max_age != -1:
            response.headers["Cache-Control"] = f"max-age={max_age}"
        
        # 先判断是否有效 再分析
        async with Parser(var) as parser:
            if not parser.valid:
                return {"code": 1, "data": "Credential 验证失败"}
            try:
                msg, obj = await parser.parse(path)  # 什么 golang 写法
                if msg == "":
                    return {"code": 0, "data": obj}
                else:
                    return {"code": 2, "data": f"解析语句 {msg} 错误"}
            except Exception as e:
                return {"code": 3, "data": f"未知错误 {e}"}
    
    return app