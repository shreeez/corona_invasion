import pygame
from pygame.sprite import Sprite


class Tucha(Sprite):
    """класс, представляющий одного пришельца"""

    def __init__(self, ai_game):
        """инициализирует пришельца, и задаёт его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # загрузка изображения пришельца и насначение атрибута rect
        self.image = pygame.image.load('images/tucha.png')
        self.rect = self.image.get_rect()

        # каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.top

        # сохранение точно горизонтальной позиции пришельца
        self.x = float(self.rect.x)


    def update(self):
        """перемещвет тучу вправо или влево"""
        self.x += (self.settings.tucha_speed *
                   self.settings.fleet_direction)

        self.rect.x = self.x


    def check_edges(self):
        """Возвращает True, если приешелец нахродиться у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True