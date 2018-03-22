"""
нужно создать словарь с деревом настроек
1. записать файл настроек
"""
import json

path = 'common/default.json'
settings = {}
paths = {}
types = {}
types['photo'] = 'photo'
types['video'] = 'video'
exts_photo = {}
exts_photo['jpg'] = 'jpg'
exts_photo['raw'] = 'cr2'
exts_photo['prew'] = 'prew'
exts_video = {}
exts_video['mpeg4'] = 'mpg4'
exts_video['mov'] = 'mov'
exts_video['avi'] = 'avi'


paths['input'] = 'hole'
paths['output'] = 'storage'
settings['paths'] = paths
settings['types'] = types
settings['exts_photo'] = exts_photo
settings['exts_video'] = exts_video

with open(path, 'w') as f:
    json.dump(settings, f, indent=4)

with open(path) as f:
    print(json.load(f))
