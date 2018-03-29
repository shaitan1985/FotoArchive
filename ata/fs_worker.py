"""
    модуль работы с файловой системой.
    - проверка свободного места
    - наличие файлов/папок
    - перемещение файлов/папок
    - чтение/запись конфигов
    - получение хэшей файла

"""
import os
import hashlib
import logging
import datetime
import shutil
from abc import ABCMeta, abstractmethod


import fleep
import exifread
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

class FSWorker(metaclass=ABCMeta):

    @abstractmethod
    def __never_born(self):
        pass

    @classmethod
    def check_free_space(cls, path):
        #проверка свободного места
        st = os.statvfs(path)
        du = st.f_bsize * st.f_bavail

        du = st.f_bsize * st.f_bavail / 1024 / 1024 # кб в мб
        cls.log(du)


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
    def get_born_date(cls, path):
        f_type = cls.get_type(path)
        date = None
        if f_type == 'raster-image':
            date = cls.__date_from_exif(path)
        elif f_type == 'video':
            date = cls.__date_from_videometa(path)
        elif f_type == 'raw-image':
            date = cls.__date_from_raw(path)
        if date is None:
            date = cls.__get_date_from_file(path)

        return date

    @classmethod
    def __date_from_raw(cls):
        pass

    @classmethod
    def __get_date_from_file(cls, path):
        t = os.path.getmtime(path)
        return datetime.datetime.fromtimestamp(t)

    @classmethod
    def __date_from_videometa(cls, path):
        """достать дату из видео"""
        if True:
            return None
        # Пока заглушка
        parser = createParser(path)
        if not parser:
            cls.log('Unable to parse file "{}"'.format(path))
            return None

        with parser:
            try:
                metadata = extractMetadata(parser)
            except Exception as err:
                cls.log("Metadata extraction error: {}".format(err))
                metadata = None
        if not metadata:
            cls.log("Unable to extract metadata")
            return None
        for line in metadata.exportPlaintext():
            cls.log(line)



    @classmethod
    def __date_from_exif(cls, path):

        with open(path, 'rb') as f:

            tags = exifread.process_file(f)

        value = str(tags.get('EXIF DateTimeOriginal'))

        try:
            date = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except ValueError:
            return None
        return date


    @classmethod
    def get_all_types(cls, path):
        types = []
        for d, dir, files in os.walk(path):
            for f in files:
                tmp_t = cls.get_type(os.path.join(d, f))
                if tmp_t is not None:
                    types.append(tmp_t)

        uniq_t = set(types)
        cls.log(uniq_t)
        return uniq_t

    @classmethod
    def get_all_files(cls, path):
        d_files = {}
        for d, dir, files in os.walk(path):
            for f in files:
                f_path = os.path.join(d, f)
                tmp_t = cls.get_type(f_path)
                if tmp_t is not None:
                    d_files[f_path] = tmp_t
        return d_files

    @classmethod
    def check_create(cls, path, file=True):
        if file:
            if not os.path.exists(path):
                return False
        else:
            try:
                os.makedirs(path)
            except OSError as err:
                cls.log(err)
        return True

    @classmethod
    def copy_file(cls, src, dst):
        try:
            shutil.copy2(src, dst)
            return True
        except IOError as err:
            cls.log('Возникла ошибка при копировании "{}"', src, err, )
        return False










if __name__ == '__main__':
    # logger(check_act_exts(check_create.read_paths(), '/media/huge/foto'))
    FSWorker.get_all_types('.')
