import pygame
from src.game import Game


def draw_board(surface: pygame.Surface, game: Game):
    pygame.draw.rect(surface, (0, 0, 0), (10, 250, 500, 500))
    hovered = (-1, -1)

    from src.render import get_mouse_position
    if 25 < get_mouse_position()[0] < 495 and 265 < get_mouse_position()[1] < 735:
        grid_x = (get_mouse_position()[0] - 10) / 100
        grid_y = (get_mouse_position()[1] - 250) / 100
        hovered = (int(grid_x), int(grid_y))
        if pygame.mouse.get_pressed()[0]:
            game.select_tile(int(grid_x), int(grid_y))

    for x in range(5):
        for y in range(5):
            if x == game.selected_board_x and y == game.selected_board_y:
                pygame.draw.rect(surface, (255, 80, 80), (25 + x * 95, 265 + y * 95, 90, 90))
            elif x == hovered[0] and y == hovered[1]:
                pygame.draw.rect(surface, (255, 180, 180), (25 + x * 95, 265 + y * 95, 90, 90))
            else:
                pygame.draw.rect(surface, (255, 255, 255), (25 + x * 95, 265 + y * 95, 90, 90))
