class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.num_of_games = 0
        self.num_of_wins = 0

    def __init__(self, username, password, games, wins):
        self.username = username
        self.password = password
        self.num_of_games = games
        self.num_of_wins = wins


class Game:
    def __init__(self, username, score, date):
        self.username = username
        self.score = score
        self.date = date
