
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
    print("Welcome to the game Hangman")
    print("You have 6 tries")  #
    enter = input("Please press enter to begin the game!")


def main():
    words_file = open("D:\Hangman words.txt", 'r')
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
                print("wrong guess :(\nplease try again")
                num_of_tries += 1
                print_hangman(num_of_tries)
            elif check_win(secret_word, old_letters_guessed):
                print(show_hidden_word(secret_word, old_letters_guessed))
                print("Congratulations!")
                break
            #else:
               # print(show_hidden_word(secret_word, old_letters_guessed))
        else:
            print("invalid letter, please try again")
        if num_of_tries == MAX_TRIES:
            print("Loser!!")
        words_file.close()


# return a word from the words file according to the number the user chose
def choose_word(file_path, index):
    words = file_path.read()
    words_list = words.split(" ")
    n = (index - 1) % len(words_list)
    print(len(words_list))
    return words_list[n]


# return True iff the letter is a letter from the 'abc' (no matter if the letter is upper or lower)
def is_valid_letter(letter):
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if len(letter) == 1 and letter in abc:
        return True
    else:
        return False


# return True iff the input of the player is valid
def check_valid_input(letter_guessed, old_letters_guessed):
    if not is_valid_letter(letter_guessed) or letter_guessed in old_letters_guessed:
        return False
    else:
        return True


# update the letters the user guessed and return true iff the letter guessed is valid and it is not guessed yet
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    if is_valid_letter(letter_guessed) and not letter_guessed in old_letters_guessed:
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        print("X")
        separator = ' --> '
        old_letters_guessed.sort()
        print(separator.join(old_letters_guessed))
        return False


# return the hidden word with the letters guessed only
def show_hidden_word(secret_word, old_letters_guessed):
    word_shown = ""
    for letter in secret_word:
        if letter in old_letters_guessed:
            word_shown = word_shown + letter + ' '
        else :
            word_shown = word_shown + "_ "
    return word_shown[:-1]


# return True iff the player has won
def check_win(secret_word, old_letters_guessed):
    for letter in secret_word :
        if letter not in old_letters_guessed:
            return False
    return True


# the names of the following keys were changed to just numbers so as to simplify the next function
HANGMAN_PHOTOS = {0 : "  x-------x",
1 : """    x-------x
    |
    |
    |
    |
    |""",
2 : """"    x-------x
    |       |
    |       0
    |
    |
    |
""",
3 : """    x-------x
    |       |
    |       0
    |       |
    |
    |
""",
4 : """    x-------x
    |       |
    |       0
    |      /|\\
    |
    |
""",
5 : """    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |""",
6 : """    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |"""}


def print_hangman(num_of_tries):
    print(HANGMAN_PHOTOS[num_of_tries])

welcome()
main()
