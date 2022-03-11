import string
import sys
import time
from random import random
from colorama import Fore, Style

import Repository
import DTO
from DAO import Players

HANGMAN_ASCII_ART = """  _    _
 | |  | |
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \\
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |
                     |___/"""

connection = Repository.Repository(sys.argv[2])
Hall_of_Fame = Players(connection)


# printing the opening screen of the game
def welcome():
    print(Fore.CYAN + HANGMAN_ASCII_ART + Style.RESET_ALL)
    time.sleep(1.5)
    print("Welcome to the game Hangman")
    time.sleep(1.7)
    enter = input("Please press enter to begin the game ")


def main():
    words_file = open(sys.argv[1], 'r')
    words = words_file.read()
    words_list = words.split(" ")
    # connection = Repository.Repository(sys.argv[2])
    connection.create_table()

    global old_letter_guessed
    game_mode = input("Choose 1 for the ultimate game or 2 for the score game ")

    while game_mode != '1' and game_mode != '2':
        print("Invalid level chosen")
        game_mode = input("Choose 1 for the ultimate game or 2 for the score game ")
    print("You have 6 tries")
    time.sleep(0.5)
    while game_mode == '1':
        secret_word = choose_word(words_list)
        game_mode = running_ultimate_game(secret_word)
    while game_mode == '2':
        secret_word = choose_word(words_list)
        game_mode = running_score_game(secret_word)

    connection.close_db()
    words_file.close()


def running_ultimate_game(secret_word):
    """
    run a game with no score
    :param secret_word: represent the word that the user should guess
    :type secret_word: str
    :return: game mode
    :rtype: str
    """
    old_letter_guessed = []
    num_of_tries = 0
    print_hangman(0)
    while num_of_tries < 6:
        print(show_hidden_word(secret_word, old_letter_guessed))
        letter_guessed = input("Please guess a letter: ").lower()

        if try_update_letter_guessed(letter_guessed, old_letter_guessed):
            if letter_guessed not in secret_word:
                print("Wrong guess :(")
                time.sleep(0.5)
                num_of_tries += 1
                print_hangman(num_of_tries)
                time.sleep(0.5)
                print("Please try again")
            elif check_win(secret_word, old_letter_guessed):
                print(show_hidden_word(secret_word, old_letter_guessed))
                print("Congratulations!")
                break
        else:
            time.sleep(0.5)
            print("Invalid letter, please try again")
        if num_of_tries == 6:
            print("Loser!!")
    return input("Choose 1 for new game or 0 to end the game ")


def running_score_game(secret_word):
    """
    run a game with score
    :param secret_word: represent the word that the user should guess
    :type secret_word: str
    :return: game mode
    :rtype: str
    """
    time.sleep(0.3)
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
                time.sleep(0.5)
                num_of_tries += 1
                print_hangman(num_of_tries)
                time.sleep(0.5)
                start += 1
                print("Please try again")
            elif check_win(secret_word, old_letter_guessed):
                timer = time.time() - start
                score = compute_score(timer, secret_word)
                print(show_hidden_word(secret_word, old_letter_guessed))
                print("Congratulations!")
                print("You've got {} points!".format(score))
                add_to_db(score)
                break
        else:
            time.sleep(0.3)
            print("Invalid letter, please try again")
        if num_of_tries == 6:
            print("Loser!!")
    return input("Choose 2 for new game or 0 to end the game ")


def add_to_db(score):
    name = input("Enter your name ")
    named_tuple = time.localtime()
    time_string = time.strftime("%m/%d/%Y", named_tuple)
    player = DTO.Player(name, score, time_string)
    Hall_of_Fame.insert(player)


def choose_word(words_list):
    """
    return a random word from a bank of words
    :param words_list: list of words
    :type words_list: list
    :return: a random word
    :rtype: str
    """
    k = random()
    k = int(k * (len(words_list) + 1))
    if k == len(words_list) - 1:
        words_list[k] = words_list[k][:-1]
    return words_list[k]


# return True iff the letter is a letter from the 'abc' (no matter if the letter is upper or lower)
def is_valid_letter(letter):
    letter.lower()
    abc = string.ascii_lowercase
    if len(letter) == 1 and letter in abc:
        return True
    return False


# return True iff the input of the player is valid
def check_valid_input(letter_guessed, old_letter_guessed):
    if not is_valid_letter(letter_guessed) or letter_guessed in old_letter_guessed:
        return False
    return True


# update the letters the user guessed and return true iff the letter guessed is valid, and it is not guessed yet
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    if is_valid_letter(letter_guessed) and not letter_guessed in old_letters_guessed:
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        print("X")
        time.sleep(0.3)
        separator = ' --> '
        old_letters_guessed.sort()
        print("Letters guessed: " + separator.join(old_letters_guessed))
        return False


# return the hidden word with the letters guessed only
def show_hidden_word(secret_word, old_letters_guessed):
    word_shown = ""
    for letter in secret_word:
        if letter in old_letters_guessed:
            word_shown = word_shown + letter + ' '
        elif letter == '_':
            word_shown = word_shown + '- '
        else:
            word_shown = word_shown + "_ "
    return word_shown[:-1]


# return True iff the player has won
def check_win(secret_word, old_letters_guessed):
    for letter in secret_word:
        if letter not in old_letters_guessed and letter != '_':
            return False
    return True


# the names of the following keys were changed to numbers so as to simplify the next function
HANGMAN_PHOTOS = {0: "  x-------x",
                  1: """    x-------x
    |
    |
    |
    |
    |""",
                  2: """"    x-------x
    |       |
    |       0
    |
    |
    |
""",
                  3: """    x-------x
    |       |
    |       0
    |       |
    |
    |
""",
                  4: """    x-------x
    |       |
    |       0
    |      /|\\
    |
    |
""",
                  5: """    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |""",
                  6: """    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |"""}


def print_hangman(num_of_tries):
    print(Fore.RED + HANGMAN_PHOTOS[num_of_tries] + Style.RESET_ALL)


def compute_score(timer, word):
    """
    calculate the score of the game
    :param timer: represent the elapsed time
    :param word: represent the word that should have been guessed
    :type timer: float
    :type word: str
    :return: score value
    :rtype: int
    """
    letter_freq_value = {'a': 1, 'b': 9, 'c': 5, 'd': 6, 'e': 1, 'f': 9, 'g':  8, 'h': 7, 'i': 2, 'j': 17, 'k': 13,
                         'l': 4, 'm': 6, 'n': 3, 'o': 3, 'p': 6, 'q': 18, 'r': 2, 's': 4, 't': 3, 'u': 6, 'v': 13,
                         'w': 12, 'x': 15, 'y': 10, 'z': 15}
    freq_value = 0
    for letter in word:
        if letter != '_':
            freq_value += letter_freq_value[letter]
    score = int((200 / timer) * freq_value)
    return score


if __name__ == '__main__':
    welcome()
    main()
