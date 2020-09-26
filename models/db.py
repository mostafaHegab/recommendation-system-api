import datetime
from random import randint, shuffle

import mysql.connector
from utils.config import DB_CONFIG

class DB:
    db = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['name']
        )

    def __init__(self):
        print(DB.db)
        if DB.create_tables() != 0:
            DB.init_data()

    @staticmethod
    def create_tables():
        c = DB.db.cursor()
        for line in open('models/create_tables.sql'):
            if len(line) != 1:
                c.execute(line)
        result = c.rowcount
        c.close()
        return result

    @staticmethod
    def init_data():
        c = DB.db.cursor()
        for line in open('models/init_data.sql'):
            if len(line) != 1:
                c.execute(line)
        DB.db.commit()
        c.close()

    @staticmethod
    def generate_random_id():
        id = f'{int(datetime.datetime.now().timestamp())}{randint(0,9999)}'
        id = list(id)
        shuffle(id)
        id = ''.join(id)
        return int(id)
