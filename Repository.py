import sqlite3
import time


class Repository:
    def __init__(self, db_location):
        self._connection = sqlite3.connect(db_location)

    def create_table(self):
        cur = self._connection.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS hall_of_fame
            name    STRING      NOT NULL,
            score   INTEGER   NOT NULL,
            date    DATE      NOT NULL
        )""")

    def insert(self, name, score):
        cur = self._connection.cursor()
        cur.execute("""
            INSERT INTO hall_of_fame (name, score, date) VALUES(?, ?, ?)
            """, [name, score, time.localtime()])

    def close_db(self):
        self._connection.commit()
        self._connection.close()
