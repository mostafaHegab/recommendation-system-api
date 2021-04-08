from .db import DB

def add_comment(text, time, pid, uid):
    id = DB.generate_random_id()
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO comments (id, text, time, pid, uid) values (%s, %s, %s, %s, %s)',
        (id, text, time, pid, uid))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res


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
