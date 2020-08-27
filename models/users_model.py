from .db import DB
db = DB().db


def user_info(id):
    c = db.cursor(dictionary=True)
    c.execute(f'SELECT id, firstname, lastname, email, image FROM users WHERE id = {id}')
    res = c.fetchall()[0]
    c.close()
    return res


def change_user_info(id, firstname, lastname):
    c = db.cursor()
    c.execute(f'UPDATE users SET firstname = "{firstname}", lastname = "{lastname}" WHERE id = {id}')
    res = c.rowcount
    db.commit()
    c.close()
    return res


def change_profile_image(id, image):
    c = db.cursor()
    c.execute(f'UPDATE users SET image = "{image}" WHERE id = {id}')
    res = c.rowcount
    db.commit()
    c.close()
    return res


def change_password(id, password):
    c = db.cursor()
    c.execute(f'UPDATE users SET password = "{password}" WHERE id = {id}')
    res = c.rowcount
    db.commit()
    c.close()
    return res
