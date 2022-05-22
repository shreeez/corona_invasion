import sys
from time import sleep
from random import random
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from virus import Virus
from raindrop import RainDrop
from random import randint
from tucha import Tucha


class FriendlyInvasion:
    """Класс для управдения ресурсами и поведением игры"""

    def __init__(self):
        """инициализирует игру и создаёт игровые ресурсы"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_heigth = self.screen.get_rect().height

        pygame.display.set_caption('Friendly Invasion')

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.viruses = pygame.sprite.Group()
        self.raindrops = pygame.sprite.Group()
        self.tuchi = pygame.sprite.Group()

        self._create_drops()
        self._create_virus()
        self._create_tucha()
        # self.fps = pygame.time.Clock()
        self.screen_sav = pygame.image.load('images/oboi.jpg').convert()

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            # self.fps.tick(144)
            self._check_events()

            if self.stats.game_active:
                self._create_virus()
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_virus()
                self._update_raindrops()
                self._update_tucha()
            self._update_screen()

    def _check_events(self):
        """Обрабатывыает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие коавиш"""
        if event.key == pygame.K_d:
            # Перемезает корабль вправо
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        # Закрытие окна по нажатию клавиши
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        # Реагирует на отпускание клавиш
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullets = Bullet(self)
            self.bullets.add(new_bullets)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        # Обновление позиций снарядов
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_virus_collisions()

    def _check_bullet_virus_collisions(self):
        """Check whether any bullets have hit an alien."""
        collision = pygame.sprite.groupcollide(
            self.bullets, self.viruses, True, True)

    def _create_virus(self):
        """Create an alien, if conditions are right."""
        if random() < self.settings.virus_frequency:
            virus = Virus(self)
            self.viruses.add(virus)

    def _update_virus(self):
        self.viruses.update()

        if pygame.sprite.spritecollideany(self.ship, self.viruses):
            self._ship_hit()
        self._check_virus_left()

    def _ship_hit(self):
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1

            self.viruses.empty()
            self.bullets.empty()

            self._create_virus()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_virus_left(self):
        """проверяет , не дорбрались ли верусята до левого края экрана"""
        screen_rect = self.screen.get_rect()
        for virus in self.viruses.sprites():
            if virus.rect.left <= screen_rect.left:
                self._ship_hit()
                break

    def _create_drops(self):
        """Fill the sky with raindrops."""
        # Create an drop and find the number of drops in a row.
        # Spacing between each drop is equal to one drop width.
        #   Note that the spacing here works reasonably for larger drops.
        #   If you're working with smaller drops, there might be a better
        #   approach to spacing.
        drop = RainDrop(self)
        drop_width, drop_height = drop.rect.size
        available_space_x = self.settings.screen_width - drop_width

        # We'll need this number again to make new rows.
        self.number_drops_x = available_space_x // (4 * drop_width) - 1

        # Determine the number of rows of drops that fit on the screen.
        available_space_y = self.settings.screen_heigth
        number_rows = available_space_y // (3 * drop_height)

        # Fill the sky with drops.
        for row_number in range(number_rows):
            self._create_row(row_number)

    def _create_row(self, row_number):
        """Create a single row of raindrops."""
        for drop_number in range(self.number_drops_x):
            self._create_drop(drop_number, row_number)

    def _create_drop(self, drop_number, row_number):
        """Create an drop and place it in the row."""
        drop = RainDrop(self)
        drop_width, drop_height = drop.rect.size
        drop.rect.x = drop_width + 5 * drop_width * drop_number
        drop.y = 3 * drop.rect.height * row_number
        drop.rect.y = drop.y
        drop.rect.x += randint(-5, 10)
        drop.rect.y += randint(-5, 10)
        self.raindrops.add(drop)

    def _update_raindrops(self):
        """Update drop positions, and look for drops
        that have disappeared.
        """
        self.raindrops.update()

        # Assume we won't make new drops.
        make_new_drops = False
        for drop in self.raindrops.copy():
            if drop.check_disappeared():
                # Remove this drop, and we'll need to make new drops.
                self.raindrops.remove(drop)
                make_new_drops = True

        # Make a new row of drops if needed.
        if make_new_drops:
            self._create_row(0)

    def _create_tucha(self):
        tucha = Tucha(self)
        tucha_width = tucha.rect.width
        avalible_space_x = self.settings.screen_width - (1 * tucha_width)
        number_tucha_x = avalible_space_x // (2 * tucha_width)
        print(number_tucha_x)

        for tucha_number in range(number_tucha_x):
            tucha = Tucha(self)
            tucha.x = tucha_width + 2 * tucha_width * tucha_number
            tucha.rect.x = tucha.x
            self.tuchi.add(tucha)

    def _check_tucha_edges(self):
        for tucha in self.tuchi.sprites():
            if tucha.check_edges():
                self.settings.fleet_direction *= -1
                break

    def _update_tucha(self):
        self._check_tucha_edges()
        self.tuchi.update()

    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран"""
        self.screen.blit(self.screen_sav, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Отображение последнего прорисованного экрана
        self.viruses.draw(self.screen)
        self.tuchi.draw(self.screen)
        self.raindrops.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    # создание экземляра и запуск игры
    ai = FriendlyInvasion()
    ai.run_game()
