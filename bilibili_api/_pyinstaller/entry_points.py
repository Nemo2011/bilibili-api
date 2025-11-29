import os


def get_hook_dirs() -> list[str]:
    return [os.path.abspath(os.path.dirname(__file__))]
