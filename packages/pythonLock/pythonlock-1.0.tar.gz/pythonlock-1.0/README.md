# python-distributed-lock module

This Python package provides a mechanism to acquire and release Redis and MYSQL locks with authentication. It is useful for ensuring that only one process can access a particular resource or execute a critical section of code at a time.

## Features
- Connects to Redis or MySQL with username and password for authentication.
- Acquires a lock, executes a function, and then releases the lock.
- Useful in distributed systems where resource locking is needed.

## Installation

To install the module, use `pip`:

```
pip install pythonLock
```
# Please check your database connection before passing it to module
## use with mysql lock
```

from pythonLock import start_cron_with_expression

mysql_user = "root"
mysql_pass = "root"
mysql_host = "localhost"
mysql_database = "mysql"

connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_pass,
    database=mysql_database,
    pool_name="mypool",
    pool_size=3
)

cron_expression = "* */5 * * *"  # Runs every 5 minute
start_cron_with_expression(connection, my_custom_function, cron_expression,"mysql")


def my_custom_function():
    # add whatever action you want in your custom function
    pass
```

## use with redis lock
```

from pythonLock import start_cron_with_expression

redis_host = "localhost"
redis_port = 6379
redis_username = "default"
redis_password = "root"

# Connect to Redis with username and password
connection = redis.StrictRedis(
    host=redis_host,
    port=redis_port,
    username=redis_username,
    password=redis_password,
    decode_responses=True
)

cron_expression = "* */5 * * *"  # Runs every 5 minute
start_cron_with_expression(connection, my_custom_function, cron_expression,"redis")


def my_custom_function():
    # add whatever action you want in your custom function
    pass

```
