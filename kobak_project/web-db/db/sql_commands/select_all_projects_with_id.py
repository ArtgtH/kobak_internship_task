from db.connection.create_connection import create_db_connection

from psycopg2 import sql


def select_all_projects_with_id():

    command = sql.SQL("SELECT id, description FROM {}").format(
        sql.Identifier("projects")
    )

    conn = create_db_connection()

    with conn.cursor() as cr:
        cr.execute(command)

        res = [i for i in cr]

    return res
