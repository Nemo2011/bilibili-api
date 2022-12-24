import os
import subprocess
import sys


def get_python_command():
    """
    Get the python command. (python or python3)

    Returns:
        str: python command
    """
    try:
        subprocess.Popen(
            "python",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception:
        pass
    else:
        return "python"
    try:
        subprocess.Popen(
            "python3",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception:
        pass
    else:
        return "python3"


curdir = os.path.dirname(os.path.abspath(__file__))
mplayer_dir = os.path.join(curdir, "mplayer", "__main__.py")
sys.exit(os.system(f"{get_python_command()} {mplayer_dir}"))
