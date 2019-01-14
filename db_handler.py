import mysql.connector

class DBHandler:
    def __init__(self):
        self.login = 'rpg_gamer'
        self.password = 'gamer_pass'
        self.config = {
            'host': 'localhost',
            'port': 3306,
            'database': 'RPG_DB',
            'user': self.login,
            'password': self.password
        }
        self.conn = mysql.connector.connect(**self.config)
        self.cur = self.conn.cursor()

    def repair_query(self, q):
        q = str(q).replace('"', '`')
        return q

    def select(self, query):
        try:
            self.cur.execute(self.repair_query(query), params=None, multi=False)
            data = self.cur.fetchall()
            return data
        except mysql.connector.Error as err:
            raise err

    def insert(self, query):
        try:
            self.cur.execute(self.repair_query(query))
            self.conn.commit()
        except mysql.connector.Error as err:
            raise err

    def update(self, query):
        try:
            self.cur.execute(self.repair_query(query))
            self.conn.commit()
        except mysql.connector.Error as err:
            raise err