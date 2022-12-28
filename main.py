import os
import sys
from matplotlib import pyplot as plt

import Repository
import DTO
from DAO import Players, Games
from wordlib import *

global player


# printing the opening screen of the game
def welcome():
    print(Fore.CYAN + HANGMAN_ASCII_ART + Style.RESET_ALL)
    print("Welcome to the game Hangman")
    input("Please press enter to begin the game ")


def enter_page():
    global player
    game_option = menu_1()
    match game_option:
        # register
        case '1':
            player = register()
            if player is None:
                enter_page()
        # login
        case '2':
            player = connection.login()
            if player is None:
                enter_page()
        # guest login
        case '3':
            player = connection.login(default=True)
            if player is None:
                player = DTO.Player('guest', 'guest')
                All_Players.register(player)
        # exit
        case '4':
            return None
    return player


def main():
    global player
    # reading txt file
    # words_file = open(sys.argv[1], 'r')
    # words = words_file.read()
    # words_list = words.split(" ")
    # words_file.close()

    # reading json file
    file = open(sys.argv[3], 'r')
    words_dict = parse_json_to_dict(file)
    file.close()

    # game run
    game_option = menu_2()
    while True:
        match game_option:
            # run an ultimate game
            case '1':
                subject = choose_subject(words_dict)
                secret_word = choose_word_by_subject(subject, words_dict)
                running_ultimate_game(secret_word)

            # run a score game
            case '2':
                # secret_word = choose_word(words_list)
                subject = choose_subject(words_dict)
                secret_word = choose_word_by_subject(subject, words_dict)
                running_score_game(secret_word)

            # show hall of fame
            case '3':
                top_ten_list = connection.get_hall_of_fame()
                print('\n'.join(top_ten_list), '\n')
                input("Press 'b' to back to menu ")

            # show all time players
            case '4':
                all_time_list = connection.get_all_time()
                print('\n'.join(map(str, all_time_list)), '\n')
                input("Press 'b' to back to menu ")

            # show stats
            case '5':
                y = connection.get_stats(player)
                if y is None:
                    print("No games were played\n")
                else:
                    # wins = (y[1] / y[0]) * 100
                    # failures = (((y[0] - y[1]) / y[0]) * 100).round(2)
                    # my_lables = [f"Wins {wins}%", f"Failures {failures}%"]
                    # plt.pie(y, labels=my_lables, shadow=True)
                    plt.figure(figsize=(5, 4))
                    plt.bar(['Games', 'Wins', 'Failures', 'Wins in a row'], [y[0], y[1], y[0] - y[1], y[2]], width=0.25)
                    plt.title(f'{player.username}\'s Stats')
                    plt.show()

            # exit
            case '9':
                break
        game_option = menu_2()

    connection.close_db()


def menu_1():
    """
    show the initial menu option for the user
    :return: a menu option
    :rtype: char
    """
    mode = input("""    1 - Register
    2 - Login
    3 - Play as a guest
    4 - exit\n""")
    while not is_valid_game_mode(mode, 1):
        print("Invalid choice")
        mode = menu_1()
    return mode


def menu_2():
    """
    show the menu of game options for the user
    :return: a game option from the menu
    :rtype: char
    """
    mode = input("""    1 - Play a ultimate game
    2 - Play a score game
    3 - Hall of Fame
    4 - All time players table
    5 - Statistics
    9 - exit\n""")
    while not is_valid_game_mode(mode, 2):
        print("Invalid choice")
        mode = menu_2()
    return mode


def register():
    """
    register a new user and sign in
    :return: a new player
    """
    username = input("Choose an username: ")
    while connection.is_already_registered(username):
        print("Username " + Fore.MAGENTA + username + Style.RESET_ALL + " is already exists")
        username = input("Choose different username or type \'\exit\' to return the main page: ")
        if username == '\exit':
            return None
    password = input("Choose a password: ")
    new_player = DTO.Player(username, password)
    All_Players.register(new_player)
    return new_player


def running_ultimate_game(secret_word):
    """
    run a game with no score
    :param secret_word: represent the word that the user should guess
    :type secret_word: str
    :return: game mode
    :rtype: str
    """
    print("You have 6 tries")
    old_letters_guessed = []
    num_of_tries = 0
    print_hangman(0)

    while num_of_tries < 6:
        print(show_hidden_word(secret_word, old_letters_guessed))
        letter_guessed = input("Please guess a letter: ").lower()

        if try_update_letter_guessed(letter_guessed, old_letters_guessed):
            if letter_guessed not in secret_word:
                print("Wrong guess :(")
                num_of_tries += 1
                print_hangman(num_of_tries)
                print("Please try again")
            elif check_win(secret_word, old_letters_guessed):
                print(show_hidden_word(secret_word, old_letters_guessed))
                print("Congratulations!")
                break
        else:
            print("Invalid letter, please try again")
        if num_of_tries == 6:
            print("Loser!!")


def running_score_game(secret_word):
    """
    run a game with score
    :param secret_word: represent the word that the user should guess
    :type secret_word: str
    :return: game mode
    :rtype: str
    """
    global player
    print("You have 6 tries")
    old_letter_guessed = []
    num_of_tries = 0
    print_hangman(0)
    start = time.time()

    while num_of_tries < 6:
        print(show_hidden_word(secret_word, old_letter_guessed))
        letter_guessed = input("Please guess a letter: ").lower()  # the user must choose a letter

        if try_update_letter_guessed(letter_guessed, old_letter_guessed):
            if letter_guessed not in secret_word:
                print("Wrong guess :(")
                num_of_tries += 1
                print_hangman(num_of_tries)
                print("Please try again")
            elif check_win(secret_word, old_letter_guessed):
                timer = time.time() - start
                score = compute_score(timer, secret_word)
                print(show_hidden_word(secret_word, old_letter_guessed))
                print("Congratulations!")
                print(f"You've got {score} points!")
                add_to_db(score)
                connection.win_game(player)
                break
        else:
            print("Invalid letter, please try again")
        if num_of_tries == 6:
            print("Loser!!")
            connection.lose_game(player)


def add_to_db(score):
    global player
    named_tuple = time.localtime()
    time_string = time.strftime("%d/%m/%Y", named_tuple)
    game = DTO.Game(player.username, score, time_string)
    Hall_of_Fame.insert(game)


if __name__ == '__main__':
    # if os.path.exists('Hall_of_Fame.db'):
    #     os.remove('Hall_of_Fame.db')
    connection = Repository.Repository(sys.argv[2])
    connection.create_table()

    Hall_of_Fame = Games(connection)
    All_Players = Players(connection)

    welcome()
    if enter_page() is None:
        exit()
    main()
