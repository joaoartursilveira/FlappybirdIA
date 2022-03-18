import os
import random
import pygame
import math

PIPE_IMG = pygame.transform.scale(pygame.image.load(os.path.join('imgs','pipe.png')), (52, 500))
BASE_IMG = pygame.transform.scale(pygame.image.load(os.path.join('imgs','base.png')), (800, 112))
BIRD_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join('imgs', bird)), (40, 35)) for bird in ['bird1.png', 'bird2.png', 'bird3.png']]
VEL_GAME = 5


class Bird():
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.height = self.y
        self.vel = 0
        self.img_count = 0
        self.img_index = 0
        self.img = self.IMGS[0]
        self.rect = self.img.get_rect()

    def jump(self):
        self.vel = -10
        self.height = self.y

    def move(self):
        self.vel += 1
        d = self.vel
        if d >= 16:
            d = 16
        elif d < 0:
            d -= 2
        self.y = self.y + d

    def draw(self, win):
        self.img_count += 1
        if self.img_count > self.ANIMATION_TIME:
                self.img_count = 0
                self.img_index += 1
                if self.img_index >= len(self.IMGS):
                    self.img_index = 0
        self.img = self.IMGS[self.img_index]
        blitRotateCenter(win, self.img, (self.x, self.y), -self.vel*2)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)

class Pipe():
    GAP = 170

    def __init__(self, x) -> None:
        self.VEL = VEL_GAME
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()
        self.T = random.randrange(1, 2)
        self.A = random.randrange(0, 6)

    def set_height(self):
        self.height = random.randrange(150, 400)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self, time):
        self.x -= self.VEL
        angular = self.A*math.sin(2*3.14*time/self.T)
        self.top -= angular
        self.bottom -= angular
        
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top-round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom-round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False
        

class Base():
    IMG = BASE_IMG
    WIDTH = BASE_IMG.get_width()

    def __init__(self, y) -> None:
        self.VEL = VEL_GAME
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
    
    def collide(self, bird):
        bird_mask = bird.get_mask() 
        base_mask = pygame.mask.from_surface(self.IMG)

        base_offset = (self.x2 - bird.x, self.y-round(bird.y))

        b_point = bird_mask.overlap(base_mask, base_offset)

        if b_point:
            return True
        return False


