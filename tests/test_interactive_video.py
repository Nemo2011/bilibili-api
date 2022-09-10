# bilibili_api.interactive_video

from typing import List
from .common import get_credential
from bilibili_api import interactive_video

v = interactive_video.InteractiveVideo(aid=73267982, credential=get_credential())

graph_version = None


async def test_a_InteractiveVideo_get_graph_version():
    return await v.get_graph_version()


async def test_b_InteractiveVideo_get_edge_info():
    return await v.get_edge_info()


async def test_c_get_all_nodes():
    print()

    edges_info = {}

    queue: List[interactive_video.InteractiveNode] = [
        (await v.get_graph()).get_root_node()
    ]

    def createEdge(edge_id: int):
        """
        创建节点信息到 edges_info
        """
        edges_info[edge_id] = {"title": None, "cid": None, "option": None}

    while queue:
        now_node = queue.pop()

        now_node.get_jumping_condition().get_result()

        if (
            now_node.get_node_id() in edges_info
            and edges_info[now_node.get_node_id()]["title"] is not None
            and edges_info[now_node.get_node_id()]["cid"] is not None
        ):
            continue

        retry = 3
        while True:
            try:
                node = await now_node.get_info()
                title = node["title"]
                print("当前节点: ", node["edge_id"], node["title"])
                break
            except Exception as e:
                retry -= 1
                if retry < 0:
                    raise e

        if node["edge_id"] not in edges_info:
            createEdge(node["edge_id"])

        edges_info[node["edge_id"]]["title"] = node["title"]

        if "questions" not in node["edges"]:
            continue

        for n in await now_node.get_children():
            if n.get_node_id() not in edges_info:
                createEdge(n.get_node_id())

            edges_info[n.get_node_id()]["cid"] = n.get_cid()
            edges_info[n.get_node_id()]["option"] = n.get_self_button().get_text()

            # 所有可达顶点 ID 入队
            queue.insert(0, n)

    return edges_info
