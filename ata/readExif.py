import datetime
import os

import exifread
import enzyme
import hachoir


# path_name = "picture2.jpg"
path_name2 = os.path.join(os.path.dirname(__file__), "video.mp4")
with open(path_name, 'rb') as f:

    tags = exifread.process_file(f)


value = str(tags.get('EXIF DateTimeOriginal'))
print(value)

try:
    date = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    print(type(date), date)
except ValueError:
    pass