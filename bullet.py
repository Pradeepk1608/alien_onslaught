import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    # A class to manage bullets fired from the ship
    def __init__(self, ai_settings, screen, ship):
        # Create the bullet object at the ship's current position
        super().__init__()  # to inherit properties from sprite
        self.screen = screen 

        # try to add image of the bullet
        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store the bullet position.
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
    
    def update(self):
        # to move the bullets up the screen by updating the decimal position of the bullet
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        # to draw the bullet on the screen 
        pygame.draw.rect(self.screen, self.color, self.rect)
    
