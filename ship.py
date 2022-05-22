import pygame


class Ship():
    """Класс для управления кораблём"""

    def __init__(self, ai_game):
        """Инициализирует корабль и задаёт его начальную позицию"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/pngwing.png')
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midleft = self.screen_rect.midleft

        # Сохранение везественной кординаты центра корабля
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Обновляет позициб корабля с учётом флага"""
        # Обновляет атрибут х, а не rect
        # Перемезение корабля вправо и влево
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Перемезение корабля ввурх и вниз
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.settings.screen_heigth:
            self.y += self.settings.ship_speed

        # Обновление атрибута rect  на основании self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """обновляет размещение пушки после столкновения"""
        self.rect.midleft = self.screen_rect.midleft
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)