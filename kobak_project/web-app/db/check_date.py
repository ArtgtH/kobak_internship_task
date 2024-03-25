"""
Получение даты последнего отчета
"""

import psycopg2


def get_last_date(connect: psycopg2._psycopg.connection, id) -> int:
    try:
        with connect.cursor() as cursor:

            cursor.execute(
                "SELECT report_date FROM reports WHERE staff = %(id)s order by id desc limit 1", {"id": id}
            )

            res = None

            for i in cursor:
                res = i[0]

    except Exception as e:
        print(f"Возникла ошибка: {e}")
        raise e

    return res


# if __name__ == '__main__':
