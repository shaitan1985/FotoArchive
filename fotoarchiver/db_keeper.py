"""
    модуль работы с базой данных
    1. Инициализация БД
    2. запись хэша
    3. возврат хэша при наличии
    4. запись связей
    5. получение связных путей
"""

"""
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
"""