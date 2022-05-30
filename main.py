import pygame
import os
from sys import exit
from random import randint
from player import Player
from misil import Misil
from coin import Coin
from cloud import Cloud
from item import Item
from button import Button

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Game:
    def __init__(self):
        # player setup
        player_sprite = Player()
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.misil = pygame.sprite.Group()
        self.coin = pygame.sprite.Group()
        self.cloud = pygame.sprite.Group()
        self.item = pygame.sprite.Group()
        self.game_active = False
        self.score = 0
        self.high_score = 0

        # audio setup
        self.bg_music = pygame.mixer.Sound('audio/airship.flac')
        self.bg_music.set_volume(0.5)
        self.intro_music = pygame.mixer.Sound('audio/happy.mp3')
        self.intro_music.set_volume(0.5)
        self.game_over_music = pygame.mixer.Sound('audio/sunshine.mp3')
        self.game_over_music.set_volume(0.5)
        self.coin_sound = pygame.mixer.Sound('audio/coin.mp3')
        self.coin_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('audio/explosion.flac')
        self.explosion_sound.set_volume(0.5)
        self.dead_sound = pygame.mixer.Sound('audio/dead.flac')
        self.dead_sound.set_volume(0.5)
        self.item_sound = pygame.mixer.Sound('audio/item.mp3')
        self.item_sound.set_volume(0.5)
        self.wind_sound = pygame.mixer.Sound('audio/wind.wav')
        self.wind_sound.set_volume(0.5)

        # game additonal setup
        self.bg_surface = pygame.image.load('graphics/background.png').convert_alpha()
        self.bg_surface = pygame.transform.smoothscale(self.bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.indicator = pygame.image.load('graphics/player/intro.png').convert_alpha()
        self.indicator = pygame.transform.smoothscale(self.indicator, (55, 37))
        self.indicator_rect = self.indicator.get_rect(center = (40, 30))

    def get_font(self, size):
        return pygame.font.Font("font/kenvector_future_thin.ttf", size)
        
    def display_score(self):
        score_surf = self.get_font(25).render(f'Score: {self.score}', False, ('Black'))
        score_rect = score_surf.get_rect(center = ((SCREEN_WIDTH/2), 30))
        screen.blit(score_surf, score_rect)

    def high_score_check(self):
        if os.path.exists('high_score.txt'):
            with open('high_score.txt', 'r') as file:
                self.high_score = int(file.read())

    def collisions_sprite(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.misil, False):
            self.dead_sound.play()
            self.misil.empty()
            self.coin.empty()
            self.cloud.empty()
            self.item.empty()
            self.player.sprite.bullets.empty()
            self.player.sprite.bullet_active = False
            self.player.sprite.indicator_active = False
            return False
        return True

    def collisions_bullet(self):
        for bullet in self.player.sprite.bullets:
            if pygame.sprite.spritecollide(bullet, self.misil, True):
                self.explosion_sound.play()
                bullet.kill()
                return True
        return False

    def item_indicator(self):
        if self.player.sprite.indicator_active:
            screen.blit(self.indicator, self.indicator_rect)

    def cheat(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.score += 1
        if keys[pygame.K_o]:
            self.game_active = False
            self.dead_sound.play()
            self.misil.empty()
            self.coin.empty()
            self.cloud.empty()
            self.item.empty()
            self.player.sprite.bullets.empty()
            self.player.sprite.bullet_active = False

    def main(self):
        self.bg_music.play(-1)
        self.wind_sound.play(-1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.game_active:
                    if event.type == obstacle_timer:
                        self.misil.add(Misil())
                    if event.type == coin_timer:
                        self.coin.add(Coin())
                    if event.type == cloud_timer:
                        self.cloud.add(Cloud())
                    if event.type == item_timer:
                        self.item.add(Item())

            if self.game_active:
                screen.blit(self.bg_surface, (0, 0))
                self.high_score_check()

                hit = pygame.sprite.spritecollide(self.player.sprite, self.coin, True)
                if hit:
                    self.coin_sound.play()
                    self.score+=1

                item_hit = pygame.sprite.spritecollide(self.player.sprite, self.item, True)
                if item_hit:
                    self.item_sound.play()
                    self.player.sprite.bullet_active = True
                    self.player.sprite.active_time = pygame.time.get_ticks()
                
                self.player.draw(screen)
                self.player.update()
                self.player.sprite.bullets.draw(screen)
                self.item.draw(screen)
                self.item.update()
                self.misil.draw(screen)
                self.misil.update()
                self.coin.draw(screen)
                self.coin.update()
                self.cloud.draw(screen)
                self.cloud.update()
                self.item_indicator()
                self.display_score()

                if self.collisions_bullet():
                    self.score += 10
                self.game_active = self.collisions_sprite()
                self.cheat()
            else:
                if self.score > self.high_score:
                    self.high_score = self.score
                    with open('high_score.txt', 'w') as file:
                        file.write(str(self.high_score))

                self.bg_music.stop()
                self.wind_sound.stop()
                self.game_over()

            pygame.display.update()
            clock.tick(60)

    def game_over(self):
        self.game_over_music.play()
        game_over_message = self.get_font(40).render('Game Over', True, (203,19,13))
        game_over_message_rect = game_over_message.get_rect(center = ((SCREEN_WIDTH/2), 100))
        score_massage = self.get_font(25).render(f'Your score: {self.score}', True, ('Black'))
        score_massage_rect = score_massage.get_rect(center = ((SCREEN_WIDTH/2), 200))
        high_score_message = self.get_font(18).render(f'High score: {self.high_score}', True, ('Black'))
        high_score_message_rect = high_score_message.get_rect(center = (700, 20))
        menu_message = self.get_font(15).render(f'esc to return to main menu', True, ('Black'))
        menu_message_rect = menu_message.get_rect(center = (140, 20))
        game_message = self.get_font(25).render('Press space to play again', True, ('Black'))
        game_message_rect = game_message.get_rect(center = ((SCREEN_WIDTH/2), 500))
        player_dead = pygame.image.load('graphics/player/dead.png').convert_alpha()
        player_dead = pygame.transform.rotozoom(player_dead, 0, 0.45)
        player_dead_rect = player_dead.get_rect(center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2)))

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False
                        self.game_active = True
                        self.game_over_music.stop()
                        self.score = 0
                        self.main()
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        self.game_over_music.stop()
                        self.main_menu()
                        
            screen.fill('#8bf8e3')
            screen.blit(game_over_message, game_over_message_rect)
            screen.blit(score_massage, score_massage_rect)
            screen.blit(high_score_message, high_score_message_rect)
            screen.blit(menu_message, menu_message_rect)
            screen.blit(game_message, game_message_rect)
            screen.blit(player_dead, player_dead_rect)
            pygame.display.update()

    def main_menu(self):
        title_text = self.get_font(35).render('Aircraft: Fly Forever', True, ('#cb130d'))
        title_rect = title_text.get_rect(center = (400, 30))
        menu_text = self.get_font(35).render("MAIN MENU", True, "Black")
        menu_rect = menu_text.get_rect(center=(400, 300))
        copyright = self.get_font(10).render('Copyright © 2022 by Ganbaru Power', True, 'Black')
        copyright_rect = copyright.get_rect(center=(115, 585))
        misil = pygame.image.load('graphics/misil/misil0.png').convert_alpha()
        misil = pygame.transform.smoothscale(misil, (83, 45))
        misil_rect = misil.get_rect(center=(700, 500))
        coin = pygame.image.load('graphics/coin/Coin0.png').convert_alpha()
        coin = pygame.transform.smoothscale(coin, (69, 63))
        coin_rect = coin.get_rect(center=(100, 200))
        player_stand = pygame.image.load('graphics/player/intro.png').convert_alpha()
        player_stand =  pygame.transform.rotozoom(player_stand, 0, 0.45)
        player_stand_rect = player_stand.get_rect(center = (400, 150))
        
        self.intro_music.play(-1)
        run = True
        while run:
            screen.fill('#c0e8ec')
            menu_mouse_pos = pygame.mouse.get_pos()

            play_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(400, 375), 
                                text_input="PLAY", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")
            quit_button = Button(image=pygame.image.load("graphics/Button Rect.png"), pos=(400, 475), 
                                text_input="QUIT", font=self.get_font(35), base_color="Black", hovering_color="#baf4fc")

            screen.blit(title_text, title_rect)
            screen.blit(player_stand, player_stand_rect)
            screen.blit(menu_text, menu_rect)
            screen.blit(copyright, copyright_rect)
            screen.blit(misil, misil_rect)
            screen.blit(coin, coin_rect)

            for button in [play_button, quit_button]:
                button.change_color(menu_mouse_pos)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(menu_mouse_pos):
                        run = False
                        self.intro_music.stop()
                        self.game_active = True
                        self.main()
                    if quit_button.check_for_input(menu_mouse_pos):
                        pygame.quit()
                        exit()

            pygame.display.update()
        
    def run(self):
        self.main_menu()

pygame.init()
pygame.display.set_caption('Aircraft: Fly Forever')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1000, 1500))
coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, randint(1000, 1500))
cloud_timer = pygame.USEREVENT + 3
pygame.time.set_timer(cloud_timer, randint(1500, 2000))
item_timer = pygame.USEREVENT + 4
pygame.time.set_timer(item_timer, randint(8000, 10000))

# game run
game = Game()
game.run()