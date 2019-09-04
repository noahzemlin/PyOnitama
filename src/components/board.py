import pygame

class Board:
    def draw(self, surface):
        pygame.draw.rect(surface, (0,0,0), (10,250,500,500))
        for x in range(5):
            for y in range(5):
                pygame.draw.rect(surface, (255,255,255), (25 + x * 95, 265 + y * 95,90,90))