"""
    модуль работы с файловой системой.
    - проверка свободного места
    - наличие фалов/папок
    - перемещение айлов/папок
    - чтение/запись конфигов
    - получение хэша файла

"""
import os

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


if __name__ == '__main__':

    print(get_hash_md5('logger.py'))
