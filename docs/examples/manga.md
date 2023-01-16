# 示例：下载漫画所有的图片

```python
from bilibili_api import manga, sync

async def main() -> None:
    # 初始化漫画类
    comic = manga.Manga(manga_id=30023)
    # 获取所有图片的未经处理的链接
    images_url = await comic.get_images_url(1)
    # 处理图片+下载
    image_cnt = 0
    for img in images_url["images"]:
        url = img["path"] # 不可以直接通过图片的链接下载
        # 将未经处理无法操作的图片链接转换为可操作的 Picture 类
        pic = await manga.manga_image_turn_to_Picture(url=url)
        # 下载图片
        await pic.download(str(image_cnt) + ".jpg")
        # 输出进度
        image_cnt += 1
        print(f"Complete {image_cnt} image(s). ")

if __name__ == "__main__":
    sync(main())
```

# 示例：设置追漫

啊，我还没做呢，急个什么啊？
