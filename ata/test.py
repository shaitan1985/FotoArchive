from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from sys import argv, stderr, exit
import os, time

filename = os.path.join(os.path.dirname(__file__), "video.mp4")
parser = createParser(filename)
if not parser:
    print("Unable to parse file", file=stderr)
    exit(1)

with parser:
    try:
        metadata = extractMetadata(parser)
    except Exception as err:
        print("Metadata extraction error: %s" % err)
        metadata = None
if not metadata:
    print("Unable to extract metadata")
    exit(1)
for line in metadata.exportPlaintext():
    print(line)

stat = os.stat(filename)
try:
    print(time.ctime(stat.st_birthtime))
except AttributeError:
    print(time.ctime(stat.st_mtime))