from db.connection.create_connection import create_db_connection


def insert_new_staff_in_db(name, tg, role, grade):

    command = """
            insert into staff(full_name, tg_name, role, grade) values (%s, %s, %s, %s)
            """

    conn = create_db_connection()

    try:
        with conn.cursor() as cr:
            cr.execute(command, [name, tg, role, grade])
            conn.commit()
    except Exception as e:
        return f'ошибка: {e}'
    else:
        return 'success'
