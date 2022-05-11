import pygame
from sys import exit
from random import randint
from player import Player
from misil import Misil
from coin import Coin
from cloud import Cloud
from item import Item

WIDTH = 800
HEIGHT = 600

class Game:
    def __init__(self):
        # player setup
        player_sprite = Player()
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.misil = pygame.sprite.Group()
        self.coin = pygame.sprite.Group()
        self.cloud = pygame.sprite.Group()
        self.item = pygame.sprite.Group()
        self.game_font = pygame.font.Font('font/kenvector_future_thin.ttf', 30)
        self.game_active = False
        self.score = 0

        # audio
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
        
    def display_score(self):
        score_surf = self.game_font.render(f'Score: {self.score}', False, (64, 64, 64))
        score_rect = score_surf.get_rect(center = ((WIDTH/2), 50))
        screen.blit(score_surf, score_rect)

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
            indicator = pygame.image.load('graphics/player/intro.png').convert_alpha()
            indicator = pygame.transform.smoothscale(indicator, (44, 30))
            indicator_rect = indicator.get_rect(center = ((50), (HEIGHT-50)))
            screen.blit(indicator, indicator_rect)

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

    def game_intro(self):
        self.intro_music.play()
        game_name = self.game_font.render('Aircraft: Fly Forever', False, (27,124,55))
        game_name_rect = game_name.get_rect(center = ((WIDTH/2), 50))
        game_message = self.game_font.render('Press any key to start', False, (27,124,55))
        game_message_rect = game_message.get_rect(center = ((WIDTH/2), 500))
        player_stand = pygame.image.load('graphics/player/intro.png').convert_alpha()
        player_stand =  pygame.transform.rotozoom(player_stand, 0, 0.45)
        player_stand_rect = player_stand.get_rect(center = ((WIDTH/2), (HEIGHT/2)))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.intro_music.stop()
                    run = False
                    self.game_active = True
            screen.fill('#c0e8ec')
            screen.blit(game_name, game_name_rect)
            screen.blit(game_message, game_message_rect)
            screen.blit(player_stand, player_stand_rect)
            pygame.display.update()

    def game_over(self):
        self.game_over_music.play()
        player_dead = pygame.image.load('graphics/player/dead.png').convert_alpha()
        player_dead = pygame.transform.rotozoom(player_dead, 0, 0.45)
        player_dead_rect = player_dead.get_rect(center = ((WIDTH/2), (HEIGHT/2)))
        game_over_message = self.game_font.render('Game Over', False, (203,19,13))
        game_over_message_rect = game_over_message.get_rect(center = ((WIDTH/2), 50))
        score_massage = self.game_font.render(f'Your score: {self.score}', False, (27,124,55))
        score_massage_rect = score_massage.get_rect(center = ((WIDTH/2), 200))
        game_message = self.game_font.render('Press any key to start', False, (27,124,55))
        game_message_rect = game_message.get_rect(center = ((WIDTH/2), 500))

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.game_active = True
                    self.game_over_music.stop()
                    self.bg_music.play(-1)
                    self.score = 0
                    run = False
            
            screen.fill('#c0e8ec')
            screen.blit(game_over_message, game_over_message_rect)
            screen.blit(score_massage, score_massage_rect)
            screen.blit(game_message, game_message_rect)
            screen.blit(player_dead, player_dead_rect)
            pygame.display.update()

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
                screen.blit(bg_surface, (0, 0))
                
                hit = pygame.sprite.spritecollide(self.player.sprite, self.coin, True)
                if hit:
                    self.coin_sound.play()
                    self.score+=1
                self.display_score()

                item_hit = pygame.sprite.spritecollide(self.player.sprite, self.item, True)
                if item_hit:
                    self.item_sound.play()
                    self.player.sprite.bullet_active = True
                    self.player.sprite.active_time = pygame.time.get_ticks()
                self.item_indicator()
                
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

                if self.collisions_bullet():
                    self.score += 10
                self.game_active = self.collisions_sprite()
                self.cheat()
            else:
                self.bg_music.stop()
                self.wind_sound.stop()
                self.game_over()

            pygame.display.update()
            clock.tick(60)
        
    def run(self):
        self.game_intro()
        self.main()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Aircraft: Fly Forever')

clock = pygame.time.Clock()

bg_surface = pygame.image.load('graphics/background.png').convert_alpha()
bg_surface = pygame.transform.smoothscale(bg_surface, (WIDTH, HEIGHT))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1000, 1500))

coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, randint(1000, 1500))

cloud_timer = pygame.USEREVENT + 3
pygame.time.set_timer(cloud_timer, randint(1500, 2000))

item_timer = pygame.USEREVENT + 4
pygame.time.set_timer(item_timer, randint(5000, 10000))

game = Game()
game.run()