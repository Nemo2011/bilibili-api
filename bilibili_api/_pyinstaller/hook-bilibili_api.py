from PyInstaller.utils.hooks import collect_data_files
from typing import List, Tuple

datas: List[Tuple[str, str]] = collect_data_files("bilibili_api")
