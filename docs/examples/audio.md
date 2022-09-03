# 示例：下载指定歌单所有歌曲

```python
from bilibili_api import audio, sync, get_session
import os

AUDIO_LIST_ID = 10624

async def main():
    # 获取歌单歌曲列表
    al = audio.AudioList(AUDIO_LIST_ID)
    audios = []
    p = 1

    while True:
        l = await al.get_song_list(p)
        audios.extend(l['data'])
        if l['pageCount'] >= p:
            break

        p += 1

    sess = get_session()

    # 创建歌单文件夹
    if not os.path.exists(str(AUDIO_LIST_ID)):
        os.mkdir(str(AUDIO_LIST_ID))

    for au in audios:
        # 下载歌曲
        file = f"{AUDIO_LIST_ID}/{au['id']} - {au['title']}.m4a"
        a = audio.Audio(au['id'])
        url = await a.get_download_url()
        url = url['cdns'][0]
        print(f"下载 {au['title']}")
        resp = await sess.get(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.bilibili.com/"
        })
        with open(file, 'wb') as f:
            for chunk in resp.iter_bytes(1024):
                if not chunk:
                    break

                f.write(chunk)


sync(main())
```

