from db.connection.create_connection import create_db_connection


def insert_new_project_in_db(description):

    command = """
            insert into projects(description) values (%s)
            """

    conn = create_db_connection()

    try:
        with conn.cursor() as cr:
            cr.execute(command, [description])
            conn.commit()
    except Exception as e:
        return f'ошибка: {e}'
    else:
        return 'success'
