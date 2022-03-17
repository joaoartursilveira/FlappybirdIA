from src.game_classes import Bird, Base, Pipe
import pygame
import neat
import os

WIN_WITDH = 500
WIN_HEIGHT = 800
DRAW_LINES = True

pygame.font.init()
pygame.display.set_caption('Flappy Bird')

WIN = pygame.display.set_mode((WIN_WITDH, WIN_HEIGHT))
SCORE_FONT = pygame.font.SysFont('arial', 30)
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 50)

def draw_lines(window, bird, pipes, pipe_ind):
    try:
        bird_center = (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2)
        pipetop_center = (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height)
        pipedown_center = (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom)
        pygame.draw.line(window, (255,0,0), bird_center, pipetop_center, 5)
        pygame.draw.line(window, (255,0,0), bird_center, pipedown_center, 5)
    except:
        pass

def draw_window(window, birds, base, pipes, score, pipe_ind):
    count = score
    window.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win=window)

    text_score = SCORE_FONT.render(f'Score: {score}', 1, (255,255,255))
    window.blit(text_score, (text_score.get_width()-60, 7))
    base.draw(win=window)

    for bird in birds:
        if DRAW_LINES:
            draw_lines(window, bird, pipes, pipe_ind)
        bird.draw(win=window)

    window.blit(SCORE_FONT.render(f'Species: {len(birds)}', 1, (255,255,255)), (30, 35))
    pygame.display.update()


def main(genomes, config):
    clock = pygame.time.Clock()
    nets = []
    birds = []
    ge = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    score = 0
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for index_bird, bird in enumerate(birds):
            bird.move()
            ge[index_bird].fitness += 0.1
            y1 = abs(bird.y - pipes[pipe_ind].height)
            y2 = abs(bird.y - pipes[pipe_ind].bottom)
            output = nets[index_bird].activate((bird.y, y1, y2))
            if output[0] > 0.5:
                bird.jump()

        base.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            for index_bird, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[index_bird].fitness -= 1
                    for list in [birds, nets, ge]:
                        list.pop(index_bird)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(WIN_WITDH))

        for r in rem:
            pipes.remove(r)

        for index_bird, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                for list in [birds, nets, ge]:
                    list.pop(index_bird)

        draw_window(WIN, birds, base, pipes, score, pipe_ind)


if __name__ == '__main__':
    run(r'./src/config-feedforward.txt')