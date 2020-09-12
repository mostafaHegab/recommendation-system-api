from .db import DB
db = DB().db


def add_rate(rate, pid, uid):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute(
        f'INSERT INTO ratings (id, rate, pid, uid) values ({id}, {rate}, {pid}, {uid})')
    res = c.rowcount
    db.commit()
    c.close()
    return res


def edit_rate(id, rate):
    c = db.cursor()
    c.execute(f'UPDATE comments SET rate = {rate} WHERE id = {id}')
    res = c.rowcount
    db.commit()
    c.close()
    return res
