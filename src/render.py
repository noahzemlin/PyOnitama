import numpy as np
import pygame
import os
from pygame.locals import *
from game import Game
from components.board import Board
from components.card import Card

# constants
SCREENRECT = Rect(0, 0, 1000, 1000)

class Screen:

    def __init__(self, game: Game):
        self.game = game
        self.running = True

    def run(self):
        pygame.init()
        pygame.display.set_caption('PyOnitama')

        winstyle = 0
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

        pieces = [pygame.image.load(file).convert_alpha() for file in ['red_pawn.png', 'red_king.png', 'blue_pawn.png', 'blue_king.png']]

        board = Board()
        Card.init()
        card1 = Card("Tiger")
        card2 = Card("Dragon")
        card3 = Card("Frog")
        card4 = Card("Rabbit")
        card5 = Card("Crab")

        clock = pygame.time.Clock()

        while self.running:
            #check events
            for event in pygame.event.get():
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return

            #render
            screen.fill((255,255,255))
            board.draw(screen)

            #draw whose turn it is
            TextSurf = Card.font.render("Player " + str(self.game.currentplayer + 1) + "'s turn!", True, (0,0,0))
            TextRect = TextSurf.get_rect()
            if self.game.currentplayer == 0:
                TextRect.center = (220, 40)
            else:
                TextRect.center = (220, 960)
            screen.blit(TextSurf, TextRect)

            #draw cards
            self.game.cardstate[0].draw(screen, 20, 90, self.game)
            self.game.cardstate[1].draw(screen, 270, 90, self.game)
            self.game.cardstate[2].draw(screen, 550, 440, self.game)
            self.game.cardstate[3].draw(screen, 20, 790, self.game)
            self.game.cardstate[4].draw(screen, 270, 790, self.game)

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

            #wait for next frame
            clock.tick(30)

        pygame.time.wait(100)
        pygame.quit()