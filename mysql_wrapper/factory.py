import os

from infcommon.factory import Factory
from mysql_wrapper.client import MySQLClient


def mysql_client(db_uri=None):
    if db_uri is None:
        db_uri = os.getenv("LOCAL_DB_URI")

    return Factory.instance('mysql_client_{}'.format(db_uri),
                            lambda: MySQLClient(db_uri)
                            )
