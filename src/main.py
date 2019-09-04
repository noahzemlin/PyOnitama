from game import Game
from render import Screen

def main():
    game = Game()
    screen = Screen(game)
    screen.run()

if __name__ == "__main__":
    main()