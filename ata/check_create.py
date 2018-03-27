"""
нужно создать словарь с деревом настроек
1. записать файл настроек
"""
import json
import os.path as Path

from ata.fs_worker import FSWorker





def read_paths():
    path = 'common/user.json'

    if not Path.exists(path):

        path = 'common/default.json'
        type_paths = {}

        type_paths['raster-image'] = Path.join('storage', 'photo', 'raster-image')
        type_paths['raw-image'] = Path.join('storage', 'photo', 'raw-image')
        type_paths['video'] = Path.join('storage', 'video')

        type_paths['preview'] = Path.join('storage', 'photo', 'preview')
        type_paths['import'] = Path.join('import')





        with open(path, 'w') as f:
            json.dump(type_paths, f, indent=4)

    with open(path) as f:
        tree = json.load(f)

    return tree


if __name__ == '__main__':
    with open('common/default.json', 'w') as f:
        pass

    FSWorker.log(read_paths())

# os.mkdir(paths['video'], mode=0o777, *, dir_fd=None)
