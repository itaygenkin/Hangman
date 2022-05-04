import sqlite3


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

    def get_hall_of_fame(self):
        cur = self._connection.cursor()
        cur.execute("SELECT * FROM Hall_of_Fame ORDER BY score")
        try:
            output = (list(cur)[-10:]).reverse()
        except:
            print(type(cur))
            print(list(cur))
        else:
            return output

    def get_all_time(self):
        cur = self._connection.cursor()
        cur.execute("SELECT * FROM Hall_of_Fame ORDER BY score")
        return (cur.fetchall()).reverse()
