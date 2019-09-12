import pygame

CARDS = {
    "Tiger": [(-2, 0), (-1, 0)],
    "Dragon": [(-1, -2), (-1, 2), (1, -1), (1, 1)],
    "Frog": [(-1, -1), (0, -2), (1, 1)],
    "Rabbit": [(-1, 1), (0, 2), (1, -1)],
    "Crab": [(-1, 0), (0, -2), (0, 2)]
}

class Card:

    def init():
        Card.font = pygame.font.Font('freesansbold.ttf',24)

    def __init__(self, card):
        self.card = card

    def draw(self, surface, x, y, game):

        # check if clicked

        bgcolor = (255,255,255)
        if game.selectedCard == self:
            bgcolor = (160, 80, 80)
        elif x < pygame.mouse.get_pos()[0] < x + 200 and y < pygame.mouse.get_pos()[1] < y + 120:
            bgcolor = (200, 160, 160)
            if pygame.mouse.get_pressed()[0]:
                game.selectCard(self)
                bgcolor = (160, 80, 80)
        pygame.draw.rect(surface, (0,0,0), (x,y,220,120))
        pygame.draw.rect(surface, bgcolor, (x+5,y+5,210,110))

        TextSurf = Card.font.render(self.card, True, (0,0,0))
        TextRect = TextSurf.get_rect()
        TextRect.center = (x+60, y+60)
        surface.blit(TextSurf, TextRect)

        pygame.draw.rect(surface, (0,0,0), (x+115,y+15, 90, 90))
        for i in range(5):
            for j in range(5):
                if (i,j) == (2,2):
                    pygame.draw.rect(surface, (180,70,40), (x+120+j*16, y+20+i*16, 14, 14))
                elif (i-2,j-2) not in CARDS[self.card]:
                    pygame.draw.rect(surface, (255,255,255), (x+120+j*16, y+20+i*16, 14, 14))
                else:
                    pygame.draw.rect(surface, (40,70,180), (x+120+j*16, y+20+i*16, 14, 14))