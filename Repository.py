import sqlite3
import numpy as np

import DTO


class Repository:
    def __init__(self, db_location):
        self._connection = sqlite3.connect(db_location)

    def create_table(self):
        cur = self._connection.cursor()
        # TODO: reimplement Hall_of_Fame table and use reference to the players
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Hall_of_Fame(
                username    STRING      NOT NULL,
                score       INTEGER     NOT NULL,
                date        STRING      NOT NULL
            )""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS All_Players(
                username    STRING      PRIMARY KEY,
                password    STRING      NOT NULL,
                games       INTEGER,
                wins        INTEGER
            )""")

    def close_db(self):
        self._connection.commit()
        self._connection.close()

    def win_game(self, player):
        cur = self._connection.cursor()
        cur.execute("""
            UPDATE All_Players 
            SET wins = wins + 1 
            WHERE username = ?
        """, (player.username,))
        cur.execute("""
            UPDATE All_Players 
            SET games = games + 1 
            WHERE username = ?
        """, (player.username,))

    def lose_game(self, player):
        cur = self._connection.cursor()
        cur.execute("""
            UPDATE All_Players 
            SET games = games + 1 
            WHERE username = ?
        """, (player.username,))

    def get_stats(self, player):
        """
        select the number of games and wins of the current player
        :param player: the player which is currently playing
        :return: array (np) of player's games and wins
        """
        cur = self._connection.cursor()
        cur.execute("""
            SELECT games, wins 
            FROM All_Players 
            WHERE username = ?
        """, (player.username,))
        x = cur.fetchall()
        stats = np.array(x)
        return stats if stats[0] > 0 else None  # TODO: debug

    def get_hall_of_fame(self):
        cur = self._connection.cursor()
        cur.execute("SELECT * FROM Hall_of_Fame ORDER BY score")
        output = cur.fetchall()
        n = min(10, len(output))
        output = output[-n:]
        return [str(output[x]) for x in range(n - 1, -1, -1)] if n > 0 else ["No games were played"]

    def get_all_time(self):
        cur = self._connection.cursor()
        cur.execute("SELECT * FROM Hall_of_Fame ORDER BY score")
        return cur.fetchall()

    def is_already_registered(self, name):
        cur = self._connection.cursor()
        cur.execute("""
            SELECT username FROM All_Players WHERE username = ?
        """, (name,))
        exists = cur.fetchall()
        if exists:
            return True
        return False

    def login(self, default=False):
        # TODO: test
        cur = self._connection.cursor()
        if default:
            cur.execute("""
                SELECT * FROM All_Players WHERE username = ?
            """, ("guest",))
            return DTO.Player(*cur.fetchall()[0])
        else:
            name = input("Username: ")
            password = input("Password: ")
            cur.execute("""
                SELECT * FROM All_Players WHERE (username, password) = (?, ?)
            """, (name, password))
            return DTO.Player(*cur.fetchall()[0])
