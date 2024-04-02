import pygame
import sys
from bullet import Bullet
from alien import Alien
from ship import Ship
from time import sleep

def check_events(ai_settings, screen,stats, sb ,play_button, ship, aliens,  bullets):
    # Watch to the key press and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen , stats,sb , play_button,ship,aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen , stats, sb, play_button, ship,aliens,bullets, mouse_x, mouse_y):
    # only start the game when the player clicks the play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset the game settings after the game over
        ai_settings.initialize_dynamic_settings()
        # hide the mouse courser once the play button is clicked
        pygame.mouse.set_visible(False)
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            stats.reset_stats()
            stats.game_active = True

            # reset the scoreBoard images
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()
            
            # empty the list of aliens and bullets 
            aliens.empty()
            bullets.empty()

            # create the fleet and center the ship
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # respond to keypresses
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen , ship , bullets)

def check_keyup_events(event, ship):
    # respond to key releases
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def fire_bullet(ai_settings, screen , ship , bullets):
    # fire a bullet if limit not reached yet
    # Create a new bullet and add it to the bullets group
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen , ship)
            bullets.add(new_bullet)

def update_screen(ai_settings, screen , stats,sb, ship , aliens, bullets, play_button):        
    # screen.fill(ai_settings.bg_color)
    screen.blit(ai_settings.background, [0, 0])
    # redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # draw the score information
    sb.show_score()
    # draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()
        
    pygame.display.flip()  # Make the most recently drawn screen visible

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Update position of bullets and get rid of old bullets
    bullets.update()    

    # get rid of the bullets that crossed the upper part of the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats,sb, ship, aliens, bullets):
    # Check for any bullets that have hit aliens 
    # if so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if(len(aliens)== 0):
        # if the entire fleet is destroyed, start a new level
        # delete existing bullets and create new fleet.
        bullets.empty()
        ai_settings.increse_speed()
        # increase level
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen , ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    # To find the number of elements that can fit in a row
    available_space_x = ai_settings.screen_width - (2*alien_width)
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings , ship_height , alien_height):
    # to determine the no of rows can be fit on the screen
    available_space_y = (ai_settings.screen_height - (4*alien_height) - ship_height)
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows

def create_alien(ai_settings, screen , aliens, alien_number, row_number):
    # create an alien and place it in the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # creating the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # creating an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def ship_hit(ai_settings , screen, stats , sb, ship ,aliens, bullets):
    # respond to the ship being hit by alien
    if stats.ship_remain != 0:
        stats.ship_remain -= 1

        # update scoreboard
        sb.prep_ships()
        # empty the list of alien and bullets
        aliens.empty()
        bullets.empty()
        # create a new fleet and center the ship
        create_fleet(ai_settings, screen , ship, aliens)
        ship.center_ship()
        # the screen will freeze for 0.5 sec
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_fleet_edges(ai_settings, aliens):
    # respond if any aliens hace reached an edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    # drop down the whole fleet and change the fleet's direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, screen ,stats, sb, ship, aliens, bullets):
    # check for any alien that hit the bottom
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat this the same as if the ship got hit
            ship_hit(ai_settings, screen,stats,sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings,screen , stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings , aliens)
    aliens.update()
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # check for the alien ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen,stats, sb, ship, aliens, bullets)

    # check the aliens for hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    # check to see if there is new high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
