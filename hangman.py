import random
import os

stars = "*" * 60

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

def show_game_banner():
    name = " Hangman2022 Ucode Game "
    print('\x1b[1;31m' + stars)
    print(name.center(60, "*"))
    print(stars + '\x1b[0m')
    print()

def get_tries():
    while True:
        print("\n\x1b[1;33mRules:\nWrong letter: -1 point and -1 life\nCorrect letter: +1 point\nCorrect word/phrase: +3 points\n\x1b[0m")
        question = "\x1b[1;37mHow many lives do you want from 1 to 10?\x1b[0m "
        attention1 = "It's not a digit. Please try again..."
        attention2 = "You can only select from 1 to 10 lives!"
        input_data = input(question.center(60))
        if not input_data.isdigit():
            print(attention1.center(60))
        elif not 1 <= int(input_data) <= 10:
            print(attention2.center(60))
        else:
            break
    return input_data

def get_random_word():
    move_list = []
    with open("words.txt", "r") as f:
        index = 0
        for line in f:
            if line != "\n":
                move_list.append(line)
                index += 1
    random_word = move_list[random.randint(0, index)].rstrip()
    return random_word

def retry_game():
    question = "\x1b[1;36mLet's try again?\x1b[0m"
    bye = "Goodbye! Have a nice day ;)"
    answer = input(question.center(60))
    if answer == 'y' or answer == 'yes':
        clear_screen()
        run_game()
    else:
        clear_screen()
        show_game_banner()
        print('\x1b[1;36m' + bye.center(60) + '\x1b[0m')
        pass

def update_visible_string(current_string, answer_string, letter):
    updated_string = ""
    index = 0
    while index < len(answer_string):
        if answer_string[index] == letter:
            updated_string = updated_string + letter + " "
        else:
            updated_string = updated_string + current_string[index:index + 2]
        index += 2
    return updated_string

def sort_string(s):
    new_s = ""
    for char in sorted(s):
        new_s += char
    return new_s

def run_game():
    secret_word = get_random_word().upper()
    visible_string = ""
    answer_string = ""
    for letter in secret_word:
        if letter.isspace():
            visible_string = visible_string + "  "
            answer_string = answer_string + "  "
        elif letter.isalpha() or letter.isdigit():
            visible_string = visible_string + "_ "
            answer_string = answer_string + letter + " "
        else:
            visible_string = visible_string + letter + " "
            answer_string = answer_string + letter + " "
    won_game = False
    show_game_banner()
    tries = int(get_tries())
    points = 0
    wrong_guesses = 0
    letters_guessed = ""
    while tries - wrong_guesses > 0 and not(won_game):
        clear_screen()
        show_game_banner()
        print(visible_string.center(60))
        print('\x1b[1;32m' + "\nEntered Letters: " + letters_guessed  + '\x1b[0m')
        print('\x1b[1;32m' + f"Lives: [ {tries - wrong_guesses} ]\nPoints: [ {points} ]"  + '\x1b[0m')
        must_guess = True
        while must_guess:
            user_guess = input('\x1b[1;34m' + "\nEnter your letter or the whole word/phrase: "  + '\x1b[0m').upper()
            if secret_word == user_guess:
                won_game = True
                must_guess = False
                points +=3
            elif len(user_guess) == 1 and letters_guessed.find(user_guess) != -1:
                    print("\nYou have already guessed this letter.")
            elif len(user_guess) == 1:
                letters_guessed = sort_string(letters_guessed + user_guess)
                must_guess = False
            else:
                print("\nYou have entered too many letters or incorrect word/phrase!")
        if secret_word.find(user_guess) != -1:
            visible_string = update_visible_string(visible_string, answer_string, user_guess)
            points += 1
            if visible_string.find("_") == -1:
                won_game = True
        else:
            wrong_guesses += 1
            points -=1
    if won_game:
        clear_screen()
        show_game_banner()
        deadman_win = "\n+----+\n|\n|\n|"
        print('\x1b[1;36m' + deadman_win + '\x1b[0m')
        final1 = "Wow !!!"
        final2 = f"You guessed \"{secret_word}\"!"
        final3 = f"Lives remaining: [ {tries - wrong_guesses} ]"
        final4 = f"Total points: [ {points} ]"
        print('\n\n\x1b[0;33m' + stars  + '\x1b[0m')
        print('\x1b[1;35m' + final1.center(60) + "\n" + final2.center(60) + "\n" + '\x1b[1;32m' + final3.center(60) + "\n" + final4.center(60))
        print('\x1b[0;33m' + stars  + '\x1b[0m')
        retry_game()
    else:
        clear_screen()
        show_game_banner()
        deadman_end = "\n+---+\n|   o\n|  /|\\\n|  / \\"
        print('\x1b[1;36m' + deadman_end + '\x1b[0m')
        end1 = f"Game Over! The word/phrase was '{secret_word}'."
        end2 = f"Total points: [ {points} ]"
        print('\n\n\x1b[0;33m' + stars  + '\x1b[0m')
        print('\x1b[1;35m' + end1.center(60)  + '\x1b[0m')
        print('\x1b[1;32m' + end2.center(60)  + '\x1b[0m')
        print('\x1b[0;33m' + stars  + '\x1b[0m')
        retry_game()
run_game()
