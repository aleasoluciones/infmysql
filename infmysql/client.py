from urllib.parse import urlparse
import warnings

import MySQLdb
from MySQLdb.cursors import Cursor
from retrying import retry

MySQLDBExceptionError = MySQLdb.Error

class MySQLClient:
    def __init__(self, db_uri, cursor_factory=Cursor):
        self._db_uri = db_uri
        self._cursor_factory = cursor_factory

    def set_db_uri(self, db_uri):
        self._db_uri = db_uri

    @retry(wait_exponential_multiplier=1000,
           wait_exponential_max=10000,
           stop_max_attempt_number=5,
           retry_on_exception=lambda e: isinstance(e, MySQLdb.Error))
    def execute(self, sql_query, args=None):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with self._connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql_query, args)
                    result_rows = cursor.fetchall()
                    last_insert_id = connection.insert_id()
                    if len(result_rows) == 0 and last_insert_id != 0:
                        return last_insert_id
                    return result_rows

    def _connection(self):
        uri = urlparse(self._db_uri)
        return MySQLdb.connect(uri.hostname,
                               uri.username,
                               uri.password,
                               uri.path[1:],
                               port=int(uri.port) if uri.port else 3306,
                               use_unicode=True,
                               charset='utf8',
                               cursorclass=self._cursor_factory,
                               autocommit=True,
                               connect_timeout=5)
