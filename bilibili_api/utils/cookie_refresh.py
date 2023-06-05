from .network_httpx import request
from .utils import get_api
from .credential import Credential

async def check_cookies(credential: Credential):
    url = get_api('check_cookies')
    return await request(url, cookies=credential)