class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры"""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_heigth = 800
        self.bg_color = (230, 150, 200)

        # Настройки корабля
        self.ship_speed = 6.0
        self.ship_limit = 3

        # Параметры снаряда
        self.bullet_speed = 15
        self.bullet_width = 15
        self.bullet_height = 5
        self.bullet_color = (30, 250, 30)
        self.bullet_allowed = 10


        self.virus_frequency = 0.01
        self.virus_speed = 2.5

        self.raindrop_speed = 0.2

        self.tucha_speed = 1.0
        self.fleet_direction = 1