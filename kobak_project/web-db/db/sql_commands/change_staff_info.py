from db.connection.create_connection import create_db_connection


def change_info(staff_id, full_name, tg_name, role, grade):

    command = """
            update staff set 
                full_name = %s,
                tg_name = %s,
                role = %s,
                grade = %s
            where id = %s
            """

    conn = create_db_connection()

    try:
        with conn.cursor() as cr:
            cr.execute(command, (full_name, tg_name, role, grade, staff_id))
            conn.commit()
    except Exception as e:
        return f'ошибка: {e}'
    else:
        return 'success'
