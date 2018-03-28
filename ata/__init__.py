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


from ata.fs_worker import FSWorker

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
        self.__moduls = {}
        self.__fill_moduls()
        self.__check_import_path()

    def __iter__(self):
        return iter(self.__moduls.items())

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

    def __check_import_path(self):
        FSWorker.check_create(Config().type_paths.get('import'), False)

    def __fill_moduls(self):
        """ ключ, это порядок выполнения"""
        self.__setattr__('q20', FolderUpdateChecker())

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
        self.make_done()


class ArtObject(metaclass=ABCMeta):

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
    # main_init.q20 = FolderUpdateChecker()
    FSWorker.log('Initializer2', main_init.__dict__)

    for item in main_init:
        FSWorker.log((item))


    main_init.start_works()

    FSWorker.log('config4', main_init.__dict__)




if __name__ == '__main__':
    main()






