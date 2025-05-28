import sys
from Guess import Guess

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["play", "test"]:
        print("Usage: python3 words.py [play|test]")
        return
    game = Guess(sys.argv[1])
    game.play()

if __name__ == "__main__":
    main()
