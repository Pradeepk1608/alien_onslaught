import pygame
class Settings():
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color=(230,230,230)
        self.background = pygame.image.load('images/bg.jpg')
        # Ship speed settings
        self.ship_speed_factor = 1.5 # this will decide the factor by which the ship will move

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3 # 3px
        self.bullet_height = 15  # 15px
        self.bullet_color = 250, 44, 2
        self.bullets_allowed = 3

        # Alien Settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 20
        # fleet_direction = 1; represents right and -1 represents left
        self.fleet_direction = 1
        self.ship_limit = 2

        # how quickly the game speeds up
        self.speedup_scale = 1.2
        # how quickly the alien pont value increases
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # initializeing the settings that change throught the game 
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1 # fleet direction "1" represents right and "-1" represents left

        # SCORING SYSTEM 
        self.alien_points =  50
    
    def increse_speed(self):
        #  increse speed settings and alien point values
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)