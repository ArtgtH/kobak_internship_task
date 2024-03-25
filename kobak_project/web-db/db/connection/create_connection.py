import psycopg2
import logging

from psycopg2 import OperationalError

from .db_credentials import user, password, host, port, database


def create_db_connection() -> psycopg2._psycopg.connection | None:

    try:
        connect = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

    except Exception as e:
        print(e)
        raise

    else:
        return connect