from db.connection.create_connection import create_db_connection

def delete_staff(staff_id):

    command = """
    delete from staff where id = %s
    """

    conn = create_db_connection()

    try:
        with conn.cursor() as cr:
            cr.execute(command, [staff_id])
            conn.commit()
    except Exception as e:
        return f'ошибка: {e}'
    else:
        return 'success'
