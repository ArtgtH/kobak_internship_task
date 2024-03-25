"""
Функция создания подключения к БД
"""

import psycopg2
from .db_creds import db_credentials

def create_connection() -> psycopg2._psycopg.connection | None:
    """
    Создаем связь с БД
    Сейчас указаны данные для подключения к моему серверу postgres на локальном сервере
    """
    try:
        connect = psycopg2.connect(
            user=db_credentials.get("user"),
            password=db_credentials.get("password"),
            host=db_credentials.get("host"),
            port=db_credentials.get("port"),
            database=db_credentials.get("database"),
        )

    except psycopg2.OperationalError as e:
        print(e)
        raise

    else:
        return connect
