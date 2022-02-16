class Players:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, player):
        cur = self._conn._connection.cursor()
        cur.execute("""
            INSERT INTO hall_of_fame (name, score, date) VALUES(?, ?, ?)
            """, [player._name, player._score, player._date])