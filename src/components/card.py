import pygame

from src.game import Game

CARDS = {
    "Rabbit": [(-1, -1), (1, 1), (2, 0)],
    "Cobra": [(-1, 0), (1, 1), (1, -1)],
    "Rooster": [(-1, 0), (-1, -1), (1, 1), (1, 0)],
    "Tiger": [(0, 2), (0, -1)],
    "Monkey": [(-1, -1), (-1, 1), (1, -1), (1, 1)]
}


class Card:
    FONT = None

    def __init__(self, card):
        self.card = card
        self.card_moves = CARDS[card]

    def draw(self, surface: pygame.Surface, x, y, game: Game):

        # check if clicked

        from src.render import get_mouse_position

        bg_color = (255, 255, 255)
        if game.selected_card == self:
            bg_color = (160, 80, 80)
        elif x < get_mouse_position()[0] < x + 200 and y < get_mouse_position()[1] < y + 120:
            bg_color = (200, 160, 160)
            if pygame.mouse.get_pressed()[0]:
                game.select_card(self)
                bg_color = (160, 80, 80)
        pygame.draw.rect(surface, (0, 0, 0), (x, y, 220, 120))
        pygame.draw.rect(surface, bg_color, (x + 5, y + 5, 210, 110))

        text_surf = Card.FONT.render(self.card, True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = (x + 60, y + 60)
        surface.blit(text_surf, text_rect)

        pygame.draw.rect(surface, (0, 0, 0), (x + 115, y + 15, 90, 90))
        for i in range(5):
            for j in range(5):
                if (i, j) == (2, 2):
                    pygame.draw.rect(surface, (180, 70, 40), (x + 120 + i * 16, y + 20 + (4-j) * 16, 14, 14))
                elif (i - 2, j - 2) not in CARDS[self.card]:
                    pygame.draw.rect(surface, (255, 255, 255), (x + 120 + i * 16, y + 20 + (4-j) * 16, 14, 14))
                else:
                    pygame.draw.rect(surface, (40, 70, 180), (x + 120 + i * 16, y + 20 + (4-j) * 16, 14, 14))
