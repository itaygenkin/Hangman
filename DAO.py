class Players:
    def __init__(self, conn):
        self._conn = conn

    def register(self, player):
        cur = self._conn._connection.cursor()
        cur.execute("""
            INSERT INTO All_Players (username, password, games, wins) VALUES(?, ?, ?)
            """, [player._username, player._password, player._num_of_games, player._num_of_wins])


class Games:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, game):
        cur = self._conn._connection.cursor()
        cur.execute("""
            INSERT INTO Hall_of_Fame (username, score, date) VALUES(?, ?, ?)
            """, [game._name, game._score, game._date])