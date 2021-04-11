from .db import DB
from utils.recommender import Recommender


def get_rate(uid, pid):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute(
        'SELECT rate FROM ratings WHERE uid = %s AND pid = %s', (uid, pid))
    res = c.fetchone()
    c.close()
    conn.close()
    return res


def add_rate(uid, pid, rate):
    conn = DB.get_connection()
    id = DB.generate_random_id()
    c = conn.cursor()
    c.execute(
        'INSERT INTO ratings (id, rate, pid, uid) values (%s, %s, %s, %s)', (id, rate, pid, uid))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    if rate > 3:
        Recommender.increase_score(uid, pid)
    else:
        Recommender.decrease_score(uid, pid)
    return res


def edit_rate(uid, pid, rate):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute(
        'UPDATE ratings SET rate = %s WHERE uid = %s AND pid = %s', (rate, uid, pid))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    if rate > 3:
        Recommender.increase_score(uid, pid)
    else:
        Recommender.decrease_score(uid, pid)
    return res
