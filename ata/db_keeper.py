"""
    модуль работы с базой данных
    1. Инициализация БД
    2. запись хэша
    3. возврат хэша при наличии
    4. запись связей
    5. получение связных путей
"""
from abc import ABCMeta, abstractmethod
from datetime import datetime
import os

from pony.orm import (
    Database,
    Required, Optional, Set, PrimaryKey,
    LongStr,
    db_session, select, JOIN,
    desc)


from ata.fs_worker import FSWorker


db_path = os.path.join('common', 'db.sqlite' )
db = Database('sqlite', db_path, create_db=True)

class ArtObject(db.Entity):
    id = PrimaryKey(str, 32)
    path = Required(str)
    f_type = Required(str, 50)
    ext = Required(str)
    preview = Optional(str)


class TelegaMessaga(db.Entity):
    id = PrimaryKey(int, auto=True)
    telega_id = Required(int, size=16)
    date = Optional(datetime, default=lambda: datetime.now())

db.generate_mapping(create_tables=True)

class DBWorker(metaclass=ABCMeta):

    @abstractmethod
    def __never_born(self):
        pass

    @classmethod
    def write_telega_id(cls, t_id):
        with db_session:
            TelegaMessaga(telega_id=t_id)

    @classmethod
    def get_telega_id_date(cls, t_id):
        with db_session:
            obj_id = TelegaMessaga.get(telega_id=t_id)
            if obj_id is None:
                return False
        return True

    @classmethod
    def get_last_id_date(cls):
        try:
            date = TelegaMessaga.select().order_by(desc(TelegaMessaga.date))[:1][0]
        except Exception:
            date = datetime(2007, 12, 6)
        return date

    @classmethod
    def write_hash(cls, f_hash, path, preview=''):
        with db_session:
            obj = ArtObject(id=f_hash,
                            path=path,
                            f_type=FSWorker.get_type(path),
                            ext=FSWorker.get_ext(path),
                            preview=preview
                            )


    @classmethod
    def check_hash(cls, f_hash, file):
        with db_session:
            FSWorker.log('DB object', file)
            obj = ArtObject.get(id=f_hash)
            if obj is None:
                return False
        return True




