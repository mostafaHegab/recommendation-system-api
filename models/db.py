import datetime
from random import randint, shuffle

import mysql.connector
from utils.config import DB_CONFIG

class DB:

    def __init__(self):
        if len(DB.get_tables()) == 0:
            DB.create_tables()
            DB.init_data()
    
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
        conn = DB.get_connection()
        c = conn.cursor()
        for line in open('models/create_tables.sql'):
            if len(line) != 1:
                c.execute(line)
        c.close()
        conn.close()

    @staticmethod
    def init_data():
        conn = DB.get_connection()
        c = conn.cursor()
        for line in open('models/init_data.sql'):
            if len(line) != 1:
                c.execute(line)
        conn.commit()
        c.close()
        conn.close()

    @staticmethod
    def generate_random_id():
        id = f'{int(datetime.datetime.now().timestamp())}{randint(0,9999)}'
        id = list(id)
        shuffle(id)
        id = ''.join(id)
        return int(id)
