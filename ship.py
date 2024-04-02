import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings, screen):
        # Initialize the ship and set its starting position
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Load the ship image and get its rect.
        self.load_image = pygame.image.load('images/ship.png')
        self.DEFAULT_IMAGE_SIZE = (110, 100)
        self.image = pygame.transform.scale(self.load_image, self.DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect()  # to create the rect of the ship which is a image
        self.screen_rect = screen.get_rect()
        
        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
    def center_ship(self):
        # to center the ship on the screen
        self.center = self.screen_rect.centerx
    def update(self):
        # Updating the ship's position based on the movement flag
        # update the ship's position, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor

        # update the rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
