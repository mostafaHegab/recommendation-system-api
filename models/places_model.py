from .db import DB
db = DB.db


def get_places(uid, skip, limit):
    c = db.cursor(dictionary=True)
    c.execute('SELECT places.id, places.name, images.name AS image, (SELECT COUNT(id) FROM favorites WHERE pid = places.id and uid = %s) AS is_favorite, CAST((SELECT AVG(rate) FROM ratings WHERE pid = places.id) AS FLOAT) AS rating FROM places, images WHERE images.pid = places.id GROUP BY places.id ORDER BY rating DESC LIMIT %s, %s',
        (uid, skip, limit)
    )
    res = c.fetchall()
    c.close()
    return res


def add_place(name, country, city, lat, lng):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute('INSERT INTO places (id, name, country, city, lat, lng) VALUES (%s, %s, %s, %s, %s, %s)',
        (id, name, country, city, lat, lng)
    )
    db.commit()
    c.close()
    return id


def place_info(id, uid):
    c = db.cursor(dictionary=True)
    c.execute('SELECT places.*, (SELECT COUNT(id) FROM favorites WHERE pid = places.id and uid = %s) AS is_favorite, (SELECT AVG(rate) FROM ratings WHERE pid = places.id) AS rating FROM places WHERE id = %s',
        (uid, id)
    )
    res = c.fetchall()[0]
    c.close()
    return res


def get_place_images(id):
    c = db.cursor(dictionary=True)
    c.execute('SELECT name FROM images WHERE pid = %s', (id,))
    res = c.fetchall()
    c.close()
    return res


def add_place_image(pid, name):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute('INSERT INTO images (id, pid, name) VALUES (%s, %s, %s)', (id, pid, name))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def get_place_comments(pid, skip, limit):
    c = db.cursor(dictionary=True)
    c.execute('SELECT comments.id AS comment_id, comments.text, comments.time, users.id AS user_id, CONCAT(users.firstname, " ", users.lastname) AS username, users.image AS user_image, ratings.rate AS rate\
    FROM comments INNER JOIN users ON comments.pid = %s and users.id = comments.uid LEFT JOIN ratings ON ratings.pid = 1 and ratings.uid = comments.uid ORDER BY comments.time DESC LIMIT %s, %s',
        (pid, skip, limit)
    )
    res = c.fetchall()
    c.close()
    return res


def visited_places(uid):
    c = db.cursor(dictionary=True)
    c.execute('SELECT places.id, places.name, images.name AS image, (SELECT COUNT(id) FROM favorites WHERE pid = places.id and uid = %s) AS is_favorite FROM visits INNER JOIN places ON visits.uid = %s AND places.id = visits.pid, images WHERE images.pid = places.id GROUP BY places.id',
        (uid,uid)
    )
    res = c.fetchall()
    c.close()
    return res


def add_visit(pid, uid):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute('INSERT INTO visits (id, pid, uid) VALUES (%s, %s, %s)', (id, pid, uid))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def delete_visit(pid, uid):
    c = db.cursor()
    c.execute('DELETE FROM visits WHERE pid = %s and uid = %s', (pid, uid))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def favorits_places(uid):
    c = db.cursor(dictionary=True)
    c.execute('SELECT places.id, places.name, images.name AS image FROM favorites INNER JOIN places ON favorites.uid = %s AND places.id = favorites.pid,\
    images WHERE images.pid = places.id GROUP BY places.id',
        (uid,)
    )
    res = c.fetchall()
    c.close()
    return res


def add_favorit(pid, uid):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute('INSERT INTO favorites (id, pid, uid) VALUES (%s, %s, %s)', (id, pid, uid))
    res = c.rowcount
    db.commit()
    c.close()
    return res


def delete_favorit(pid, uid):
    c = db.cursor()
    c.execute('DELETE FROM favorites WHERE pid = %s and uid = %s', (pid, uid))
    res = c.rowcount
    db.commit()
    c.close()
    return res
