"""
    модуль работы с файловой системой.
    - проверка свободного места
    - наличие фалов/папок
    - перемещение айлов/папок
    - чтение/запись конфигов
    - получение хэша файла

"""
import os
import hashlib


import fleep


from fotoarchiver.logger import log_debug as logger


class FSWorker(object):

    def check_free_space(path):
        #проверка свободного места
        st = os.statvfs(path)
        du = st.f_bsize * st.f_bavail

        du = st.f_bsize * st.f_bavail / 1024 / 1024 # кб в мб
        print(du)



    def get_hash_md5(filename):
        with open(filename, 'rb') as f:
            m = hashlib.md5()
            while True:
                data = f.read(8192) # размер блока чтения 8 мб
                if not data:
                    break
                m.update(data)
            return m.hexdigest()


    def get_type(file):
        info = fleep.get(file.read(128))

        logger(info.type)

        return info.type


    def get_all_types(path):
        types = {}
        for d, dir, files in os.walk(path):
            for f in files:
                with open(os.path.join(d, f), "rb") as file:
                    f_type = get_type(file)







if __name__ == '__main__':
    # logger(check_act_exts(check_create.read_paths(), '/media/huge/foto'))
    get_all_types('.')