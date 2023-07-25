"""
IVITools

A Simple IVI file manager & toolbox.

BY Nemo2011 <yimoxia@outlook.com>

Licensed under the GNU General Public License v3+.
"""
__author__ = "Nemo2011 <yimoxia@outlook.com>"
__license__ = "GPLv3+"

import sys
import platform
import warnings
from typing import List

from colorama import Fore

from .touch import touch_ivi
from .scan import scan_ivi_file
from .extract import extract_ivi
from .download import download_interactive_video


def run_args(command: str, args: List[str]):
    if command == "help":
        print(
            "IVITools - A Simple IVI file manager & toolbox. \n\
BY Nemo2011<yimoxia@outlook.com>\n\
\n\
Commands: download, extract, help, play, scan, touch\n\
\n\
ivitools download [BVID] [OUT]\n\
ivitools extract [IVI]\n\
ivitools help\n\
ivitools play [IVI] (PyQT6 require)\n\
ivitools scan [IVI]\n\
ivitools touch [IVI]"
        )
    if command == "scan":
        scan_ivi_file(args[0])
    elif command == "extract":
        extract_ivi(args[0], args[1])
    elif command == "touch":
        touch_ivi(args[0])
    elif command == "download":
        download_interactive_video(args[0], args[1])
    elif command == "play":
        try:
            import PyQt6
        except ImportError:
            warnings.warn(
                "IVITools Built-in Player require PyQt6 but IVITools can't find it. \nYou can install it by `pip3 install PyQt6`. "
            )
            return
        from .player import main, prepopen

        if len(args) == 0:
            main()
        else:
            prepopen(args[0])
    else:
        raise ValueError("Command not found. Use `ivitools help` for helps. ")


def main():
    if len(sys.argv) == 1:
        print(Fore.YELLOW + "[WRN]: No arguments. " + Fore.RESET)
        print(Fore.YELLOW + "[WRN]: Use `ivitools help` for helps. " + Fore.RESET)
        return
    try:
        args = sys.argv
        run_args(args[1], args[2:])
    except Exception as e:
        print(Fore.RED + "[ERR]: " + str(e) + Fore.RESET)


if __name__ == "__main__":
    main()
