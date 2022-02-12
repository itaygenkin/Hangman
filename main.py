import string
import sys
import time

HANGMAN_ASCII_ART = """  _    _
 | |  | |
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \\
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |
                     |___/"""
picture_0 = "  x-------x"
picture_1 = """    x-------x
    |
    |
    |
    |
    |"""
picture_2 = """"    x-------x
    |       |
    |       0
    |
    |
    |
"""
picture_3 = """    x-------x
    |       |
    |       0
    |       |
    |
    |
"""
picture_4 = """    x-------x
    |       |
    |       0
    |      /|\\
    |
    |
"""
picture_5 = """    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |"""
picture_6 = """    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |"""
hangman_pictures = [picture_0, picture_1, picture_2, picture_3, picture_4, picture_5, picture_6]
old_letters_guessed = []


# printing the begging screen of the game
def welcome():
    print(HANGMAN_ASCII_ART)
    time.sleep(1.3)
    print("Welcome to the game Hangman")
    time.sleep(1.8)
    print("You have 6 tries")
    time.sleep(1.7)
    enter = input("Please press enter to begin the game!")


def main():
    words_file = open(sys.argv[1], 'r')
    word_index = int(input("Please enter a number "))
    secret_word = choose_word(words_file, word_index)

    num_of_tries = 0
    MAX_TRIES = 6
    print_hangman(num_of_tries)

    while num_of_tries < MAX_TRIES:
        print(show_hidden_word(secret_word, old_letters_guessed))
        letter_guessed = input("Please guess a letter: ").lower()

        if try_update_letter_guessed(letter_guessed, old_letters_guessed):
            if letter_guessed not in secret_word:
                print("Wrong guess :(")
                time.sleep(0.5)
                num_of_tries += 1
                print_hangman(num_of_tries)
                time.sleep(0.6)
                print("Please try again")
            elif check_win(secret_word, old_letters_guessed):
                print(show_hidden_word(secret_word, old_letters_guessed))
                print("Congratulations!")
                break
        else:
            time.sleep(0.3)
            print("Invalid letter, please try again")
        if num_of_tries == MAX_TRIES:
            print("Loser!!")
        words_file.close()


# return a word from the words file according to the number the user chose
def choose_word(file_path, index):
    words = file_path.read()
    words_list = words.split(" ")
    n = (index - 1) % len(words_list)
    if n == len(words_list) - 1:
        words_list[n] = words_list[n][:-1]
    return words_list[n]


# return True iff the letter is a letter from the 'abc' (no matter if the letter is upper or lower)
def is_valid_letter(letter):
    letter.lower()
    abc = string.ascii_lowercase
    if len(letter) == 1 and letter in abc:
        return True
    return False


# return True iff the input of the player is valid
def check_valid_input(letter_guessed, old_letters_guessed):
    if not is_valid_letter(letter_guessed) or letter_guessed in old_letters_guessed:
        return False
    return True


# update the letters the user guessed and return true iff the letter guessed is valid and it is not guessed yet
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


# the names of the following keys were changed to just numbers so as to simplify the next function
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
    print(HANGMAN_PHOTOS[num_of_tries])


if __name__ == '__main__':
    welcome()
    main()
