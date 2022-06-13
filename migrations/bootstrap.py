# Script to bootstrap database
import pymysql

from api.config import (
    DB_ADMIN_USER,
    DB_ADMIN_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

connection = pymysql.connect(
    host=DB_HOST,
    port=int(DB_PORT),
    user=DB_ADMIN_USER,
    password=DB_ADMIN_PASSWORD,
    cursorclass=pymysql.cursors.DictCursor,
)

with connection:
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(DB_NAME))
        cursor.execute(
            "CREATE USER IF NOT EXISTS '{}'@'%' IDENTIFIED BY '{}'".format(
                DB_USER, DB_PASSWORD
            )
        )
        cursor.execute("GRANT ALL ON {}.* TO '{}'@'%'".format(DB_NAME, DB_USER))
    connection.commit()
