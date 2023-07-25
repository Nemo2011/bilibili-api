from typing import List, Tuple

from PyInstaller.utils.hooks import collect_data_files

datas: List[Tuple[str, str]] = collect_data_files("bilibili_api")
