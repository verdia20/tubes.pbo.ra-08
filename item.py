import pygame
from random import randint

SCREEN_HEIGHT = 600

class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/item/item.png').convert_alpha()
        self.rect = self.image.get_rect(bottomright = (randint(1000, 1200), randint(60, SCREEN_HEIGHT)))
        self.vel = randint(4, 7)

    # menghapus misil jika sudah keluar layar
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.rect.x -= self.vel
        self.destroy()