from db.connection.create_connection import create_db_connection
from psycopg2 import sql


def select_all_staff_projects_with_relations():

    command = sql.SQL("select full_name, description from {} \
    inner join staff on project_staff.staff_id = staff.id \
    inner join projects on project_staff.project_id = projects.id").format(sql.Identifier("project_staff"))

    conn = create_db_connection()

    with conn.cursor() as cr:
        cr.execute(command)

        res = [i for i in cr]

    return res
