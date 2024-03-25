"""
Функция поиска пользовательского id по его ТГ-ссылке
"""
from typing import Union

import psycopg2
# from connection import create_connection

def get_user_id(connect: psycopg2._psycopg.connection, user) -> Union[int, None]:
    try:
        with connect.cursor() as cursor:

            cursor.execute(
                "SELECT id FROM staff WHERE tg_name = %(tg_name)s", {"tg_name": user}
            )

            res = None

            for i in cursor:
                res = i[0]

    except Exception as e:
        print(f"Возникла ошибка: {e}")
        raise

    return res


# if __name__ == '__main__':
#     connection = create_connection()
#     output = get_user_id(connection, '@ArtemVichuk')
#     print(type(output))
#     print(output)