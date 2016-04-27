# -*- coding: utf-8 -*-
import logging
import sqlite3
from my_finance import settings

logger = logging.getLogger(__name__)

_CONN = None


class DbCursor(object):

    def __init__(self, db_file):
        self.db_file = db_file
        self._cursor = None

    def __enter__(self):
        global _CONN
        if not _CONN:
            _CONN = sqlite3.connect(self.db_file)
        self._cursor = _CONN.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.error('%s: %s' % (exc_type, exc_val))
        try:
            self._cursor.close()
            self._cursor = None
        except:
            pass
        return True


def init():
    with DbCursor(settings.DB_FILE) as cursor, open(settings.DB_SQL_FILE) as sqlfile:
        schema = sqlfile.read()
        cursor.executescript(schema)


def select(sql, parameters=None, is_fetchone=False):
    with DbCursor(settings.DB_FILE) as cursor:
        cursor.execute(sql, parameters)
        if is_fetchone:
            return cursor.fetchone()
        else:
            return cursor.fetchall()


def execute(sql, parameters=None):
    with DbCursor(settings.DB_FILE) as cursor:
        cursor.execute(sql, parameters)
        _CONN.commit()
