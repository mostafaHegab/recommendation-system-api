from .db import DB
db = DB().db


def add_rate(rate, pid, uid):
    c = db.cursor()
    c.execute(f'INSERT INTO ratings (rate, pid, uid) values ({rate}, {pid}, {uid})')
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


def add_comment(text, time, pid, uid):
    c = db.cursor()
    c.execute(f'INSERT INTO comments (text, time, pid, uid) values ("{text}", "{time}", {pid}, {uid})')
    res = c.rowcount
    db.commit()
    c.close()
    return res


def edit_comment(id, text):
    c = db.cursor()
    c.execute(f'UPDATE comments SET text = "{text}" WHERE id = {id}')
    res = c.rowcount
    db.commit()
    c.close()
    return res


def delete_comment(id):
    c = db.cursor()
    c.execute(f'DELETE FROM comments where id = {id}')
    res = c.rowcount
    db.commit()
    c.close()
    return res