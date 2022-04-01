import sys
import tkinter as tk
from tkinter import ttk

import Repository
import DTO
from Words import *
from DAO import Players

connection = Repository.Repository(sys.argv[2])
Hall_of_Fame = Players(connection)


# printing the opening screen of the game
def welcome():
    # root = tk.Tk()
    # frame = ttk.Frame(root, padding=180)
    # frame.grid()
    # ttk.Label(frame, text=HANGMAN_ASCII_ART).grid(column=0, row=0)
    # root.mainloop()

    print(Fore.CYAN + HANGMAN_ASCII_ART + Style.RESET_ALL)
    time.sleep(1)
    print("Welcome to the game Hangman")
    time.sleep(1)
    enter = input("Please press enter to begin the game ")


def main():
    words_file = open(sys.argv[1], 'r')
    words = words_file.read()
    words_list = words.split(" ")
    words_file.close()
    print(words_list)
    # connection = Repository.Repository(sys.argv[2])
    connection.create_table()

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
    old_letters_guessed = []
    num_of_tries = 0
    print_hangman(0)
    while num_of_tries < 6:
        print(show_hidden_word(secret_word, old_letters_guessed))
        letter_guessed = input("Please guess a letter: ").lower()

        if try_update_letter_guessed(letter_guessed, old_letters_guessed):
            if letter_guessed not in secret_word:
                print("Wrong guess :(")
                time.sleep(0.5)
                num_of_tries += 1
                print_hangman(num_of_tries)
                time.sleep(0.5)
                print("Please try again")
            elif check_win(secret_word, old_letters_guessed):
                print(show_hidden_word(secret_word, old_letters_guessed))
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


if __name__ == '__main__':
    welcome()
    main()
