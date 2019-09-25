import numpy as np
import pygame
import os
from src.game import Game
from src.components.board import Board
from src.components.card import Card

# constants
SCREENRECT = pygame.Rect(0, 0, 1000, 1000)

class Screen:

    def __init__(self, game: Game):
        self.game = game
        self.running = True

        pygame.init()
        pygame.display.set_caption('PyOnitama')

        winstyle = 0
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)

        self.screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
        self.pieces = [pygame.image.load("assets/" + file).convert_alpha() for file in ['red_pawn.png', 'red_king.png', 'blue_pawn.png', 'blue_king.png']]
        self.board = Board()

        Card.init()
        Card("Tiger")
        Card("Dragon")
        Card("Frog")
        Card("Rabbit")
        Card("Crab")

    def update(self):
        screen = self.screen
        pieces = self.pieces
        board = self.board

        #render
        screen.fill((255,255,255))
        board.draw(screen, self.game)

        #draw whose turn it is
        if self.game.currentplayer <= 1:
            TextSurf = Card.font.render("Player " + str(self.game.currentplayer + 1) + "'s turn!", True, (0,0,0))
            TextRect = TextSurf.get_rect()
            if self.game.currentplayer == 0:
                TextRect.center = (220, 40)
            else:
                TextRect.center = (220, 960)
        else:
            if self.game.currentplayer == 2:
                TextSurf = Card.font.render("Player 1 Won!", True, (0,0,0))
            else:
                TextSurf = Card.font.render("Player 2 Won!", True, (0,0,0))
            TextRect = TextSurf.get_rect()
            TextRect.center = (220, 40)
        screen.blit(TextSurf, TextRect)

        #draw cards
        self.game.cardstate[0].draw(screen, 20, 90, self.game) #top left
        self.game.cardstate[1].draw(screen, 270, 90, self.game) #top right
        self.game.cardstate[2].draw(screen, 550, 440, self.game) #center
        self.game.cardstate[3].draw(screen, 20, 790, self.game) #bottom left
        self.game.cardstate[4].draw(screen, 270, 790, self.game) #bottom right

        #draw pieces
        for x in range(0,5):
            for y in range(0,5):
                if self.game.gamestate[x,y] != 0:
                    if self.game.gamestate[x,y] < 6:
                        if self.game.gamestate[x,y] == 3:
                            #red king
                            screen.blit(pieces[1], (25 + x * 95, 265 + y * 95,90,90))
                        else:
                            #red pawn
                            screen.blit(pieces[0], (25 + x * 95, 265 + y * 95,90,90))
                    else:
                        if self.game.gamestate[x,y] == 8:
                            #blue king
                            screen.blit(pieces[3], (25 + x * 95, 265 + y * 95,90,90))
                        else:
                            #blue pawn
                            screen.blit(pieces[2], (25 + x * 95, 265 + y * 95,90,90))


        #render
        pygame.display.flip()