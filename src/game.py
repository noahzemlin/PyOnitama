import numpy as np
from src.components.card import Card, CARDS

class Game:

    def __init__(self):
        # Define gamestate as 5 by 5 grid. Each piece is uniquely numbered and
        # id is stored at the matrix position. 0,0 is top left.
        self.gamestate = np.zeros((5,5))
        
        #place pieces
        for i in range(1,6):
            self.gamestate[i-1,0] = i
            self.gamestate[i-1,4] = i+5

        self.cardstate = [Card(card) for card in CARDS]
        self.selectedCard = None
        self.selectedCardI = -1
        self.selectedBoardX = -1
        self.selectedBoardY = -1
        self.currentplayer = 0


        Game.instance = self

    def game():
        return Game.instance

    def selectCard(self, card):
        if (card == self.cardstate[0] or card == self.cardstate[1]) and self.currentplayer == 0:
            self.selectedCard = card
            for i in range(0, 5):
                if card == self.cardstate[i]:
                    self.selectedCardI = i
        elif (card == self.cardstate[3] or card == self.cardstate[4]) and self.currentplayer == 1:
            self.selectedCard = card
            for i in range(0, 5):
                if card == self.cardstate[i]:
                    self.selectedCardI = i
    
    def selectTile(self, x, y):

        if self.selectedCard != None and self.selectedBoardX != -1 and self.checkValidCardMove(self.selectedBoardX, self.selectedBoardY, x, y, self.selectedCard) and ((self.gamestate[x,y] == 0 or self.gamestate[x,y] > 5) and self.currentplayer == 0):
            self.gamestate[x,y] = self.gamestate[self.selectedBoardX, self.selectedBoardY]
            self.gamestate[self.selectedBoardX, self.selectedBoardY] = 0
            self.selectedBoardX = self.selectedBoardY = -1
            self.currentplayer = 1
            self.cardstate[self.selectedCardI] = self.cardstate[2]
            self.cardstate[2] = self.selectedCard
            self.selectedCard = None
            self.checkWin()
            return

        # succesful player 2 move
        if self.selectedCard != None and self.selectedBoardX != -1 and self.checkValidCardMove(self.selectedBoardX, self.selectedBoardY, x, y, self.selectedCard) and ((self.gamestate[x,y] == 0 or self.gamestate[x,y] <= 5) and self.currentplayer == 1):
            self.gamestate[x,y] = self.gamestate[self.selectedBoardX, self.selectedBoardY]
            self.gamestate[self.selectedBoardX, self.selectedBoardY] = 0
            self.selectedBoardX = self.selectedBoardY = -1
            self.currentplayer = 0
            self.cardstate[self.selectedCardI] = self.cardstate[2]
            self.cardstate[2] = self.selectedCard
            self.selectedCard = None
            self.checkWin()
            return

        if ((1 <= self.gamestate[x,y] <= 5 and self.currentplayer == 0) or (self.gamestate[x,y] > 5 and self.currentplayer == 1)):
            self.selectedBoardX = x
            self.selectedBoardY = y

    def checkValidCardMove(self, fromX, fromY, toX, toY, card):

        #print(f'attempting to move from ({fromX},{fromY}) to ({toX},{toY}) with {card.card}')

        positions = CARDS[card.card]
        # do upside down if player 1 lol
        if self.currentplayer == 0:
            for possible in positions:
                dx = -possible[1]
                dy = -possible[0]
                if toX - fromX == dx and toY - fromY == dy:
                    return True
        else:
            for possible in positions:
                dx = possible[1]
                dy = possible[0]
                if toX - fromX == dx and toY - fromY == dy:
                    return True

        return False


    def checkWin(self):
        # win by reaching enemy start
        if self.gamestate[2,0] == 8:
            self.currentplayer = 3
        if self.gamestate[2,4] == 3:
            self.currentplayer = 2

        player1Master = False
        player2Master = False

        for x in range(0,5):
            for y in range(0,5):
                if self.gamestate[x,y] == 3:
                    player1Master = True
                if self.gamestate[x,y] == 8:
                    player2Master = True
        
        if not player1Master:
            self.currentplayer = 3
        if not player2Master:
            self.currentplayer = 2
