import os
import random
from Game import Game
from StringDatabase import StringDatabase

class Guess:
    def __init__(self, mode):
        self.mode = mode
        self.database = StringDatabase()
        self.games = []

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause(self):
        input("Press Enter to continue...")

    def play(self):
        while True:
            word = self.database.get_random_word()
            game = Game(word)
            while True:
                self.clear_screen()
                print("Welcome to the Word Guess Game")
                print(f"Word to guess: {''.join(game.current_guess)}")
                print(f"Letters guessed: {' '.join(game.letters_guessed)}")
                if self.mode == "test":
                    print(f"[DEBUG] Actual word: {word}")
                print("\nOptions:")
                print("g) Guess the word")
                print("l) Guess a letter")
                print("t) Tell me the word")
                print("q) Quit")
                choice = input("Choose an option: ").lower().strip()

                if choice == "g":
                    guess = input("Enter your word guess: ").strip().lower()
                    if game.guess_word(guess):
                        game.finalize(True)
                        print("🎉 Correct! Well done.")
                        self.pause()
                        break
                    else:
                        print("❌ Nope! Try again.")
                        self.pause()

                elif choice == "l":
                    letter = input("Enter a single letter: ").strip().lower()
                    if len(letter) != 1 or not letter.isalpha():
                        print("Please enter a valid letter.")
                        input("Press Enter to continue...")
                        continue
                    result = game.guess_letter(letter)
                    if result == -1:
                        print(f"'{letter}' is already already guessed.")
                    elif result == 0:
                        print(f"'{letter}' is not in the word.")
                    elif result:
                        print(f"'{letter}' found {result} time(s)!")
                    else:
                        print(f"You already guessed '{letter}'.")
                    input("Press Enter to continue...")
                    if game.is_complete():
                        # Finalize score before current_guess has no blanks
                        game.finalize(True)
                        print("🎉 You completed the word!")
                        print(f"Word: {''.join(game.current_guess)}")
                        self.pause()
                        self.clear_screen()
                        break



                elif choice == "t":
                    game.give_up()
                    game.finalize(False)
                    print(f"The word was: {word}")
                    self.pause()
                    break

                elif choice == "q":
                    self.games.append(game)
                    self.show_report()
                    return

                else:
                    print("Invalid choice.")
                    input("Press Enter to continue...")

            self.games.append(game)

    def show_report(self):
        self.clear_screen()
        print("Final Report".center(100, "-"))
        print(f"{'Game':<5}{'Word':<20}{'Status':<20}{'Bad Guesses':<15}{'Missed':<20}{'Score':<10}")
        total = 0
        for i, game in enumerate(self.games, start=1):
            if game.status.lower() == "in progress":
                continue
            print(f"{i:<5}{game.word:<20}{game.status:<20}{game.bad_word_guesses:<15}"
                f"{game.missed_letters:<20}{game.score:<10.2f}")
            total += game.score
        print("-" * 100)
        print(f"{'Final Score:':<81}{total:.2f}")

