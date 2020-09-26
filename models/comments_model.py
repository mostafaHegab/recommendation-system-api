from .db import DB
db = DB.db


def add_comment(text, time, pid, uid):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute(
        'INSERT INTO comments (id, text, time, pid, uid) values (%s, %s, %s, %s, %s)',
        (id, text, time, pid, uid))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def edit_comment(id, text):
    c = db.cursor()
    c.execute('UPDATE comments SET text = %s WHERE id = %s', (text, id))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def delete_comment(id):
    c = db.cursor()
    c.execute('DELETE FROM comments where id = %s', (id,))
    res = c.rowcount
    db.commit()
    c.close()
    return res
