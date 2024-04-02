import pygame 
from pygame.sprite import Group
# Import classes
from ship import Ship
from settings import Settings
import game_functions as gf
from alien import Alien
from game_data import GameData
from button import Button
from scoreBoard import Scoreboard

def run_game():
    # Initialize the game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien_Invasion")

    play_button = Button(ai_settings, screen , "Play")
    # Create an instance to store game statistics and create a scoreboard.
    stats = GameData(ai_settings)
    sb = Scoreboard(ai_settings , screen, stats)

    ship = Ship(ai_settings,screen)  # Make a ship
    bullets = Group()   # make a group to store bullet in
    alien = Alien(ai_settings, screen)
    aliens = Group()  # Make a group of aliens
    gf.create_fleet(ai_settings, screen,ship, aliens)  # Create the fleet of aliens

    while True:
        gf.check_events(ai_settings, screen, stats , sb, play_button , ship, aliens,bullets)
        if stats.game_active:
            ship.update() # updating the position of the ship
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen ,stats,sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens ,bullets, play_button)  # Updating the screen after each event
                    
run_game()