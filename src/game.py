import numpy as np
from components.card import Card, CARDS

class Game:

    def __init__(self):
        print("cool!")

        # Define gamestate as 5 by 5 grid. Each piece is uniquely numbered and
        # id is stored at the matrix position. 0,0 is top left.
        self.gamestate = np.zeros((5,5))
        
        #place pieces
        for i in range(1,6):
            self.gamestate[i-1,0] = i
            self.gamestate[i-1,4] = i+5

        self.cardstate = [Card(card) for card in CARDS]
        self.selected = None
        self.currentplayer = 0

    def select(self, card):
        if (card == self.cardstate[0] or card == self.cardstate[1]) and self.currentplayer == 0:
            self.selected = card
        elif (card == self.cardstate[3] or card == self.cardstate[4]) and self.currentplayer == 1:
            self.selected = card