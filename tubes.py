import pygame
from sys import exit

width = 800
height = 300

# kelas utama
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_frames = []
        for i in range(1, 3):
            self.player_frames.append(pygame.image.load('graphics/player/fly_{}.png'.format(i)).convert_alpha())
        self.player_frame_index = 0
        
        self.image = self.player_frames[self.player_frame_index]
        self.rect = self.image.get_rect()

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
        self.player_frame_index += 1
        if self.player_frame_index >= len(self.player_frames):
            self.player_frame_index = 0
        self.image = self.player_frames[self.player_frame_index]

    def update(self):
        self.player_input()
        self.player_constraint()
        self.animation_state()

class Misil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.misil_frames = []
        for i in range(3):
            self.misil_frames.append(pygame.image.load('graphics/misil/misil{}.png'.format(i)).convert_alpha())
        self.misil_frame_index = 0
        
        self.image = self.misil_frames[self.misil_frame_index]
        self.rect = self.image.get_rect()

    def animation_state(self):
        self.misil_frame_index += 1
        if self.misil_frame_index >= len(self.misil_frames):
            self.misil_frame_index = 0
        self.image = self.misil_frames[self.misil_frame_index]

    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.rect.move_ip(-5, 0)
        self.animation_state()
        self.destroy()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.coin_frames = []
        for i in range(4):
            self.coin_frames.append(pygame.image.load('graphics/coin/coin{}.png'.format(i)).convert_alpha())
        self.coin_frame_index = 0

        self.image = self.coin_frames[self.coin_frame_index]
        self.rect = self.image.get_rect()

    def animation_state(self):
        self.coin_frame_index += 1
        if self.coin_frame_index >= len(self.coin_frames):
            self.coin_frame_index = 0
        self.image = self.coin_frames[self.coin_frame_index]

    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.rect.move_ip(-5, 0)
        self.animation_state()
        self.destroy()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cloud_frames = []
        for i in range(1, 10):
            self.cloud_frames.append(pygame.image.load('graphics/clouds/cloud{}.png'.format(i)).convert_alpha())
        self.cloud_frame_index = 0

        self.image = self.cloud_frames[self.cloud_frame_index]
        self.rect = self.image.get_rect()

    def animation_state(self):
        self.cloud_frame_index += 1
        if self.cloud_frame_index >= len(self.cloud_frames):
            self.cloud_frame_index = 0
        self.image = self.cloud_frames[self.cloud_frame_index]
    
    def update(self):
        self.rect.move_ip(-5, 0)
        self.animation_state()
        self.destroy()
    
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

def game_over():
    pass

def display_score():
    pass

def collisions():
    pass


# main program
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Plane')

clock = pygame.time.Clock()
game_active = False
score = 0

bg_surface = pygame.image.load('graphics/BG.png').convert_alpha()

player = Player()
misil = Misil()
coin = Coin()
cloud = Cloud()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        else:    
            if event.type == pygame.KEYDOWN:
                game_active = True
                score = 0

    if game_active:
        screen.blit(bg_surface, (0, 0))
        
        display_score()
        
        player.draw(screen)
        player.update()

        misil.draw(screen)
        misil.update()

        coin.draw(screen)
        coin.update()

        cloud.draw(screen)
        cloud.update()

        game_active = collisions()
    else:
        game_over()

    pygame.display.update()
    clock.tick(60)