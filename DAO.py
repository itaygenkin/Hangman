class Players:
    def __init__(self, conn):
        self._conn = conn

    def register(self, player):
        cur = self._conn._connection.cursor()
        cur.execute("""
            INSERT INTO All_Players (username, password, games, wins) VALUES(?, ?, ?, ?)
            """, [player.username, player.password, 0, 0])


class Games:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, game):
        cur = self._conn._connection.cursor()
        cur.execute("""
            INSERT INTO Hall_of_Fame (username, score, date) VALUES(?, ?, ?)
            """, [game.username, game.score, game.date])
