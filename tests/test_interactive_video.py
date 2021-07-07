from . import common
from bilibili_api import interactive_video

credential = common.get_credential()
BVID = 'BV1Dt411N7LY'

graph_version = None

async def test_a_get_graph_version():
    global graph_version
    graph_version = await interactive_video.get_graph_version(BVID, credential=credential)
    return graph_version

async def test_b_get_edge_info():
    return await interactive_video.get_edge_info(BVID, graph_version, credential=credential)
