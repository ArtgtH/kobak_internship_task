"""
Функция получения id всех проектов из БД
"""

import psycopg2


def get_all_projects(connect: psycopg2._psycopg.connection) -> list:
        try:
            with connect.cursor() as cursor:

                cursor.execute(
                    "SELECT id FROM projects", {"staff_id": id}
                )
                res: list = [info[0] for info in cursor]

        except Exception as e:
            print(f"Возникла ошибка: {e}")
            raise

        return res
