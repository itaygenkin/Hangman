import string
import time
from random import random
from colorama import Fore, Style


def choose_word(words_list):
    """
    randomly chooses a word from a bank of words
    :param words_list: list of words
    :type words_list: list
    :return: a random word
    :rtype: str
    """
    k = random()
    k = int(k * len(words_list))
    if words_list[k][-1] == '\n':
        words_list[k] = words_list[k][:-1]
    return words_list[k]


# return True iff the letter is a letter from the 'abc' (no matter if the letter is upper or lower)
def is_valid_letter(letter):
    """
    check if letter is one of the abc letters (no matter upper or lower)
    :param letter: char
    :return: True if letter is a legal letter, False otherwise
    :rtype: bool
    """
    letter.lower()
    abc = string.ascii_lowercase
    if len(letter) == 1 and letter in abc:
        return True
    return False


# update the letters the user guessed and return true iff the letter guessed is valid, and it is not guessed yet
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    if is_valid_letter(letter_guessed) and letter_guessed not in old_letters_guessed:
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


HANGMAN_ASCII_ART = """  _    _
 | |  | |
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \\
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |
                     |___/"""


def print_hangman(num_of_tries):
    print(Fore.RED + HANGMAN_PHOTOS[num_of_tries] + Style.RESET_ALL)
