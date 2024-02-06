from bilibili_api import opus
from .common import get_credential

o = opus.Opus(863994527716737095, get_credential())


async def test_a_Opus_get_info():
    return await o.get_info()


async def test_b_transfer():
    return (
        o.turn_to_article()
        .turn_to_opus()
        .turn_to_article()
        .turn_to_opus()
        .turn_to_dynamic()
        .turn_to_opus()
        .turn_to_dynamic()
        .turn_to_opus()
    )
