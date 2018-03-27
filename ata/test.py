def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Registry(object):
    __slots__ = ('__params',)

    def __init__(self):
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


r = Registry()
r2 = Registry()


r.db_host = 'localhost'
r2.db_user = 'root'
print(r.__dir__())
for key, value in r:
    print(key, value)