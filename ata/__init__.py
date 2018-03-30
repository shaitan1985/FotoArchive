"""
    Решаемые проблемы:
        1. распределение фотографий по датам создания из exif
        2. создание бд хешей для идентивикации уникальности файлов
        3. распределение по разным форматам и хранение в базе связей
        4. создание превью картинок меньшего формата
        extra
        5. создание веб приложения для доступа к превьюшкам
        6. создание гуи для локального просмотра и открытия редакторов
        7. автоматическая закачка файлов со сторонних ресурсов

"""

from abc import ABCMeta, abstractmethod
import json
import os.path as Path
from collections import OrderedDict
from telethon import TelegramClient

from ata.fs_worker import FSWorker
from ata.db_keeper import DBWorker

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Config(object):
    __slots__ = ('__params',)

    def __init__(self):
        self.__params = {}
        self.load_static()

    def __iter__(self):
        return iter(self.__params.items())

    def __getattribute__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            return self.__params.get(key)

    def __setattr__(self, key, value):
        try:
            super().__setattr__(key, value)
        except AttributeError:
            self.__params[key] = value

    def __delattr__(self, key):
        try:
            super().__delattr__(key)
        except AttributeError:
            del self.__params[key]

    def load_static(self):
        path = Path.join(Path.dirname(__file__), '/common/user.json')

        if not Path.exists(path):
            path = Path.join(Path.dirname(__file__), 'common/default.json')
        with open(path) as f:
            tree = json.load(f)
        self.__setattr__('type_paths', tree)

@singleton
class Flags(object):
    __slots__ = ('__params',)

    def __init__(self):
        self.__params = {}
        self.__fill_flags()

    def __iter__(self):
        return iter(self.__params.items())

    def __getattribute__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            return self.__params.get(key)

    def __setattr__(self, key, value):
        try:
            super().__setattr__(key, value)
        except AttributeError:
            self.__params[key] = value

    def __delattr__(self, key):
        try:
            super().__delattr__(key)
        except AttributeError:
            del self.__params[key]

    def __fill_flags(self):
        """ некоторые флаги"""
        self.__setattr__('got_work', False)


@singleton
class Initializer(object):
    __slots__ = ('__moduls', )

    def __init__(self):
        Config()
        self.__moduls = OrderedDict()
        self.__fill_moduls()
        self.__check_start_paths()

    def __iter__(self):
        return iter(sorted(self.__moduls.items()))

    def __getattribute__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            return self.__moduls.get(key)

    def __setattr__(self, key, value):
        try:
            super().__setattr__(key, value)
        except AttributeError:
            self.__moduls[key] = value

    def __delattr__(self, key):
        try:
            super().__delattr__(key)
        except AttributeError:
            del self.__moduls[key]

    def __check_start_paths(self):
        FSWorker.check_create(Config().type_paths.get('import'), False)

    def __fill_moduls(self):
        """ ключ, это порядок выполнения"""
        self.__setattr__('q20', FolderUpdateChecker())
        self.__setattr__('q30', ToArchiveMover())

    def start_works(self):
        FSWorker.log('start_works')
        for key, ex in self:
            FSWorker.log('Now working:', key, ex)
            ex.execute()
        FSWorker.log('ended works')

    def skip_all_done(self):
        for key, ex in self:
            ex.make_undone()
            FSWorker.log(ex, 'made undone')


class TaskExecuterTemplate(metaclass=ABCMeta):

    def __init__(self):
        self.__done = False

    @abstractmethod
    def execute(self):
        pass

    def make_undone(self):
        self.__done = False

    def make_done(self):
        self.__done = True


class TelegaUpdateChecker(TaskExecuterTemplate):

    def __init__(self):
        super().__init__()

    def execute(self):
        api_id = 263724
        api_hash = "3a8ae22a8e6981038a370c7149d51fc2"

        sn_path = Path.join(Path.dirname(__file__), 'session_name')
        client = TelegramClient(sn_path, api_id, api_hash)
        client.connect()
        username = 'shaitan1985'
        try:
            for message in client.get_messages(username, limit=1):
                if not DBWorker.get_telega_id_date(message.id):

                    file = client.download_media(message, Config().type_paths.get('import'))
                    FSWorker.log('From telega was downloaded: "{}"'.format(file))
                    DBWorker.write_telega_id(message.id)
        except Exception as err:
            FSWorker.log("Fucken bitch dead again. BIIIIITCH")



