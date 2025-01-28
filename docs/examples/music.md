# 示例：获取视频识别出来的音乐的相关视频

``` python
from bilibili_api import video, music, sync, aid2bvid
from pprint import pprint


BVID = "BV1Y9iZYUE6y"


async def main():
    v = video.Video(bvid=BVID)
    vinfo = await v.get_detail()  # 获取视频信息，从视频信息中获取识别到的音乐
    try:
        music_maid = vinfo["Tags"][0]["music_id"]
    except:
        print("未识别到音乐。")
        return
    if music_maid == "":
        print("未识别到音乐。")
        return
    m = music.Music(music_maid)
    m_videos = await m.get_music_videos()
    for m_v in m_videos["list"]:
        print(m_v["bvid"], m_v["title"])


sync(main())
```
