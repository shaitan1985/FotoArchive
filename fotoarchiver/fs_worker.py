"""
    модуль работы с файловой системой.
    - проверка свободного места
    - наличие фалов/папок
    - перемещение айлов/папок
    - чтение/запись конфигов
    - получение хэша файла

"""
import os

import fleep

from fotoarchiver.logger import log_debug as logger
from fotoarchiver import check_create


def check_free_space(path):
    #проверка свободного места
    st = os.statvfs(path)
    du = st.f_bsize * st.f_bavail

    du = st.f_bsize * st.f_bavail / 1024 / 1024 # кб в мб
    print(du)
import hashlib


def get_hash_md5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192) # размер блока чтения 8 мб
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def get_all_exts(path):
    exts = {}
    for d, dir, files in os.walk(path):
        for f in files:
            _, ext = os.path.splitext(str(f).lower())
            ext = ext.lstrip('.')
            if ext != '':
                exts[ext] = ext
    logger(exts)
    return exts


def check_act_exts(act_exts, path):

    path_exts = get_all_exts(path)
    to_del = []

    for key in path_exts.keys():
        ext = act_exts.get(key.split('_')[0])
        if ext is None:
            logger(key, ext)
            to_del.append(key)
    for i in to_del:
        del path_exts[i]

    return path_exts


def get_all_types(path):
    types = {}
    for d, dir, files in os.walk(path):
        for f in files:
            with open(os.path.join(d, f), "rb") as file:

def get_type(path):
    exts = {}

                info = fleep.get(file.read(128))

                logger(info.extension)






if __name__ == '__main__':
    # logger(check_act_exts(check_create.read_paths(), '/media/huge/foto'))
    get_exts('/media/huge/foto')