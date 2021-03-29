from urllib.parse import urlparse
import warnings

import MySQLdb
from retrying import retry

MySQLDBExceptionError = MySQLdb.Error


class MySQLClient:
    def __init__(self, db_uri):
        self._db_uri = db_uri

    def set_db_uri(self, db_uri):
        self._db_uri = db_uri

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5, retry_on_exception=lambda e: isinstance(e, MySQLdb.Error))
    def execute(self, sql_query, args=None):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            return self._execute(sql_query, args)

    def _execute(self, sql_query, args):
        connection = None
        cursor = None

        uri = urlparse(self._db_uri)
        try:
            connection = MySQLdb.connect(uri.hostname,
                                            uri.username,
                                            uri.password,
                                            uri.path[1:],
                                            port=int(uri.port) if uri.port else 3306,
                                            use_unicode=True,
                                            charset='utf8',
                                            connect_timeout=5)
            connection.autocommit(True)
            cursor = connection.cursor()
            cursor.execute(sql_query, args)
            result_rows = cursor.fetchall()

            last_insert_id = connection.insert_id()
            if len(result_rows) == 0 and last_insert_id != 0:
                return last_insert_id
            return result_rows
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
