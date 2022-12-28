import zipfile
import os

zip = zipfile.ZipFile("MPlayer.zip", "w", zipfile.ZIP_DEFLATED)
for path, dirnames, filenames in os.walk("MPlayer"):
    fpath = path.replace("MPlayer", '')

    for filename in filenames:
        zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
zip.close()
