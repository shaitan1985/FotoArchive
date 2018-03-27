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
import logging
from abc import ABCMeta


import fleep


from ata.logger import log_debug as logger


class FSWorker(metaclass=ABCMeta):

    @classmethod
    def check_free_space(cls, path):
        #проверка свободного места
        st = os.statvfs(path)
        du = st.f_bsize * st.f_bavail

        du = st.f_bsize * st.f_bavail / 1024 / 1024 # кб в мб
        print(du)


    @classmethod
    def log(cls, *args):
        log_path = os.path.join(os.path.dirname(__file__), 'debug.log')
        formatt = '[%(levelname)s] %(asctime).19s [%(filename)s_Line:%(lineno)d] %(message)s'

        logging.basicConfig(
            level=logging.DEBUG,
            format=formatt,
            filename=log_path,
            filemode='w'
        )

        logger = logging.getLogger()

        logger.debug(args)

    @classmethod
    def get_hash_md5(cls, file):
        with open(file, 'rb') as f:
            m = hashlib.md5()
            while True:
                data = f.read(8192) # размер блока чтения 8 мб
                if not data:
                    break
                m.update(data)
            return m.hexdigest()

    @classmethod
    def get_type(cls, path):

        with open(path, "rb") as file:
            info = fleep.get(file.read(128))

        if len(info.type):
            return info.type[0]
        return None

    @classmethod
    def get_all_types(cls, path):
        types = []
        for d, dir, files in os.walk(path):
            for f in files:
                tmp_t = cls.get_type(os.path.join(d, f))
                if tmp_t is not None:
                    types.append(tmp_t)

        uniq_t = set(types)
        return uniq_t


    @classmethod
    def check_create(cls, path, file=True):
        if file:
            if not os.path.exists(path):
                return False
        else:
            try:
                os.mkdir(path)
            except OSError:
                pass
        return True






if __name__ == '__main__':
    # logger(check_act_exts(check_create.read_paths(), '/media/huge/foto'))
    FSWorker.get_all_types('.')