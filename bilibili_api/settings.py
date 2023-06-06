"""
bilibili_api.settings

这里是配置模块的地方
"""

import logging

proxy: str = ""
"""
代理设置

e.x.:
``` python
from bilibili_api import settings
settings.proxy = "https://www.example.com"
```
"""

timeout: float = 5.0
"""
web 请求超时时间设置
"""

geetest_auto_open: bool = True
"""
是否自动打开 geetest 验证窗口
"""

request_log: bool = False
"""
请求 Api 时是否打印 Api 信息
"""

logger = logging.getLogger("request")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "[Request][%(asctime)s] %(message)s"
        )
    )
    logger.addHandler(handler)