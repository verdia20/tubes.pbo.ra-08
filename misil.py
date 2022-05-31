import pygame
from random import randint

SCREEN_HEIGHT = 600

class Misil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.misil_frames = []
        for i in range(3):
            self.misil_frames.append(pygame.image.load('graphics/misil/misil{}.png'.format(i)).convert_alpha())
        self.misil_frames = [pygame.transform.smoothscale(image, (83, 45)) for image in self.misil_frames]
        self.misil_frame_index = 0
        
        self.image = self.misil_frames[self.misil_frame_index]
        self.rect = self.image.get_rect(bottomright = (randint(1000, 1200), randint(50, SCREEN_HEIGHT)))
        self.vel = randint(4, 7)

    # animasi misil
    def animation_state(self):
        self.misil_frame_index += 1
        if self.misil_frame_index >= len(self.misil_frames):
            self.misil_frame_index = 0
        self.image = self.misil_frames[self.misil_frame_index]

    # menghapus misil jika sudah keluar layar
    def destroy(self):
        if self.rect.left <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self.vel
        self.destroy()