class FolderUpdateChecker(TaskExecuterTemplate):
    """ проверка наличия файлов для обработки"""
    def __init__(self):
        super().__init__()
        FSWorker.log('FolderUpdateChecker started')
        FSWorker.log(Config().type_paths.get('import'))
        self.__import_path = Config().type_paths.get('import')

    def execute(self):
        if self.__got_work():
            Flags().got_work = True
        FSWorker.log('nu kakto tak')
        self.make_done()

    def __got_work(self):
        if FSWorker.get_all_types(self.__import_path):
            FSWorker.log('got work', self.__import_path)
            return True
        return False


class ToArchiveMover(TaskExecuterTemplate):
    def __init__(self):
        super().__init__()
        FSWorker.log('ToArchiveMover started')

    def execute(self):
        """ перенос """
        if not Flags().got_work:
            return
        # проверить папки по типам
        import_path = Path.join(Path.dirname(__file__),
                                                '..',
                                                 Config().type_paths.get('import'))

        self.__check_folders(import_path)
        types = FSWorker.get_all_types(import_path)
        # получить список файлов
        files = FSWorker.get_all_files(import_path)
        # пройти по файлам

        for file, f_type in files.items():
            if f_type not in types:
                continue
            if not FSWorker.check_free_space(file):
                FSWorker.log('For "{}" not enaugh space'.format(file))
                raise Exception
            f_hash = FSWorker.get_hash_md5(file)
            FSWorker.log(f_hash, file)
            if not DBWorker.check_hash(f_hash, file): # проверить хэш
                date = FSWorker.get_born_date(file)
                FSWorker.log('born date of "{}" is "{}"'.format(file, date))
                # создать/проверить папку
                folder = self.__date_to_folder(date, f_type)
                if folder is None:
                    continue
                _, f = Path.split(file)
                src = FSWorker.get_filename(Path.join(folder, f))
                if FSWorker.copy_file(file, src) and FSWorker.check_create(src):
                    # переместить и записать хэш
                    if f_hash == FSWorker.get_hash_md5(src):
                        # запись хэша
                        DBWorker.write_hash(f_hash, src)
                        FSWorker.remove(file)
            else:
                FSWorker.remove(file)

        FSWorker.remove_empty(import_path)


        self.make_done()

    def __date_to_folder(self, date, f_type):
        type_path = Config().type_paths.get(f_type)
        if type_path is not None:
            path = Path.join(Path.dirname(__file__),
                                            '..',
                                            type_path,
                                            str(date.year),
                                            str(date.month),
                                            str(date.day))
            if FSWorker.check_create(path, False):
                return path
        return None


    def __check_folders(self, path):
        for f_type in FSWorker.get_all_types(path):
            folder = Config().type_paths.get(f_type)
            FSWorker.log('type folder', folder)
            if folder is None:
                continue

            FSWorker.log(FSWorker.check_create(Path.join(Path.dirname(__file__),
                                                         '..',
                                                         folder),
                                                        False))


class ArtObject(metaclass=ABCMeta):
    """ Объект фото/исходник/видео"""
    def __init__(self, path):
        self.path = path
        self.type = FSWorker.get_type(path)
        self.archive_path = self.path_from_date()


    def path_from_date(self):
        pass




def main():
    """
        Запуск Наблюдателя(синглтон):
            Наблюдатель работает весь цикл приложения и отследживает события,
            инициализированные при запуске.
        Инициализация:
            * после обработки передает сообщение наблюдателю
            - создание синглтона конфигурации
            - заполнение событиями посредника
            - проверка наличия необходимых ресурсов
                (папка import, jpeg, raw, vid, prew)
                так же необходимо реализовать восстановление бд
                    или подключение к другой базе

            extra
            - наличие установленных приложений (gimp, darktable)
        Запуск проверки наличия новых данных для обработки:
            * после обработки передает сообщение наблюдателю

    """

    config = Config()
    Flags()
    FSWorker.log('config3', config.__dict__)

    main_init = Initializer()
    """ здесь можно добавлять обработчики"""
    main_init.q9 = TelegaUpdateChecker()
    FSWorker.log('Initializer2', main_init.__dict__)

    for item in main_init:
        FSWorker.log((item))


    main_init.start_works()

    FSWorker.log('config4', main_init.__dict__)




if __name__ == '__main__':
    main()






