import pygame

from src.interfaces.game_state import GameState
from src.interfaces.interface_state import InterfaceState
from src.interfaces.cards_enum import CARDS

def get_mouse_position():
    return int(pygame.mouse.get_pos()[0] / Card.SCREEN_SCALE), int(pygame.mouse.get_pos()[1] / Card.SCREEN_SCALE)


class Card:
    SCREEN_SCALE = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, index, surface: pygame.Surface, font, interface_state: InterfaceState, game_state: GameState):
        # check if clicked

        bg_color = (255, 255, 255)
        if interface_state.selected_card == index:
            bg_color = (160, 80, 80)
        elif self.x < get_mouse_position()[0] < self.x + 200 and self.y < get_mouse_position()[1] < self.y + 120:
            bg_color = (200, 160, 160)
            if pygame.mouse.get_pressed()[0]:
                interface_state.select_card(index)
                bg_color = (160, 80, 80)
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, 220, 120))
        pygame.draw.rect(surface, bg_color, (self.x + 5, self.y + 5, 210, 110))

        text_surf = font.render(game_state.cards[index], True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = (self.x + 60, self.y + 60)
        surface.blit(text_surf, text_rect)

        pygame.draw.rect(surface, (0, 0, 0), (self.x + 115, self.y + 15, 90, 90))
        for i in range(5):
            for j in range(5):
                if (i, j) == (2, 2):
                    pygame.draw.rect(surface, (180, 70, 40),
                                     (self.x + 120 + i * 16, self.y + 20 + (4 - j) * 16, 14, 14))
                elif (i - 2, j - 2) not in CARDS[game_state.cards[index]]:
                    pygame.draw.rect(surface, (255, 255, 255),
                                     (self.x + 120 + i * 16, self.y + 20 + (4 - j) * 16, 14, 14))
                else:
                    pygame.draw.rect(surface, (40, 70, 180),
                                     (self.x + 120 + i * 16, self.y + 20 + (4 - j) * 16, 14, 14))
