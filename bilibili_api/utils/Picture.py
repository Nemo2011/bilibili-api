from dataclasses import dataclass
from PIL import Image
from typing import Any
import tempfile
import os
import httpx


@dataclass
class Picture:
    """
    (@dataclasses.dataclass)

    图片类，包含图片链接、尺寸以及下载操作。

    Args:
        height    (int)  : 高度           
        imageType (str)  : 格式，例如: png
        size      (Any)  : 尺寸           
        url       (str)  : 图片链接        
        width     (int)  : 宽度           
        content   (bytes): 图片内容       

    初始化可以不传入任何参数，可以用 `from_url` 或 `from_file` 加载。
    """

    height: int = -1
    imageType: str = ""
    size: Any = ""
    url: str = ""
    width: int = -1
    content: bytes = b''

    def __set_picture_meta_from_bytes(self, imgtype: str) -> None:
        tmp_dir = tempfile.gettempdir()
        img_path = os.path.join(tmp_dir, "test." + imgtype)
        with open(img_path, "wb+") as file:
            file.write(self.content)
        img = Image.open(img_path)
        self.size = img.size
        self.height = img.height
        self.width = img.width
        self.imageType = imgtype

    def from_url(self, url: str) -> "Picture":
        session = httpx.Client()
        resp = session.get(url)
        self.content = resp.read()
        self.url = url
        self.__set_picture_meta_from_bytes(url.split("/")[-1].split(".")[1])
        return self

    def from_file(self, path: str) -> "Picture":
        with open(path, "rb") as file:
            self.content = file.read()
        self.url = "file://" + path
        self.__set_picture_meta_from_bytes(os.path.basename(path).split(".")[1])
        return self

    def convert_format(self, new_format: str) -> None:
        tmp_dir = tempfile.gettempdir()
        img_path = os.path.join(tmp_dir, "test." + self.imageType)
        img = Image.open(img_path)
        new_img_path = os.path.join(tmp_dir, "test." + new_format)
        img.save(new_img_path)
        with open(new_img_path, "rb") as file:
            self.content = file.read()
        self.__set_picture_meta_from_bytes(new_format)

    def download(self, path: str) -> None:
        tmp_dir = tempfile.gettempdir()
        img_path = os.path.join(tmp_dir, "test." + self.imageType)
        img = Image.open(img_path)
        img.save(path)
