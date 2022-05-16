import sqlite3
import numpy as np


class Repository:
    def __init__(self, db_location):
        self._connection = sqlite3.connect(db_location)

    def create_table(self):
        cur = self._connection.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Hall_of_Fame(
            username    STRING      NOT NULL,
            score       INTEGER     NOT NULL,
            date        STRING      NOT NULL
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS All_Players(
            username    STRING      NOT NULL    PRIMARY KEY,
            password    STRING      NOT NULL    PRIMARY KEY,
            games       INTEGER,
            wins        INTEGER,
        """)

    def close_db(self):
        self._connection.commit()
        self._connection.close()

    def win_game(self, player):
        # TODO: implement
        pass

    def lose_game(self, player):
        # TODO: implement
        pass

    def get_stats(self, player):
        # TODO: correct (using 'SELECT...')
        wins = player._num_of_wins
        failures = player._num_of_games - wins
        stats = np.array([wins, failures])
        return stats if stats[0] + stats[1] > 1 else None

    def get_hall_of_fame(self):
        cur = self._connection.cursor()
        cur.execute("SELECT * FROM Hall_of_Fame ORDER BY score")
        output = cur.fetchall()
        n = min(10, len(output))
        output = output[-n:]
        return [str(output[x]) for x in range(n-1, -1, -1)] if n > 0 else ["No games were played"]

    def get_all_time(self):
        cur = self._connection.cursor()
        cur.execute("SELECT * FROM Hall_of_Fame ORDER BY score")
        return cur.fetchall()

    def is_already_registered(self, name):
        cur = self._connection.cursor()
        cur.execute("""
            SELECT username FROM All_Players WHERE username=?
            """, (name,))
        exists = cur.fetchall()
        if not exists:
            return True
        return False

    def login(self, default=False):
        # TODO: implement
        pass
