import os

from MySQLdb.cursors import Cursor, DictCursor

from infcommon.factory import Factory

from infmysql.client import MySQLClient


def mysql_client(db_uri=None, use_dict_cursor=False):
    if db_uri is None:
        db_uri = os.getenv("MYSQL_DB_URI")

    cursor_factory = _cursor_factory(use_dict_cursor)
    return Factory.instance(
        f'mysql_client_{db_uri}_{use_dict_cursor}',
        lambda: MySQLClient(db_uri, cursor_factory=cursor_factory),
    )


def _cursor_factory(use_dict_cursor=False):
    if use_dict_cursor:
        return DictCursor
    return Cursor
