from bilibili_api.dynamic import DrawDynamic, TextDynamic, InstantDynamic, UploadImages, ScheduleDynamic
from bilibili_api import Verify

# 验证类
verify = Verify(sessdata="", csrf="")

# 上传图片路径列表
img_path = [
    "pic1", "pic2"
]

# 上传图片类
upload = UploadImages(images_path=img_path, verify=verify)

# 如果要@人，格式为 “@用户UID@ ”
# 画册动态类
draw = DrawDynamic(text="这是文字内容", upload_images=upload, verify=verify)

# 纯文本动态
text = TextDynamic(text="这是文字内容", verify=verify)

# 立即发送动态类
instant = InstantDynamic(draw)

# 定时发送动态类（timestamp是时间戳）
sche = ScheduleDynamic(dynamic=text, timestamp=1111111)

# 发送动态，图片会自动上传
instant.send()

sche.send()
