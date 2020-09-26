from .db import DB

db = DB.db


def user_info(id):
    c = db.cursor(dictionary=True)
    c.execute('SELECT id, firstname, lastname, email, image FROM users WHERE id = %s', (id,))
    res = c.fetchall()[0]
    c.close()
    return res


def change_user_info(id, firstname, lastname):
    c = db.cursor()
    c.execute('UPDATE users SET firstname = %s, lastname = %s WHERE id = %s',
        (firstname, lastname, id)
    )
    res = c.rowcount
    db.commit()
    c.close()
    return res


def change_profile_image(id, image):
    c = db.cursor()
    c.execute('UPDATE users SET image = %s WHERE id = %s', (image, id))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def change_password(id, password):
    c = db.cursor()
    c.execute('UPDATE users SET password = %s WHERE id = %s', (password, id))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def get_user_password(id):
    c = db.cursor(dictionary=True)
    c.execute('SELECT password FROM users WHERE id = %s', (id,))
    res = c.fetchall()[0]
    db.commit()
    c.close()
    return res
