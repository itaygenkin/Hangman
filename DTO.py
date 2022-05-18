class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.num_of_games = 0
        self.num_of_wins = 0


class Game:
    def __init__(self, username, score, date):
        self.username = username
        self.score = score
        self.date = date
