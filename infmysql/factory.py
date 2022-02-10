import os

from infcommon.factory import Factory

from infmysql.client import MySQLClient


def mysql_client(db_uri=None):
    if db_uri is None:
        db_uri = os.getenv("MYSQL_DB_URI")

    return Factory.instance(
        f'mysql_client_{db_uri}',
        lambda: MySQLClient(db_uri)
    )
