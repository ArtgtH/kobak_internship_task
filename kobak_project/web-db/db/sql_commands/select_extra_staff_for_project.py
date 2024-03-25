from db.connection.create_connection import create_db_connection
from psycopg2 import sql


def select_extra_staff_for_projects(project_name):

    command = """
    select staff.full_name from extra_report_summands
    inner join reports on extra_report_summands.parent_report = reports.id
    inner join projects on extra_report_summands.project = projects.id
    inner join staff on reports.staff = staff.id
    where projects.description = %s
    """



    conn = create_db_connection()

    with conn.cursor() as cr:
        cr.execute(command, [project_name])

        res = list(set([i for i in cr]))

    return res
