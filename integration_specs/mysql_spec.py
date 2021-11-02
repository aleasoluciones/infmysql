from mamba import description, context, before, it
from expects import expect, equal, raise_error

import os
from datetime import datetime, timezone

from MySQLdb import _exceptions as mysql_exceptions

from infmysql.client import MySQLClient


MYSQL_DB_URI = os.getenv('MYSQL_DB_URI')
TEST_TABLE = 'test_table'


with description('MySQLClientTest') as self:
    with before.each:
        self.mysql_client = MySQLClient(MYSQL_DB_URI)
        self.mysql_client.execute(f"DROP TABLE IF EXISTS {TEST_TABLE}")
        self.mysql_client.execute(f"CREATE TABLE {TEST_TABLE} (id SERIAL, item varchar(10), size INT, active BOOLEAN, date TIMESTAMP, PRIMARY KEY (id));")
        self.mysql_client.execute(f"INSERT INTO {TEST_TABLE}(item, size, active, date) VALUES(%s, %s, %s, %s);", ("item_a", 40, False, datetime.fromtimestamp(7300, tz=timezone.utc)))
        self.mysql_client.execute(f"INSERT INTO {TEST_TABLE}(item, size, active, date) VALUES(%s, %s, %s, %s);", ("item_b", 20, True, datetime.fromtimestamp(3700, tz=timezone.utc)))

    with context('FEATURE: execute'):
        with context('happy path'):
            with context('when selecting all rows'):
                with it('returns a tuple containing all values'):
                    query = f"SELECT * FROM {TEST_TABLE}"

                    result = self.mysql_client.execute(query)

                    expect(result).to(equal((
                        (1, 'item_a', 40, 0, datetime(1970, 1, 1, 2, 1, 40)),
                        (2, 'item_b', 20, 1, datetime(1970, 1, 1, 1, 1, 40))
                    )))

            with context('when counting rows'):
                with it('returns number of values'):
                    query = f"SELECT COUNT(*) FROM {TEST_TABLE}"

                    result = self.mysql_client.execute(query)

                    expect(result[0][0]).to(equal(2))

            with context('when selecting non-existing rows'):
                with it('returns empty tuple'):
                    query = f"SELECT * FROM {TEST_TABLE} WHERE size > %s;"
                    params = (50, )

                    result = self.mysql_client.execute(query, params)

                    expect(result).to(equal(()))

            with context('when deleting a row'):
                with it('returns empty tuple'):
                    query = f"DELETE FROM {TEST_TABLE} WHERE active = %s;"
                    params = (False, )

                    result = self.mysql_client.execute(query, params)

                    expect(result).to(equal(()))

            with context('when inserting a row'):
                with it('returns the number of rows'):
                    query = f"INSERT INTO {TEST_TABLE}(item, size, active, date) VALUES(%s, %s, %s, %s);"
                    params = ("item_c", 60, True, datetime.fromtimestamp(11000))

                    result = self.mysql_client.execute(query, params)

                    expect(result).to(equal(3))

            with context('when updating a row'):
                with it('returns empty tuple'):
                    query = f'UPDATE {TEST_TABLE} SET size = size + %s WHERE {TEST_TABLE}.item = %s;'
                    params = (10, 'item_a')

                    result = self.mysql_client.execute(query, params)

                    expect(result).to(equal(()))

        with context('unhappy path'):
            with context('when executing a malformed query'):
                with it('raises exception from wrapped library'):
                    malformed_query = f'UPDATE {TEST_TABLE} SET size = size + %s WHERE {TEST_TABLE}.invalid_column = %s;'
                    params = (10, 'item_a')

                    def _execute_query_with_invalid_column():
                        self.mysql_client.execute(malformed_query, params)

                    # https://www.tutorialspoint.com/why-the-hash1054-unknown-column-error-occurs-in-mysql-and-how-to-fix-it
                    expect(_execute_query_with_invalid_column).to(raise_error(mysql_exceptions.OperationalError, 1054))
