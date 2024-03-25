from db.connection.create_connection import create_db_connection


def get_all_logins_passwords():

    command = """
        select login, password from managers
        """

    conn = create_db_connection()

    with conn.cursor() as cr:
        cr.execute(command)

        res = [i for i in cr]

    return res
