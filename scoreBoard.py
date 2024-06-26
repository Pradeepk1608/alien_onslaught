import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    # Class to report scoring system
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for scoring information
        self.text_color = (250, 250, 252)
        self.font = pygame.font.SysFont(None, 45)

        # prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    def prep_score(self):
        # to turn the text displayed into an image
        rounded_score = int((round(self.stats.score, -1)))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # display the score at the topp right of the screen 
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def show_score(self):
        # Draw score to the screen 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # show ships
        self.ships.draw(self.screen)


    def prep_high_score(self):
        #  to turn the high score as displayed into an image
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # to center the high score at the top of the window
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top  = self.score_rect.top
    
    def prep_level(self):
        # turn the level number into image
        self.level_image = self.font.render(str(self.stats.level), True , self.text_color)

        # position the levvel image
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_ships(self):
        # to show how many ships are left
        self.ships = Group()  # group instance
        for ship_number in range(self.stats.ship_remain):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

