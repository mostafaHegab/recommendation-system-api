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

    @staticmethod
    def create_tables():
        c = DB.db.cursor()
        for line in open('models/create_tables.sql'):
            if len(line) != 1:
                c.execute(line)
        c.close()

    @staticmethod
    def init_data():
        c = DB.db.cursor()
        for line in open('models/init_data.sql'):
            if len(line) != 1:
                c.execute(line)
        DB.db.commit()
        c.close()
