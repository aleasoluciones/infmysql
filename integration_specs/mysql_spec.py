from mamba import description, context, it
from expects import expect, be, have_len, be_above, equal

import os

from infmysql.client import MySQLClient


TEST_TABLE = 'integration_test_table'


with description('Infmysql Specs'):
    with before.each:
        self.mysql_client = MySQLClient(os.getenv("LOCAL_DB_URI"))

        sql_query = "DROP TABLE IF EXISTS {0}".format(TEST_TABLE)
        self.mysql_client.execute(sql_query)

    with context('creating a table'):
        with it('creates'):
            sql_query = "CREATE TABLE {0} (value varchar(10))".format(TEST_TABLE)
            result = self.mysql_client.execute(sql_query)

            expect(result).to(be(tuple()))

    with context('making a query with results'):
        with it('returns it'):
            sql_query = "SELECT * FROM mysql.user WHERE User=%s"

            result = self.mysql_client.execute(sql_query, ['root'])

            expect(result).to(have_len(be_above(0)))

    with context('making a query with no results'):
        with it('returns empty'):
            sql_query = "SELECT * FROM mysql.user WHERE User=%s"

            result = self.mysql_client.execute(sql_query, ['non-existing-user'])

            expect(result).to(have_len(be(0)))

    with context('inserting value into table'):
        with it('returns inserted primary key id'):
            self.mysql_client.execute("CREATE TABLE {0} (id int not null auto_increment, value varchar(10), primary key (id))".format(TEST_TABLE))

            result = self.mysql_client.execute("INSERT INTO {0}(value) VALUES(%s)".format(TEST_TABLE), ("foo",))

            expect(result).to(equal(1))
