from mamba import description, context, it
from expects import expect, equal

from mysql_wrapper.client import MySQLClient


with description('MySQLClient specs'):
    with context('changing db_uri'):
        with it('updates db_uri'):
            self.sut = MySQLClient(db_uri=None)

            self.sut.set_db_uri('updated_db_uri')

            expect(self.sut._db_uri).to(equal('updated_db_uri'))
