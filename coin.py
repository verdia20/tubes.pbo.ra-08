import pygame
from random import randint

SCREEN_HEIGHT = 600

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.coin_frames = []
        for i in range(14):
            self.coin_frames.append(pygame.image.load('graphics/coin/coin{}.png'.format(i)).convert_alpha())
        self.coin_frames = [pygame.transform.smoothscale(image, (69, 63)) for image in self.coin_frames]
        self.coin_frame_index = 0

        self.image = self.coin_frames[self.coin_frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1000, 1200), randint(60, SCREEN_HEIGHT)))
        self.vel = randint(4, 7)

    # animasi coin
    def animation_state(self):
        self.coin_frame_index += 1
        if self.coin_frame_index >= len(self.coin_frames):
            self.coin_frame_index = 0
        self.image = self.coin_frames[self.coin_frame_index]

    # menghapus coin jika sudah keluar layar
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self.vel
        self.destroy()