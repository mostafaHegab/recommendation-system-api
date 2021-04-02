from .db import DB


def get_products(uid, skip, limit):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT products.id, products.name, products.image, (SELECT COUNT(id) FROM favorites WHERE pid = products.id and uid = %s) AS is_favorite, CAST((SELECT AVG(rate) FROM ratings WHERE pid = products.id) AS FLOAT) AS rating FROM products ORDER BY rating DESC LIMIT %s, %s',
        (uid, skip, limit)
    )
    res = c.fetchall()
    c.close()
    conn.close()
    return res

def product_info(id, uid):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT products.*, (SELECT COUNT(id) FROM favorites WHERE pid = products.id and uid = %s) AS is_favorite, (SELECT AVG(rate) FROM ratings WHERE pid = products.id) AS rating FROM products WHERE id = %s',
        (uid, id)
    )
    res = c.fetchall()[0]
    c.close()
    conn.close()
    return res


# def get_product_image(id):
#     conn = DB.get_connection()
#     c = conn.cursor(dictionary=True)
#     c.execute('SELECT products.image FROM products WHERE id = %s',
#         (id)
#     )
#     res = c.fetchall()[0]
#     c.close()
#     conn.close()
#     return res


# def set_product_image(pid, name):
#     conn = DB.get_connection()
#     id = DB.generate_random_id()
#     c = conn.cursor()
#     c.execute('UPDATE products SET image = %s WHERE id = %s, (name, pid))
#     res = c.rowcount
#     conn.commit()
#     c.close()
#     conn.close()
#     return res


def get_comments(pid, skip, limit):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT comments.id AS comment_id, comments.text, comments.time, users.id AS user_id, CONCAT(users.firstname, " ", users.lastname) AS username, users.image AS user_image, ratings.rate AS rate\
    FROM comments INNER JOIN users ON comments.pid = %s and users.id = comments.uid LEFT JOIN ratings ON ratings.pid = 1 and ratings.uid = comments.uid ORDER BY comments.time DESC LIMIT %s, %s',
        (pid, skip, limit)
    )
    res = c.fetchall()
    c.close()
    conn.close()
    return res


def get_favorits(uid):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT products.id, products.name, products.image, CAST((SELECT AVG(rate) FROM ratings WHERE pid = products.id) AS FLOAT) AS rating FROM favorites INNER JOIN products ON favorites.uid = %s AND products.id = favorites.pid',
        (uid,)
    )
    res = c.fetchall()
    c.close()
    conn.close()
    return res


def add_favorit(pid, uid):
    conn = DB.get_connection()
    id = DB.generate_random_id()
    c = conn.cursor()
    c.execute('INSERT INTO favorites (id, pid, uid) VALUES (%s, %s, %s)', (id, pid, uid))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res


def delete_favorit(pid, uid):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM favorites WHERE pid = %s and uid = %s', (pid, uid))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res
