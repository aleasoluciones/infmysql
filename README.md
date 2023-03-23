# infmysql

[![CI](https://github.com/aleasoluciones/infmysql/actions/workflows/ci.yml/badge.svg)](https://github.com/aleasoluciones/infmysql/actions/workflows/ci.yml)
![Python versions supported](https://img.shields.io/badge/supports%20python-3.9%20|%203.10%20|%203.11-blue.svg)

Wrapper for the [mysqlclient](https://mysqlclient.readthedocs.io) library using Python 3.

## Development

### Setup

Create a virtual environment, install dependencies and load environment variables.

```python
mkvirtualenv infmysql -p $(which python3)
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

The client can be initialized using the factory with a database URI and an optional parameter which determines if we want to use a dict cursor (false by default).

> mysql_client = factory.**mysql_client**(*database_uri*, *use_dict_cursor=False*)

### execute()

Executes a SQL query and returns the result. Passing parameters is possible by using `%s` placeholders in the SQL query, and passing a sequence of values as the second argument of the function.

> mysql_client.**execute**(*query*, *params*)

➡️ Parameters

- **query**: `str`
- **params** (optional): `tuple<any>`. Defaults to `None`.

⬅️ Returns a tuple of tuples or dictionaries, each containing a row of results.

`tuple<tuple<any>>`

💥 Throws the same exceptions than the mysqlclient library.

#### Usage example

```python
from infmysql import factory

mysql_client = factory.mysql_client('mysql://username:password@host:port/databasename')

sql_query = 'SELECT (name, surname, age) FROM users WHERE age < %s AND active = %s;'
params = (30, True, )

result = mysql_client.execute(sql_query, params)

# (
#   ('Ann', 'White', 18, ),
#   ('Axel', 'Schwarz', 21, ),
#   ('Camille', 'Rouge', '27', ),
# )
```

#### Usage example with dict cursor

```python
from infmysql import factory

mysql_client = factory.mysql_client('mysql://username:password@host:port/databasename', use_dict_cursor=True)

sql_query = 'SELECT (name, surname, age) FROM users WHERE age < %s AND active = %s;'
params = (30, True, )

result = mysql_client.execute(sql_query, params)

# (
#   {'name': 'Ann', 'surname': 'White', 'age': 18},
#   {'name': 'Axel', 'surname': 'Schwarz', 'age': 21},
#   {'name': 'Camille', 'surname': 'Rouge', 'age': 27},
# )
```
