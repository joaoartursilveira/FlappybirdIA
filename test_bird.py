from src.game_classes import Bird, Base, Pipe
import pygame
import os
import pickle

WIN_WITDH = 800
WIN_HEIGHT = 800
DRAW_LINES = False

pygame.font.init()
pygame.display.set_caption('Flappy Bird')

WIN = pygame.display.set_mode((WIN_WITDH, WIN_HEIGHT))
SCORE_FONT = pygame.font.SysFont('arial', 30)
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bg.png')), (800, 800))
WHITE = (255, 255, 255)


def draw_window(window, bird, base, pipes, score):
    window.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win=window)

    score_text = SCORE_FONT.render(f'Score: {score}', 1, WHITE)
    window.blit(score_text, (score_text.get_width()-60, 7))
    base.draw(win=window)

    bird.draw(win=window)
    pygame.display.update()


def main(model):
    net = model
    bird = Bird(200, 250)
    base = Base(730)
    pipes = [Pipe(600)]
    score = 0

    clock = pygame.time.Clock()
    pipe_frequency = 1500
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    run = True
    while run:
        clock.tick(30)
        base.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
    
        pipe_ind = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1

        bird.move()
        y1 = abs(bird.y - pipes[pipe_ind].height)
        y2 = abs(bird.y - pipes[pipe_ind].bottom)
        output = net.activate((bird.y, y1, y2))
        if output[0] > 0.5:
            bird.jump()

        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                run = False
                pass

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            pipe.move(pygame.time.get_ticks())

        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            last_pipe = time_now
            pipes.append(Pipe(WIN_WITDH))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            run = False
            pass

        draw_window(WIN, bird, base, pipes, score)
        

if __name__ == '__main__':
    best_bird = pickle.load(open('best_bird.pickle', 'rb'))
    main(model=best_bird)
