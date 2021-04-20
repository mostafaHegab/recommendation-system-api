from .db import DB


def create_user(firstname, lastname, email, password, verified, image):
    id = DB.generate_random_id()
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO users (id, firstname, lastname, email, password, verified, image) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (id, firstname, lastname, email, password, verified, image)
    )
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    neo_g = DB.get_neo4j_connection()
    neo_g.run(f'''
               CREATE (n:User {{id:$id}} ) WITH n MATCH (t: Tag) MERGE (n)-[:FOLLOWS{{score: 1}}]->(t)
            ''', {
        "id": id
    })
    return res


def find_user(email):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT id, firstname, lastname, email, password, image, verified FROM users WHERE email = %s', (email,))
    res = c.fetchall()
    c.close()
    conn.close()
    return res


def get_verification_code(email):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT id, verified FROM users WHERE email = %s', (email,))
    res = c.fetchall()
    c.close()
    conn.close()
    return res


def verify_account(id):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET verified = 0 WHERE id = %s', (id,))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res


def set_reset_code(id, code):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET reset_code = %s WHERE id = %s', (code, id))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res


def get_reset_code(email):
    conn = DB.get_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT id, reset_code FROM users WHERE email = %s', (email,))
    res = c.fetchall()
    c.close()
    conn.close()
    return res


def reset_password(id, password):
    conn = DB.get_connection()
    c = conn.cursor()
    c.execute(
        'UPDATE users SET password = %s, reset_code = 0 WHERE id = %s', (password, id))
    res = c.rowcount
    conn.commit()
    c.close()
    conn.close()
    return res
