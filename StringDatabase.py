class StringDatabase:
    def __init__(self, filename="words.txt"):
        self.words = []
        with open(filename, 'r') as f:
            for line in f:
                # Split by spaces and strip extra whitespace
                for word in line.strip().split():
                    if len(word) == 4:
                        self.words.append(word.lower())

    def get_random_word(self):
        import random
        return random.choice(self.words)
