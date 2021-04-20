from .db import DB
from utils.recommender import Recommender


def search_by_name(name, skip, limit):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('select products.id, products.name, products.image, products.tags, CAST((SELECT AVG(rate) FROM ratings WHERE pid = products.id) AS FLOAT) AS rating from products where LOCATE(%s, name) > 0 LIMIT %s, %s',
              (name, skip, limit))
    res = c.fetchall()
    c.close()
    conn.close()
    return res


def search_by_tag(tag_name, skip, limit):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('select products.id, products.name, products.image, products.tags, CAST((SELECT AVG(rate) FROM ratings WHERE pid = products.id) AS FLOAT) AS rating from products where LOCATE(%s, tags) > 0 LIMIT %s, %s',
              (tag_name, skip, limit))
    res = c.fetchall()
    c.close()
    conn.close()
    return res


def get_recommendations(uid, skip, limit):
    return Recommender.hybrid(uid, skip, limit)

def get_similar_product(pid, skip, limit):
    return Recommender.get_similar_product(pid, skip, limit)

def get_products(uid, skip, limit):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT products.id, products.name, products.image, (SELECT COUNT(id) FROM favorites WHERE pid = products.id and uid = %s) AS is_favorite, CAST((SELECT AVG(rate) FROM ratings WHERE pid = products.id) AS FLOAT) AS rating FROM products ORDER BY rating DESC LIMIT %s, %s',
              (uid, skip, limit))
    res = c.fetchall()
    c.close()
    conn.close()
    return res


def product_info(uid, pid):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT products.*, (SELECT COUNT(id) FROM favorites WHERE pid = products.id and uid = %s) AS is_favorite, (SELECT AVG(rate) FROM ratings WHERE pid = products.id) AS rating FROM products WHERE id = %s',
              (uid, pid))
    res = c.fetchall()[0]
    c.close()
    conn.close()
    Recommender.create_relation(uid, pid)
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
    FROM comments INNER JOIN users ON comments.pid = %s and users.id = comments.uid LEFT JOIN ratings ON ratings.pid = comments.pid and ratings.uid = comments.uid ORDER BY comments.time DESC LIMIT %s, %s',
              (pid, skip, limit))
    res = c.fetchall()
    c.close()
    conn.close()
    return res


def get_favorits(uid, skip, limit):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT products.id, products.name, products.image, CAST((SELECT AVG(rate) FROM ratings WHERE pid = products.id) AS FLOAT) AS rating FROM favorites INNER JOIN products ON favorites.uid = %s AND products.id = favorites.pid LIMIT %s, %s',
              (uid, skip, limit))
    res = c.fetchall()
    c.close()
    conn.close()
    return res


def add_favorit(uid, pid):
    conn = DB.get_connection()
    id = DB.generate_random_id()
    c = conn.cursor()
    c.execute(
        'INSERT INTO favorites (id, uid, pid) VALUES (%s, %s, %s)', (id, uid, pid))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    Recommender.increase_score(uid, pid)
    return res


def delete_favorit(uid, pid):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM favorites WHERE uid = %s and pid = %s', (uid, pid))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    Recommender.decrease_score(uid, pid)
    return res
