import pygame
from random import randint

HEIGHT = 600

class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/item/item.png').convert_alpha()
        self.rect = self.image.get_rect(bottomright = (randint(1000, 1200), randint(60, HEIGHT)))

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.rect.x -= 5
        self.destroy()