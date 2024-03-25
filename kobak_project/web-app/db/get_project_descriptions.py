"""
Функция получения названия (описания) проекта по его id
"""

import psycopg2


def get_projects(connect: psycopg2._psycopg.connection, id) -> list:
    try:
        with connect.cursor() as cursor:

            cursor.execute(
                "SELECT description FROM projects WHERE id = %(id)s", {"id": id}
            )
            res: list = [info[0]for info in cursor]

    except Exception as e:
        print(f"Возникла ошибка: {e}")
        raise

    return res
