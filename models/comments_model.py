from .db import DB
from utils.sentiment_analyzer import sentiment_analyzer
from utils.recommender import Recommender
import datetime


def add_comment(text, time, uid, pid):
    id = DB.generate_random_id()
    sa = sentiment_analyzer(text)
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO comments (id, text, time, uid, pid, sentiment_analysis) values (%s, %s, %s, %s, %s, %s)',
        (id, text, time, uid, pid, int(sa)))
    conn.commit()
    c.close()
    conn.close()
    if sa == 1:
        Recommender.increase_score(uid, pid)
    else:
        Recommender.decrease_score(uid, pid)
    return id


def edit_comment(id, text):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute('UPDATE comments SET text = %s WHERE id = %s', (text, id))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res


def delete_comment(id):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM comments where id = %s', (id,))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res
