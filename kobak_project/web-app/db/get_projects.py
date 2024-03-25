"""
Функция получения id проектов, соответствующих конкретному работнику по его id
"""

import psycopg2


def get_user_projects(connect: psycopg2._psycopg.connection, id) -> list:
    try:
        with connect.cursor() as cursor:

            cursor.execute(
                "SELECT project_id FROM project_staff WHERE staff_id = %(staff_id)s", {"staff_id": id}
            )
            res: list = [info[0]for info in cursor]

    except Exception as e:
        print(f"Возникла ошибка: {e}")
        raise

    return res

