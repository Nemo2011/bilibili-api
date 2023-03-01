# bilibili_api.__init__

from bilibili_api import parse_link, get_real_url
from .common import get_credential

parse_link_urls = [
    "av82054919",
    "AV82054919",
    "BV1XJ41157tQ",
    "https://www.bilibili.com/video/av82054919",
    "https://www.bilibili.com/video/BV1XJ41157tQ",
    "https://www.bilibili.com/bangumi/media/md28237119",
    "https://www.bilibili.com/bangumi/play/ss41410",
    "https://www.bilibili.com/bangumi/play/ep508404",
    "ml966613735",
    "ML966613735",
    "https://space.bilibili.com/558830935/favlist",
    "https://space.bilibili.com/558830935/favlist?fid=966613735&ftype=create",
    "https://space.bilibili.com/558830935/favlist?fid=966613735&ftype=collect&ctype=11",
    "https://space.bilibili.com/558830935/favlist?fid=articles",
    "https://space.bilibili.com/558830935/favlist?fid=pugvfav",
    "https://www.bilibili.com/medialist/detail/ml966613735",
    "https://www.bilibili.com/cheese/play/ss61",
    "https://www.bilibili.com/cheese/play/ep790",
    "au800841",
    "AU800841",
    "https://www.bilibili.com/audio/au800841",
    "am10624",
    "AM10624",
    "https://www.bilibili.com/audio/am10624",
    "cv17809055",
    "CV17809055",
    "https://www.bilibili.com/read/cv17809055",
    "uid558830935",
    "UID558830935",
    "https://space.bilibili.com",
    "https://space.bilibili.com/558830935",
    "https://live.bilibili.com/558830935",
    "https://space.bilibili.com/19319172/channel/collectiondetail?sid=250818",
    "https://space.bilibili.com/558830935/channel/seriesdetail?sid=2972810",
    "https://www.bilibili.com/list/471723540?sid=849191&spm_id_from=333.999.0.0&desc=1",
    "https://space.bilibili.com/558830935/favlist?fid=56245&ftype=collect&ctype=21",
    "https://www.bilibili.com/read/readlist/rl207146",
    "https://t.bilibili.com/747943493670797385",
    "https://www.bilibili.com/blackroom/ban/2670821",
    "https://www.biligame.com/detail/?id=103009",
    "https://www.bilibili.com/v/topic/detail/?topic_id=57290",
    "https://manga.bilibili.com/detail/mc32020",
    "https://h.bilibili.com/1198098",
    "https://www.bilibili.com/h5/note-app/view?cvid=21385583",
    "https://www.bilibili.com/opus/767674573455884292",
]


async def test_a_parse_link():
    print()
    for url in parse_link_urls:
        print(f"正在测试 {url} ...")
        result = await parse_link(url, get_credential())
        assert result[0] != -1
        print(f"结果: {result}")


async def test_b_get_real_url():
    return await get_real_url("https://b23.tv/mx00St")
