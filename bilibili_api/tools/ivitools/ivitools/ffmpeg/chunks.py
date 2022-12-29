import os


def get_size(path: str):
    size: int = 0
    stream = open(path, "rb")
    while True:
        s: bytes = stream.read(1024)

        if not s:
            break

        size += len(s)
    stream.close()
    return size

def chai(path: str, out1: str, out2: str):
    size = get_size(path)
    stream = open(path, "rb")
    open(out1, "wb+").write(stream.read(size // 2))
    open(out2, "wb+").write(stream.read())
    stream.close()

def hebing(path1: str, path2: str, dest: str):
    if os.path.exists(dest):
        os.remove(dest)
    while True:
        if not os.path.exists(dest):
            break
    stream = open(dest, "wb+")
    stream.write(open(path1, "rb").read())
    stream.write(open(path2, "rb").read())
    stream.close()
