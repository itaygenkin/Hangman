import sqlite3
import numpy as np


class Repository:
    def __init__(self, db_location):
        self._connection = sqlite3.connect(db_location)
        self._num_of_wins = 0
        self._num_of_failures = 0

    def create_table(self):
        cur = self._connection.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Hall_of_Fame(
            name    STRING      NOT NULL,
            score   INTEGER     NOT NULL,
            date    STRING      NOT NULL
        )""")

    def get_stats(self):
        stats = np.array([self._num_of_wins, self._num_of_failures])
        return stats if stats[0] + stats[1] > 1 else None

    def win_game(self):
        self._num_of_wins += 1

    def lose_game(self):
        self._num_of_failures += 1

    def close_db(self):
        self._connection.commit()
        self._connection.close()

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
