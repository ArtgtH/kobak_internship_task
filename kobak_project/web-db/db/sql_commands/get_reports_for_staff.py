from db.connection.create_connection import create_db_connection


def get_reports(identificator: int):

    command = """
        select report_date, project, parent_report, time_in_percent from reports \
        inner join report_summands on reports.id = report_summands.parent_report \
        where staff = %s
        order by report_date desc
        """

    conn = create_db_connection()

    with conn.cursor() as cr:
        cr.execute(command, [identificator])

        res = [i for i in cr]

    return res
