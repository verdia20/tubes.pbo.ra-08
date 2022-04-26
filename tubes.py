import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_frames = []
        for i in range(1, 3):
            self.player_frames.append(pygame.image.load('graphics/player/fly_{}.png'.format(i)).convert_alpha())
        self.player_frames = [pygame.transform.smoothscale(image, (110, 75)) for image in self.player_frames]
        self.player_frame_index = 0
        
        self.image = self.player_frames[self.player_frame_index]
        self.rect = self.image.get_rect(midbottom = (200, (height/2)))

        self.bullet_active = False
        self.active_time = 0

        self.ready = True
        self.bullet_time = 0
        self.bullet_cooldown = 600

        self.bullets = pygame.sprite.Group()

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.move_ip(0, -5)
        if keys[pygame.K_s]:
            self.rect.move_ip(0, 5)
        if keys[pygame.K_a]:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_d]:
            self.rect.move_ip(5, 0)

        if self.bullet_active:
            if keys[pygame.K_SPACE] and self.ready:
                self.shoot_bullet()
                shoot_sound.play()
                self.ready = False
                self.bullet_time = pygame.time.get_ticks()
            
    def player_constraint(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

    def animation_state(self):
        self.player_frame_index += 0.1
        if self.player_frame_index >= len(self.player_frames):
            self.player_frame_index = 0
        self.image = self.player_frames[int(self.player_frame_index)]

    def deactivate(self):
        bullet_current_time = pygame.time.get_ticks()
        if bullet_current_time - self.active_time >= 5000:
            self.bullet_active = False

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time >= self.bullet_cooldown:
                self.ready = True

    def shoot_bullet(self):
        self.bullets.add(Bullet(self.rect.center, 5))

    def update(self):
        self.player_input()
        self.player_constraint()
        self.animation_state()
        self.deactivate()
        self.recharge()
        self.bullets.update()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.bullet_frames = []
        for i in range(1, 6):
            self.bullet_frames.append(pygame.image.load('graphics/bullet/Bullet ({}).png'.format(i)).convert_alpha())
        self.bullet_frames = [pygame.transform.smoothscale(image, (36, 38)) for image in self.bullet_frames]
        self.bullet_frame_index = 0
        self.image = self.bullet_frames[self.bullet_frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = speed
    
    def animation_state(self):
        self.bullet_frame_index += 1
        if self.bullet_frame_index >= len(self.bullet_frames):
            self.bullet_frame_index = 0
        self.image = self.bullet_frames[self.bullet_frame_index]

    def destroy(self):
        if self.rect.x > width:
            self.kill()

    def update(self):
        self.rect.x += self.speed
        self.animation_state()
        self.destroy()

class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/item/item.png').convert_alpha()
        self.rect = self.image.get_rect(bottomright = (randint(1000, 1200), randint(60, height)))

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.rect.x -= 5
        self.destroy()

class Misil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.misil_frames = []
        for i in range(3):
            self.misil_frames.append(pygame.image.load('graphics/misil/misil{}.png'.format(i)).convert_alpha())
        self.misil_frames = [pygame.transform.smoothscale(image, (83, 45)) for image in self.misil_frames]
        self.misil_frame_index = 0
        
        self.image = self.misil_frames[self.misil_frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1000, 1200), randint(50, height)))
        self.vel = randint(4, 7)

    def animation_state(self):
        self.misil_frame_index += 1
        if self.misil_frame_index >= len(self.misil_frames):
            self.misil_frame_index = 0
        self.image = self.misil_frames[self.misil_frame_index]

    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self.vel
        self.destroy()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.coin_frames = []
        for i in range(14):
            self.coin_frames.append(pygame.image.load('graphics/coin/coin{}.png'.format(i)).convert_alpha())
        self.coin_frames = [pygame.transform.smoothscale(image, (69, 63)) for image in self.coin_frames]
        self.coin_frame_index = 0

        self.image = self.coin_frames[self.coin_frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1000, 1200), randint(60, height)))
        self.vel = randint(4, 7)

    def animation_state(self):
        self.coin_frame_index += 1
        if self.coin_frame_index >= len(self.coin_frames):
            self.coin_frame_index = 0
        self.image = self.coin_frames[self.coin_frame_index]

    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self.vel
        self.destroy()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cloud_frames = []
        for i in range(1, 4):
            self.cloud_frames.append(pygame.image.load('graphics/clouds/cloud{}.png'.format(i)).convert_alpha())
        self.cloud_frames = [pygame.transform.smoothscale(image, (95, 63)) for image in self.cloud_frames]
        self.cloud_frame_index = 0

        self.image = self.cloud_frames[self.cloud_frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1000, 1200), randint(60, height)))

    def animation_state(self):
        self.cloud_frame_index += 0.1
        if self.cloud_frame_index >= len(self.cloud_frames):
            self.cloud_frame_index = 0
        self.image = self.cloud_frames[int(self.cloud_frame_index)]
    
    def update(self):
        self.animation_state()
        self.rect.move_ip(-5, 0)
        self.destroy()
    
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

