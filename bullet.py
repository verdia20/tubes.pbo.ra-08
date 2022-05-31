import pygame

SCREEN_WIDTH = 800

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
    
    # animasi bullet
    def animation_state(self):
        self.bullet_frame_index += 1
        if self.bullet_frame_index >= len(self.bullet_frames):
            self.bullet_frame_index = 0
        self.image = self.bullet_frames[self.bullet_frame_index]

    # menghapus bullet jika sudah keluar layar
    def destroy(self):
        if self.rect.x > SCREEN_WIDTH:
            self.kill()

    def update(self):
        self.rect.x += self.speed
        self.animation_state()
        self.destroy()