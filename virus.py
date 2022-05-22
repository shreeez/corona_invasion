import pygame
from pygame.sprite import Sprite
from random import randint


class Virus(Sprite):
    """инициализирует вирус, и задаёт его начальную позицию"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # загрузка изображения пришельца и насначение атрибута rect
        self.image = pygame.image.load('images/virus.png')
        self.rect = self.image.get_rect()


        self.rect.left = self.screen.get_rect().right
        # The farthest down the screen we'll place the alien is the height
        #   of the screen, minus the height of the alien.
        virus_top_max = self.settings.screen_heigth - self.rect.height
        self.rect.top = randint(0, virus_top_max)

        # сохранение точно горизонтальной позиции пришельца
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien steadily to the left."""
        self.x -= self.settings.virus_speed
        self.rect.x = self.x

