from .db import DB
db = DB().db


def get_places():
    c = db.cursor(dictionary=True)
    c.execute(f'SELECT * FROM places')
    res = c.fetchall()
    c.close()
    return res


def add_place(name, country, city, lat, lng):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute(f'INSERT INTO places (id, name, country, city, lat, lng) VALUES ({id}, "{name}", "{country}", "{city}", {lat}, {lng})')
    res = c.lastrowid
    db.commit()
    c.close()
    return res


def place_info(id):
    c = db.cursor(dictionary=True)
    c.execute(f'SELECT places.*, AVG(ratings.rate) AS rating FROM places, ratings WHERE places.id = {id} and ratings.pid = {id}')
    res = c.fetchall()[0]
    c.close()
    return res


def get_place_images(id):
    c = db.cursor(dictionary=True)
    c.execute(f'SELECT name FROM images WHERE pid = {id}')
    res = c.fetchall()
    c.close()
    return res


def add_place_image(pid, name):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute(f'INSERT INTO images (id, pid, name) VALUES ({id}, {pid}, "{name}")')
    res = c.rowcount
    db.commit()
    c.close()
    return res


def get_place_comments(pid, skip, limit):
    c = db.cursor(dictionary=True)
    c.execute(f'SELECT comments.id AS comment_id, comments.text, comments.time, users.id AS user_id, CONCAT(users.firstname, " ", users.lastname) AS username, users.image AS user_image\
    FROM comments INNER JOIN users ON comments.pid = {pid} and users.id = comments.uid ORDER BY comments.time DESC LIMIT {skip}, {limit}')
    res = c.fetchall()
    c.close()
    return res


def visited_places(uid):
    c = db.cursor(dictionary=True)
    c.execute(f'SELECT places.id, places.name, images.name AS image FROM visits INNER JOIN places ON visits.uid = {uid} AND places.id = visits.pid,\
    images WHERE images.pid = places.id GROUP BY places.id')
    res = c.fetchall()
    c.close()
    return res


def add_visit(pid, uid):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute(f'INSERT INTO visits (id, pid, uid) VALUES ({id}, {pid}, {uid})')
    res = c.rowcount
    db.commit()
    c.close()
    return res


def delete_visit(pid, uid):
    c = db.cursor()
    c.execute(f'DELETE FROM visits WHERE pid = {pid} and uid = {uid}')
    res = c.rowcount
    db.commit()
    c.close()
    return res


def favorits_places(uid):
    c = db.cursor(dictionary=True)
    c.execute(f'SELECT places.id, places.name, images.name AS image FROM favorites INNER JOIN places ON favorites.uid = {uid} AND places.id = favorites.pid,\
    images WHERE images.pid = places.id GROUP BY places.id')
    res = c.fetchall()
    c.close()
    return res


def add_favorit(pid, uid):
    id = DB.generate_random_id()
    c = db.cursor()
    c.execute(f'INSERT INTO favorites (id, pid, uid) VALUES ({id}, {pid}, {uid})')
    res = c.rowcount
    db.commit()
    c.close()
    return res


def delete_favorit(pid, uid):
    c = db.cursor()
    c.execute(f'DELETE FROM favorites WHERE pid = {pid} and uid = {uid}')
    res = c.rowcount
    db.commit()
    c.close()
    return res
