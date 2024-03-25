from db.connection.create_connection import create_db_connection


def insert_new_relation(staff_id, project_id):

    command = """
            insert into project_staff(staff_id, project_id) values (%s, %s)
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
