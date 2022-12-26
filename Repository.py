import sqlite3
import numpy as np
import DTO


class Repository:
    def __init__(self, db_location):
        self.connection = sqlite3.connect(db_location)

    def create_table(self):
        cur = self.connection.cursor()
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
                wins        INTEGER,
                row         INTEGER
            )""")
        cur.close()

    def close_db(self):
        self.connection.commit()
        self.connection.close()

    def win_game(self, player):
        cur = self.connection.cursor()
        cur.execute("""
            UPDATE All_Players 
            SET wins = wins + 1, games = games + 1, row = row + 1 
            WHERE username = ?
        """, (player.username,))
        # cur.execute("""
        #     UPDATE All_Players
        #     SET games = games + 1
        #     WHERE username = ?
        # """, (player.username,))
        cur.close()

    def lose_game(self, player):
        cur = self.connection.cursor()
        cur.execute("""
            UPDATE All_Players 
            SET games = games + 1, row = row + 1 
            WHERE username = ?
        """, (player.username,))
        # cur.execute("""
        #     UPDATE All_Players
        #     SET row = row + 1
        #     WHERE username = ?
        # """, (player.username,))
        cur.close()

    def get_stats(self, player):
        """
        select the number of games and wins of the current player
        :param player: the player which is currently playing
        :return: array (np) of player's games and wins
        """
        cur = self.connection.cursor()
        cur.execute("""
            SELECT games, wins, row 
            FROM All_Players 
            WHERE username = ?
        """, (player.username,))
        x = cur.fetchall()
        cur.close()
        stats = np.array(*x, dtype=np.int32)
        return stats if stats[0] > 0 else None

    def get_hall_of_fame(self):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM Hall_of_Fame ORDER BY score")
        output = cur.fetchall()
        cur.close()
        n = min(10, len(output))
        output = output[-n:]
        return [str(output[x]) for x in range(n - 1, -1, -1)] if n > 0 else ["No games were played"]

    def get_all_time(self):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM Hall_of_Fame ORDER BY score")
        x = cur.fetchall()
        cur.close()
        return x

    def is_already_registered(self, name):
        cur = self.connection.cursor()
        cur.execute("""
            SELECT username FROM All_Players WHERE username = ?
        """, (name,))
        exists = cur.fetchall()
        cur.close()
        return True if exists else False

    def login(self, default=False):
        cur = self.connection.cursor()
        if default:
            cur.execute("""SELECT * FROM All_Players WHERE username = ?""", ("guest",))
            try:
                return DTO.Player(*cur.fetchall()[0])
            except IndexError:
                return None
        else:
            name = input("Username: ")
            password = input("Password: ")
            cur.execute("""SELECT * FROM All_Players WHERE (username, password) = (?, ?)""", (name, password))
            try:
                return DTO.Player(*cur.fetchall()[0])
            except IndexError:
                print("Invalid username or password")
                return None
