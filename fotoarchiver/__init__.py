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

    def __init__(self, ):
        self.__params = {}

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



class Initializer(object):
    """
    проверка свободного места
    import os
    st = os.statvfs("/home")
    du = st.f_bsize * st.f_bavail
    print(du)
    du = st.f_bsize * st.f_bavail / 1024 / 1024 # в мб
    """


    def __init__(self):





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

    Observer()


    initilizer = Initializer()






