import pygame
from bullet import Bullet

WIDTH = 800
HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_frames = []
        for i in range(1, 3):
            self.player_frames.append(pygame.image.load('graphics/player/fly_{}.png'.format(i)).convert_alpha())
        self.player_frames = [pygame.transform.smoothscale(image, (110, 75)) for image in self.player_frames]
        self.player_frame_index = 0
        self.player_shoot = []
        for i in range(1, 6):
            self.player_shoot.append(pygame.image.load('graphics/player/Shoot ({}).png'.format(i)).convert_alpha())
        self.player_shoot = [pygame.transform.smoothscale(image, (110, 75)) for image in self.player_shoot]
        self.player_shoot_index = 0
        
        self.image = self.player_frames[self.player_frame_index]
        self.rect = self.image.get_rect(midbottom = (200, (HEIGHT/2)))

        self.bullet_active = False
        self.active_time = 0

        self.ready = True
        self.bullet_time = 0
        self.bullet_cooldown = 600
        self.indicator_active = False

        self.shoot_sound = pygame.mixer.Sound('audio/shoot.wav')
        self.shoot_sound.set_volume(0.3)

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
            self.indicator_active = True
            if keys[pygame.K_SPACE] and self.ready:
                self.shoot_bullet()
                self.shoot_sound.play()
                self.ready = False
                self.bullet_time = pygame.time.get_ticks()

    def cheat(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_i]:
            self.bullet_active = True
            self.active_time = pygame.time.get_ticks()
            
    def player_constraint(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def animation_state(self):
        keys = pygame.key.get_pressed()
        if self.bullet_active and keys[pygame.K_SPACE]:
            self.player_shoot_index += 1
            if self.player_shoot_index >= len(self.player_shoot):
                self.player_shoot_index = 0
            self.image = self.player_shoot[self.player_shoot_index]
        else:
            self.player_frame_index += 0.1
            if self.player_frame_index >= len(self.player_frames):
                self.player_frame_index = 0
            self.image = self.player_frames[int(self.player_frame_index)]

    def deactivate(self):
        bullet_current_time = pygame.time.get_ticks()
        if bullet_current_time - self.active_time >= 5000:
            self.bullet_active = False
            self.indicator_active = False

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
        self.cheat()
        self.bullets.update()