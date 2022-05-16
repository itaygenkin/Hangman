class Player:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._num_of_games = 0
        self._num_of_wins = 0


class Game:
    def __init__(self, username, score, date):
        self._username = username
        self._score = score
        self._date = date
