# infmysql

[![Build status](https://travis-ci.com/aleasoluciones/infmysql.svg?branch=master)](https://travis-ci.com/aleasoluciones/infmysql)

Wrapper for the [mysqlclient](https://mysqlclient.readthedocs.io) library using Python 3.7.

## Development

### Setup

Create a virtual environment, install dependencies and load environment variables.

```python
mkvirtualenv infmysql -p $(which python3.7)
dev/setup_venv.sh
source dev/env_develop
```

Run a MySQL Docker container.

```python
dev/start_local_dependencies.sh
```

### Running tests, linter & formatter and configure git hooks

Note that project uses Alea's [pydevlib](https://github.com/aleasoluciones/pydevlib), so take a look at its README to see the available commands.

## infmysql client API

Below is described the public API that this library provides.

### \_\_init\_\_()

The client must be initialized with a database URI.

> mysql_client = **MySQLClient**(*database_uri*)

### execute()

Executes a SQL query and returns the result. Passing parameters is possible by using `%s` placeholders in the SQL query, and passing a sequence of values as the second argument of the function.

> mysql_client.**execute**(*sql_query*, *args*)

➡️ Parameters

- **sql_query**: `str`
- **args** (optional): `tuple<any>`. Defaults to `None`.

⬅️ Returns a tuple of tuples, each containing a row of results.

`tuple<tuple<any>>`

💥 Throws the same exceptions than the mysqlclient library.

#### Usage example

```python
from infmysql.client import MySQLClient

mysql_client = MySQLClient('mysql://username:password@host:port/databasename')

sql_query = 'SELECT (name, surname, age) FROM users WHERE age < %s AND active = %s;'
params = (30, True, )

result = mysql_client.execute(sql_query, params)

# (('Ann', 'White', 18, ), ('Axel', 'Schwarz', 21, ), ('Camille', 'Rouge', '27', ), )
```
