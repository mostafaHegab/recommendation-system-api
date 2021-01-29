from .db import DB
db = DB.db


def get_rate(uid, pid):
    c = db.cursor(dictionary=True)
    c.execute(
        'SELECT rate FROM ratings WHERE uid = %s AND pid = %s', (uid, pid))
    res = c.fetchone()
    c.close()
    return res

def add_rate(uid, pid, rate):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute(
        'INSERT INTO ratings (id, rate, pid, uid) values (%s, %s, %s, %s)', (id, rate, pid, uid))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def edit_rate(uid, pid, rate):
    c = db.cursor()
    c.execute('UPDATE ratings SET rate = %s WHERE uid = %s AND pid = %s', (rate, uid, pid))
    res = c.rowcount
    db.commit()
    c.close()
    return res
