from db.connection.create_connection import create_db_connection


def delete_relation(staff_id, project_id):

    command = """
            delete from project_staff where staff_id = %s and project_id = %s
            """

    conn = create_db_connection()

    try:
        with conn.cursor() as cr:
            cr.execute(command, [staff_id, project_id])
            conn.commit()
    except Exception as e:
        return f'ошибка: {e}'
    else:
        return 'success'
