import json
import string
import time
import random
from colorama import Fore, Style


def parse_json_to_dict(file):
    """
    parse a json file, and convert it to dictionary
    :param file: json file to read
    :return: dictionary of object(str) - list of str
    :rtype: dictionary
    """
    data = json.loads(file.read())
    parsed_dict = {}
    for o in data:
        parsed_dict[o] = data[o]
    return parsed_dict


def choose_subject(words_dict):
    """
    get a dict and ask the user to choose a subject from the dict keys
    :param words_dict: dictionary which the keys are the subject that the user can choose
    :return: a key (subject) from the dict
    :rtype: str
    """
    subjects_list = list(words_dict.keys())
    print("Choose subject: ")
    for i in range(len(subjects_list)):
        print("\t", i+1, f"- {subjects_list[i]}")
    subject_chosen = input()
    try:
        subject_chosen = int(subject_chosen)
    except:
        print("Invalid choice")
        return choose_subject(words_dict)
    return subjects_list[subject_chosen-1]


def choose_word_by_subject(subject, words_dict):
    """
    chooses a word from a list of words by the key=subject
    :param subject: the subject from the user which the word should be relate to
    :param words_dict: dictionary of subjects and words
    :type subject: str
    :type words_dict: dict
    :return: a word from the values list of the key (subject)
    :rtype: str
    """
    words_list = words_dict[subject]
    return random.choice(words_list)


def choose_word(words_list):
    """
    randomly chooses a word from a bank of words
    :param words_list: list of words
    :type words_list: list
    :return: a random word
    :rtype: str
    """
    k = random.random()
    k = int(k * len(words_list))
    if words_list[k][-1] == '\n':
        words_list[k] = words_list[k][:-1]
    return words_list[k]


def is_valid_game_mode(mode, menu):
    """
    check if the mode the user chose is valid in the current menu
    :param mode:
    :param menu: the current menu
    :return: whether the mode is legal or not\
    :rtype: bool
    """
    mode_list = ['1', '2', '3', '4']
    if menu == 2:
        mode_list.append('5')
        mode_list.append('9')
    if mode in mode_list:
        return True
    return False


def is_valid_letter(letter):
    """
    check if letter is one of the abc letters (no matter upper or lower)
    :param letter: char
    :return: True if letter is a legal letter, False otherwise
    :rtype: bool
    """
    letter.lower()
    abc_list = string.ascii_lowercase
    if len(letter) == 1 and letter in abc_list:
        return True
    return False


# update the letters the user guessed and return true iff the letter guessed is valid, and it is not guessed yet
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    if is_valid_letter(letter_guessed) and letter_guessed not in old_letters_guessed:
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        print("X")
        # time.sleep(0.3)
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
