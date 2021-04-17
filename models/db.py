import datetime
from random import randint, shuffle
import pandas as pd

import mysql.connector
from py2neo import Graph
from utils.config import DB_CONFIG, NEO4J_CONFIG


class DB:

    def __init__(self):
        if len(DB.get_tables()) == 0:
            DB.init_data()
            DB.init_neo4j_data()

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['name']
        )

    @staticmethod
    def get_neo4j_connection():
        return Graph(NEO4J_CONFIG['url'], password=NEO4J_CONFIG['password'])

    @staticmethod
    def get_tables():
        conn = DB.get_connection()
        c = conn.cursor()
        c.execute('SHOW TABLES')
        tables = c.fetchall()
        c.close()
        conn.close()
        return tables

    @staticmethod
    def create_tables():
        print('creating tables')
        conn = DB.get_connection()
        c = conn.cursor()
        for line in open('models/create_tables.sql'):
            if len(line) != 1:
                c.execute(line)
        c.close()
        conn.close()
        print('tables created')

    @staticmethod
    def init_data():
        DB.create_tables()
        conn = DB.get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO users (id, firstname, lastname, email, password, verified) VALUES (0, "graduation", "project", "g@p.com", "graduation project", 1)')
        data = pd.read_csv('models/movies_data.csv')
        data['genre'] = data['genre'].apply(eval)
        for i in range(data.shape[0]):
            row = data.iloc[i]
            print(f'adding {i}/{data.shape[0]} - {row["imdb_title_id"]}')
            row['genre'] = [genre.title() for genre in row['genre']]
            c.execute('INSERT INTO products (id, name, description, image, tags) VALUES (%s,%s,%s,%s,%s)',
                      (i, row['original_title'], row['description'], row['poster_url'], ', '.join(row['genre'])))
            c.execute('INSERT INTO ratings (id, rate, pid, uid) VALUES (%s, %s, %s,%s)',
                      (i, float(row['avg_vote']/2), i, 0))
        conn.commit()
        c.close()
        conn.close()

    @ staticmethod
    def init_neo4j_data():
        g = DB.get_neo4j_connection()
        g.run('MATCH (n) DETACH DELETE n')
        tags = ['music', 'crime', 'mystery', 'western', 'fantasy', 'thriller', 'animation', 'reality-tv', 'adventure', 'action', 'sport', 'drama',
                'adult', 'sci-fi', 'family', 'documentary', 'history', 'musical', 'romance', 'biography', 'film-noir', 'news', 'comedy', 'horror', 'war']
        for i in range(len(tags)):
            g.run(f"CREATE (n:Tag{{name: $name, id: $id}})", {
                "name": tags[i],
                "id": i
            })
        data = pd.read_csv('models/movies_data.csv')
        data['genre_ids'] = data['genre_ids'].apply(eval)
        for i in range(data.shape[0]):
            row = data.iloc[i]
            print(f'adding {i}/{data.shape[0]} - {row["imdb_title_id"]}')
            g.run(f'''
                CREATE (n:Product{{id: $id, name: $name, image: $image, pscore: $pscore, nscore: 0}})
                WITH n
                MATCH (t: Tag) WHERE t.id IN $tags
                MERGE (n)-[:HAS_TAG]->(t)
            ''', {
                "id": i,
                "name": row['original_title'],
                "image": row['poster_url'],
                "pscore": int(row['avg_vote']/2),
                "tags": row['genre_ids']
            })

    @ staticmethod
    def generate_random_id():
        id = f'{int(datetime.datetime.now().timestamp())}{randint(0,9999)}'
        id = list(id)
        shuffle(id)
        id = ''.join(id)
        return int(id)
