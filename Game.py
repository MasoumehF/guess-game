LETTER_FREQUENCIES = {
    'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70,
    'f': 2.23, 'g': 2.02, 'h': 6.09, 'i': 6.97, 'j': 0.15,
    'k': 0.77, 'l': 4.03, 'm': 2.41, 'n': 6.75, 'o': 7.51,
    'p': 1.93, 'q': 0.10, 'r': 5.99, 's': 6.33, 't': 9.06,
    'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15, 'y': 1.97,
    'z': 0.07
}

class Game:
    def __init__(self, word):
        self.word = word
        self.current_guess = ["-"] * 4
        self.letters_guessed = []
        self.bad_word_guesses = 0
        self.status = "IN PROGRESS"
        self.missed_letters = 0
        self.bad_letter_guesses = []
        self.score = 0.0
        self.letter_guess_count = 0

    def guess_letter(self, letter):
        if letter in self.letters_guessed:
            return -1
        self.letters_guessed.append(letter)
        self.letter_guess_count += 1

        count = self.word.count(letter)
        if count > 0:
            for i, c in enumerate(self.word):
                if c == letter:
                    self.current_guess[i] = letter
        else:
            self.missed_letters += 1
            self.bad_letter_guesses.append(letter)

        return count



    def guess_word(self, guess):
        if guess == self.word:
            self.current_guess = list(self.word)
            return True
        else:
            self.bad_word_guesses += 1
            return False

    def give_up(self):
        self.status = "GAVE UP"

    def is_complete(self):
        return "-" not in self.current_guess

    def finalize(self, won):
        self.status = "Success" if won else "Give Up"

        score = 0.0

        if won:
            # If word was completed via individual letter guesses,
            # all letters are filled, so we must compute score based on when the word *became complete*
            hidden_letters = [c for i, c in enumerate(self.word) if self.current_guess[i] == '-']
            
            # Calculate score for the last correct guess that completed the word
            if hidden_letters:
                total_freq = sum(LETTER_FREQUENCIES.get(c, 0) for c in hidden_letters)
            else:
                # All letters are revealed; score is based on full word frequency
                total_freq = sum(LETTER_FREQUENCIES.get(c, 0) for c in self.word)

            if self.letter_guess_count > 0:
                score = total_freq / self.letter_guess_count
            else:
                score = total_freq  # Direct word guess

            score *= (1 - 0.1 * self.bad_word_guesses)

        else:
            # User gave up; deduct all unguessed letters
            hidden_letters = [c for i, c in enumerate(self.word) if self.current_guess[i] == '-']
            score = -sum(LETTER_FREQUENCIES.get(c, 0) for c in hidden_letters)

        self.score = round(score, 2)


