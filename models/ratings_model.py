from .db import DB
db = DB.db


def add_rate(rate, pid, uid):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute(
        'INSERT INTO ratings (id, rate, pid, uid) values (%s, %s, %s, %s)', (id, rate, pid, uid))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def edit_rate(id, rate):
    c = db.cursor()
    c.execute('UPDATE ratings SET rate = %s WHERE id = %s', (rate, id))
    res = c.rowcount
    db.commit()
    c.close()
    return res
