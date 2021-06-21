from bilibili_storytree import StoryGraph, ScriptNode

class Oscar:
  def __init__(self, videos: dict, aid: int):
    self.videos = videos
    # Create graph
    self.graph = StoryGraph(aid=aid)

  def gen_simple_graph(self, root_title: str):
    # 建情节树：只有一个分支剧情模块
    root_video = self.videos[root_title] 
    n_root = ScriptNode(node_type="videoNode", isRoot=True)
    n_root.set_video(video=root_video)
    self.graph._update_script_nodes([n_root]) # update graph["script"]["nodes"]
    self.graph._sync_nodes() # create graph["nodes"]
    self.graph._sync_vars() # create graph["regional_vars"]
