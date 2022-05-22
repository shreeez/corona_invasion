import pygame
from pygame.sprite import Sprite


class RainDrop(Sprite):
    """класс, представляющий одного пришельца"""

    def __init__(self, ai_game):
        """инициализирует пришельца, и задаёт его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # загрузка изображения пришельца и насначение атрибута rect
        self.image = pygame.image.load('images/rain.png')
        self.rect = self.image.get_rect()

        # каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # сохранение точно горизонтальной позиции пришельца

    def check_disappeared(self):
        """Check if drop has disappeared off bottom of screen."""
        if self.rect.top > self.screen.get_rect().bottom:
            return True
        else:
            return False

    def update(self):
        """Move the raindrop down the screen."""
        self.y += self.settings.raindrop_speed
        self.rect.y = self.y



    def check_edges(self):
        """Возвращает True, если приешелец нахродиться у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom:
            return True
