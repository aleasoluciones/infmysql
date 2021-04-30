from mamba import description, context, it
from expects import expect, equal

from infmysql.client import MySQLClient

with description('MySQLClient specs') as self:
    with context('changing db_uri'):
        with it('updates db_uri'):
            self.mysql_client = MySQLClient(db_uri=None)

            self.mysql_client.set_db_uri('updated_db_uri')

            expect(self.mysql_client._db_uri).to(equal('updated_db_uri'))
