from db.connection.create_connection import create_db_connection

from psycopg2 import sql


def select_all_staff_from_db():

    command = sql.SQL("SELECT id, full_name, tg_name, role, grade FROM {}").format(
        sql.Identifier("staff")
    )

    conn = create_db_connection()

    with conn.cursor() as cr:
        cr.execute(command)

        res = [i for i in cr]

    return res
