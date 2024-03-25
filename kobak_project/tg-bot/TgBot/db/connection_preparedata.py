"""
Здесь лежат запросы к БД в формате SQL
"""

import psycopg2
from psycopg2 import sql

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

    except Exception as e:
        print(e)
        raise

    else:
        return connect



def get_tgs(connect: psycopg2._psycopg.connection) -> dict:

    """
    Получаем словарь типа {ФИО: тг-ссылка}
    :param connect: connection for db
    :return: dict(tg_name: full_name)
    """

    command = sql.SQL("SELECT full_name AS names, tg_name AS target_address FROM {}").format(
        sql.Identifier("staff")
    )

    with connect.cursor() as cursor:
        cursor.execute(command)

        res: dict = { tg_name:full_name for full_name, tg_name in cursor}

    return res



def check_person_in_staff_db(curr_user: str) -> bool:
    """
    Соединение двух предыдущих функций;
    Осуществляет проверку вхождения ссылки пользователя в список ссылок из бд
    :param curr_user:
    :return: True/False
    """
    conn = create_connection()
    usernames_directory = get_tgs(conn)

    return curr_user in usernames_directory.keys()








