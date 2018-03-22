import exifread
import datetime


path_name = "picture2.jpg"
with open(path_name, 'rb') as f:

    tags = exifread.process_file(f)


value = str(tags.get('EXIF DateTimeOriginal'))
print(value)

try:
    date = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    print(type(date), date)
except ValueError:
    pass