import pygame
from src.game import Game

class Board:
    def draw(self, surface: pygame.Surface, game: Game):
        pygame.draw.rect(surface, (0,0,0), (10,250,500,500))
        hovered = (-1, -1)
        
        if 25 < pygame.mouse.get_pos()[0] < 495 and 265 < pygame.mouse.get_pos()[1] < 735:
            gridX = (pygame.mouse.get_pos()[0] - 10) / 100
            gridY = (pygame.mouse.get_pos()[1] - 250) / 100
            hovered = (int(gridX), int(gridY))
            if pygame.mouse.get_pressed()[0]:
                game.selectTile(int(gridX), int(gridY))

        for x in range(5):
            for y in range(5):
                if x == game.selectedBoardX and y == game.selectedBoardY:
                    pygame.draw.rect(surface, (255,80,80), (25 + x * 95, 265 + y * 95,90,90))
                elif x == hovered[0] and y == hovered[1]:
                    pygame.draw.rect(surface, (255,180,180), (25 + x * 95, 265 + y * 95,90,90))
                else:
                    pygame.draw.rect(surface, (255,255,255), (25 + x * 95, 265 + y * 95,90,90))