def display_score():
    score_surf = game_font.render(f'Score: {score}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = ((width/2), 50))
    screen.blit(score_surf, score_rect)

def collisions_sprite():
    if pygame.sprite.spritecollide(player.sprite, misil, False):
        dead_sound.play()
        misil.empty()
        coin.empty()
        cloud.empty()
        item.empty()
        player.sprite.bullets.empty()
        player.sprite.bullet_active = False
        return False
    return True

def collisions_bullet():
    for bullet in player.sprite.bullets:
        if pygame.sprite.spritecollide(bullet, misil, True):
            explosion_sound.play()
            bullet.kill()
            return True
    return False

def game_intro():
    global game_active
    intro_music.play()
    player_stand = pygame.image.load('graphics/player/intro.png').convert_alpha()
    player_stand =  pygame.transform.rotozoom(player_stand, 0, 0.45)
    player_stand_rect = player_stand.get_rect(center = ((width/2), (height/2)))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                intro_music.stop()
                run = False
                game_active = True
        screen.fill('#c0e8ec')
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
        screen.blit(player_stand, player_stand_rect)
        pygame.display.update()

def game_over():
    global game_active
    global score

    game_over_music.play()
    player_dead = pygame.image.load('graphics/player/dead.png').convert_alpha()
    player_dead = pygame.transform.rotozoom(player_dead, 0, 0.45)
    player_dead_rect = player_dead.get_rect(center = ((width/2), (height/2)))
    game_over_message = game_font.render('Game Over', False, (203,19,13))
    game_over_message_rect = game_over_message.get_rect(center = ((width/2), 50))
    score_massage = game_font.render(f'Your score: {score}', False, (27,124,55))
    score_massage_rect = score_massage.get_rect(center = ((width/2), 200))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                game_active = True
                game_over_music.stop()
                bg_music.play(-1)
                score = 0
                run = False
        
        screen.fill('#c0e8ec')
        screen.blit(game_over_message, game_over_message_rect)
        screen.blit(score_massage, score_massage_rect)
        screen.blit(game_message, game_message_rect)
        screen.blit(player_dead, player_dead_rect)
        pygame.display.update()

def main():
    global game_active
    global score

    bg_music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active:
                if event.type == obstacle_timer:
                    misil.add(Misil())
                if event.type == coin_timer:
                    coin.add(Coin())
                if event.type == cloud_timer:
                    cloud.add(Cloud())
                if event.type == item_timer:
                    item.add(Item())

        if game_active:
            screen.blit(bg_surface, (0, 0))
            
            hit = pygame.sprite.spritecollide(player.sprite, coin, True)
            if hit:
                coin_sound.play()
                score+=1
            display_score()

            item_hit = pygame.sprite.spritecollide(player.sprite, item, True)
            if item_hit:
                item_sound.play()
                player.sprite.bullet_active = True
                player.sprite.active_time = pygame.time.get_ticks()
            
            player.draw(screen)
            player.update()
            player.sprite.bullets.draw(screen)

            item.draw(screen)
            item.update()

            misil.draw(screen)
            misil.update()

            coin.draw(screen)
            coin.update()

            cloud.draw(screen)
            cloud.update()

            if collisions_bullet():
                score += 10

            game_active = collisions_sprite()
        else:
            bg_music.stop()
            game_over()

        pygame.display.update()
        clock.tick(60)

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Aircraft: Fly Forever')

clock = pygame.time.Clock()
game_font = pygame.font.Font('font/kenvector_future_thin.ttf', 30)
game_active = False
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

misil = pygame.sprite.Group()
coin = pygame.sprite.Group()
cloud = pygame.sprite.Group()
item = pygame.sprite.Group()

bg_surface = pygame.image.load('graphics/background.png').convert_alpha()
bg_surface = pygame.transform.smoothscale(bg_surface, (width, height))

# intro screen
game_name = game_font.render('Aircraft: Fly Forever', False, (27,124,55))
game_name_rect = game_name.get_rect(center = ((width/2), 50))
game_message = game_font.render('Press any key to start', False, (27,124,55))
game_message_rect = game_message.get_rect(center = ((width/2), 500))

# audio
bg_music = pygame.mixer.Sound('audio/airship.flac')
bg_music.set_volume(0.5)
game_over_music = pygame.mixer.Sound('audio/sunshine.mp3')
game_over_music.set_volume(0.5)
intro_music = pygame.mixer.Sound('audio/happy.mp3')
intro_music.set_volume(0.5)
coin_sound = pygame.mixer.Sound('audio/coin.mp3')
coin_sound.set_volume(0.5)
shoot_sound = pygame.mixer.Sound('audio/shoot.wav')
shoot_sound.set_volume(0.3)
explosion_sound = pygame.mixer.Sound('audio/explosion.flac')
explosion_sound.set_volume(0.5)
dead_sound = pygame.mixer.Sound('audio/dead.flac')
dead_sound.set_volume(0.5)
item_sound = pygame.mixer.Sound('audio/item.mp3')
item_sound.set_volume(0.5)

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1000, 1500))

coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, randint(1000, 1500))

cloud_timer = pygame.USEREVENT + 3
pygame.time.set_timer(cloud_timer, randint(1500, 2000))

item_timer = pygame.USEREVENT + 4
pygame.time.set_timer(item_timer, randint(5000, 10000))

game_intro()
main()
