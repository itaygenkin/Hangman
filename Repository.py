import sqlite3
import time


class Repository:
    def __init__(self, db_location):
        self._connection = sqlite3.connect(db_location)

    def create_table(self):
        cur = self._connection.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Hall_of_Fame(
            name    STRING      NOT NULL,
            score   INTEGER     NOT NULL,
            date    STRING      NOT NULL
        )""")

    def close_db(self):
        self._connection.commit()
        self._connection.close()
