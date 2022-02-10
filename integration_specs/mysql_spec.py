from mamba import description, context, before, it
from expects import expect, equal, raise_error

import os
from datetime import datetime

from MySQLdb import _exceptions as mysql_exceptions

from infmysql.client import MySQLClient


MYSQL_DB_URI = os.getenv('MYSQL_DB_URI')
TEST_TABLE = 'test_table'


with description('MySQLClientTest') as self:
    with before.each:
        self.mysql_client = MySQLClient(MYSQL_DB_URI)
        self.mysql_client.execute(
            f"DROP TABLE IF EXISTS {TEST_TABLE}"
        )
        self.mysql_client.execute(
            f"CREATE TABLE {TEST_TABLE} (id SERIAL, item varchar(10), size INT, active BOOLEAN, date TIMESTAMP, PRIMARY KEY (id));"
        )
        self.mysql_client.execute(
            f"INSERT INTO {TEST_TABLE} (item, size, active, date) VALUES(%s, %s, %s, %s);",
            ("item_a", 40, False, datetime.fromtimestamp(7300))
        )
        self.mysql_client.execute(
            f"INSERT INTO {TEST_TABLE} (item, size, active, date) VALUES(%s, %s, %s, %s);",
            ("item_b", 20, True, datetime.fromtimestamp(3700))
        )

    with context('FEATURE: execute'):
        with context('happy path'):
            with context('when selecting all rows'):
                with it('returns a tuple containing all values'):
                    query = f"SELECT * FROM {TEST_TABLE}"

                    result = self.mysql_client.execute(query)

                    expect(result).to(equal((
                        (1, 'item_a', 40, 0, datetime.fromtimestamp(7300)),
                        (2, 'item_b', 20, 1, datetime.fromtimestamp(3700)),
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
                with before.each:
                    self.query_delete = f"DELETE FROM {TEST_TABLE} WHERE active = %s;"
                    self.params_delete = (False, )

                with it('returns empty tuple'):

                    result = self.mysql_client.execute(self.query_delete, self.params_delete)

                    expect(result).to(equal(()))

                with it('deletes the row'):

                    self.mysql_client.execute(self.query_delete, self.params_delete)

                    query_select = f"SELECT * FROM {TEST_TABLE}"
                    result_select = self.mysql_client.execute(query_select)
                    expect(result_select).to(equal((
                        (2, 'item_b', 20, 1, datetime.fromtimestamp(3700)),
                    )))

            with context('when inserting a row'):
                with before.each:
                    self.query_insert = f"INSERT INTO {TEST_TABLE}(item, size, active, date) VALUES(%s, %s, %s, %s);"
                    self.query_params = ("item_c", 60, True, datetime.fromtimestamp(9000))

                with it('returns the number of rows'):

                    result = self.mysql_client.execute(self.query_insert, self.query_params)

                    expect(result).to(equal(3))

                with it('inserts the row'):

                    self.mysql_client.execute(self.query_insert, self.query_params)

                    query_select = f"SELECT * FROM {TEST_TABLE}"
                    result_select = self.mysql_client.execute(query_select)
                    expect(result_select).to(equal((
                        (1, 'item_a', 40, 0, datetime.fromtimestamp(7300)),
                        (2, 'item_b', 20, 1, datetime.fromtimestamp(3700)),
                        (3, 'item_c', 60, 1, datetime.fromtimestamp(9000)),
                    )))

            with context('when updating a row'):
                with before.each:
                    self.query_update = f'UPDATE {TEST_TABLE} SET size = size + %s WHERE {TEST_TABLE}.item = %s;'
                    self.params_update = (10, 'item_a')

                with it('returns empty tuple'):

                    result = self.mysql_client.execute(self.query_update, self.params_update)

                    expect(result).to(equal(()))

                with it('updates the row'):

                    self.mysql_client.execute(self.query_update, self.params_update)

                    query_select = f"SELECT item, size FROM {TEST_TABLE}"
                    result_select = self.mysql_client.execute(query_select)
                    expect(result_select).to(equal((
                        ('item_a', 50),
                        ('item_b', 20),
                    )))

        # To see a list of possible exceptions take a look at https://mysqlclient.readthedocs.io/MySQLdb.html#MySQLdb.DataError
        with context('unhappy path'):
            with context('when executing with an invalid column'):
                with it('raises exception from wrapped library'):
                    query = f'UPDATE {TEST_TABLE} SET size = size + %s WHERE {TEST_TABLE}.invalid_column = %s;'
                    params = (10, 'item_a')

                    def _execute_query_with_invalid_column():
                        self.mysql_client.execute(query, params)

                    # https://www.tutorialspoint.com/why-the-hash1054-unknown-column-error-occurs-in-mysql-and-how-to-fix-it
                    expect(_execute_query_with_invalid_column).to(raise_error(mysql_exceptions.OperationalError, 1054))

            with context('when executing with a malformed query'):
                with it('raises exception from wrapped library'):
                    query = f'SELEC * FROM {TEST_TABLE};'

                    def _execute_query_with_a_malformed_query():
                        self.mysql_client.execute(query)

                    expect(_execute_query_with_a_malformed_query).to(raise_error(mysql_exceptions.ProgrammingError, 1064))

