from src.game_classes import Bird, Base, Pipe
import pygame
import neat
import os
import math

WIN_WITDH = 800
WIN_HEIGHT = 800
DRAW_LINES = False

pygame.font.init()
pygame.display.set_caption('Flappy Bird')

WIN = pygame.display.set_mode((WIN_WITDH, WIN_HEIGHT))
SCORE_FONT = pygame.font.SysFont('arial', 30)
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bg.png')), (800, 800))
WHITE = (255, 255, 255)


def draw_window(window, bird, base, pipe):
    window.blit(BG_IMG, (0,0))

    pipe.draw(win=window)

    base.draw(win=window)
    bird.draw(win=window)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    bird = Bird(250, 250)

    base = Base(730)
    pipe = Pipe(600)
    run = True
    while run:
        clock.tick(30)
        base.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        pipe.move(time=pygame.time.get_ticks())
        draw_window(WIN, bird, base, pipe)


if __name__ == '__main__':
    main()