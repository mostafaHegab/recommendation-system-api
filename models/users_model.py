from .db import DB


def user_info(id):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT id, firstname, lastname, email, image FROM users WHERE id = %s', (id,))
    res = c.fetchall()[0]
    c.close()
    conn.close()
    return res


def change_user_info(id, firstname, lastname):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET firstname = %s, lastname = %s WHERE id = %s',
        (firstname, lastname, id)
    )
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res


def change_profile_image(id, image):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET image = %s WHERE id = %s', (image, id))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res


def change_password(id, password):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET password = %s WHERE id = %s', (password, id))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res


def get_user_password(id):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT password FROM users WHERE id = %s', (id,))
    res = c.fetchall()[0]
    conn.commit()
    c.close()
    conn.close()
    return res
