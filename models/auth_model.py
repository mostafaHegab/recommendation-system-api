from .db import DB
db = DB.db


def create_user(firstname, lastname, email, password, verified, image):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute(
        'INSERT INTO users (id, firstname, lastname, email, password, verified, image) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (id, firstname, lastname, email, password, verified, image)
    )
    res = c.rowcount
    db.commit()
    c.close()
    return res


def find_user(email):
    c = db.cursor(dictionary=True)
    c.execute('SELECT id, firstname, lastname, email, password, image, verified FROM users WHERE email = %s', (email,))
    res = c.fetchall()
    c.close()
    return res


def get_verification_code(email):
    c = db.cursor(dictionary=True)
    c.execute('SELECT id, verified FROM users WHERE email = %s', (email,))
    res = c.fetchall()
    c.close()
    return res


def verify_account(id):
    c = db.cursor()
    c.execute('UPDATE users SET verified = 0 WHERE id = %s', (id,))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def set_reset_code(id, code):
    c = db.cursor()
    c.execute('UPDATE users SET reset_code = %s WHERE id = %s', (code, id))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def get_reset_code(email):
    c = db.cursor(dictionary=True)
    c.execute('SELECT id, reset_code FROM users WHERE email = %s', (email,))
    res = c.fetchall()
    c.close()
    return res


def reset_password(id, password):
    c = db.cursor()
    c.execute('UPDATE users SET password = %s, reset_code = 0 WHERE id = %s', (password, id))
    res = c.rowcount
    db.commit()
    c.close()
    return res
