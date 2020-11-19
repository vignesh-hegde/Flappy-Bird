import pygame
import random
import time

pygame.init()
pygame.display.set_caption('Flappy Bird by Vignesh Hegde')
font = pygame.font.Font('freesansbold.ttf', 32)
bg = pygame.image.load("bg.png")
start = pygame.image.load("start.png")
end = pygame.image.load("end.png")
bird_image = pygame.image.load("bird.png")
score_sound = pygame.mixer.Sound('point.wav')
crash_sound = pygame.mixer.Sound('hit.wav')
flap_sound = pygame.mixer.Sound('wing.wav')

size_x = 300
size_y = 500
pipe_width = 40
FPS = 50
distance = 140
screen = pygame.display.set_mode((size_x, size_y))

pipe_color = (112, 137, 79)
Refresh = (0, 0, 0)
clock = pygame.time.Clock()
RUN = True


class Pipe:
    def __init__(self, top, bottom, loc):
        self.top = top
        self.bottom = bottom
        self.loc = loc

    def dec(self):
        self.loc -= 1


def NewPipe():
    temp = random.randint(9, 11) * 10
    temp2 = (size_y - 80 - temp) // 10
    top = random.randint(8, temp2) * 10
    bottom = top + temp
    return Pipe(top, bottom, size_x)


def NewPipe1():
    temp = random.randint(9, 11) * 10
    temp2 = (size_y - 80 - temp) // 10
    top = random.randint(8, temp2) * 10
    bottom = top + temp
    return Pipe(top, bottom, pipes[-1].loc + distance)


def isColide(pos, my):
    if pos <= my[0] or pos >= my[1] - 25:
        return True


def start_screen(ini=False):
    global pipes
    global current_pipe
    global score
    global u
    global vel
    global temp
    global temp2
    global ss

    pipes = [NewPipe(), NewPipe(), NewPipe()]
    pipes[1].loc = pipes[0].loc + distance
    pipes[2].loc = pipes[1].loc + distance
    current_pipe = (pipes[0].top, pipes[0].bottom)
    score = 0
    u = 90
    vel = False
    temp = 0
    temp2 = 0
    ss = False
    if ini:
        return 0

    screen.blit(start, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
                return 0
            elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()


def exit_screen():
    screen.blit(end, (0, 0))
    screen.blit(font.render(str(score), 1, (255, 255, 255)), ((size_x // 3)+35, size_y // 4))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_SPACE:
                    start_screen(True)
                    return False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


pipes = []
current_pipe = ()
score = 0
u = 0
vel = False
temp = 0
temp2 = 0
ss = True
start_screen()
while RUN:
    clock.tick(FPS)

    if vel and temp < 10:
        u -= 5
        temp += 1
        if temp == 9:
            temp = 0
            temp2 = 0
            vel = False
    else:
        if temp2 < 8:
            temp2 += 1
            u += 1
        else:
            u += 3
    if u >= size_y - 23:
        u = size_y - 23
    elif u <= 4:
        u = 4

    if pipes[0].loc <= -pipe_width:
        pipes.append(NewPipe1())
        pipes.pop(0)
        current_pipe = (pipes[0].top, pipes[0].bottom)
        ss = not ss

    screen.blit(bg, (0, 0))
    screen.blit(bird_image, (50, u))
    pipes[0].dec()
    pipes[1].dec()
    pipes[2].dec()
    pygame.draw.rect(screen, pipe_color, (pipes[0].loc, 0, pipe_width, pipes[0].top))
    pygame.draw.rect(screen, pipe_color, (pipes[1].loc, 0, pipe_width, pipes[1].top))
    pygame.draw.rect(screen, pipe_color, (pipes[2].loc, 0, pipe_width, pipes[2].top))
    pygame.draw.rect(screen, pipe_color, (pipes[0].loc, pipes[0].bottom, pipe_width, 500))
    pygame.draw.rect(screen, pipe_color, (pipes[1].loc, pipes[1].bottom, pipe_width, 500))
    pygame.draw.rect(screen, pipe_color, (pipes[2].loc, pipes[2].bottom, pipe_width, 500))
    screen.blit(font.render(str(score), 1, (255, 255, 255)), (((size_x // 3)+35, 20)))

    if pipes[0].loc <= 10 and ss:
        score_sound.play()
        score += 1
        ss = not ss

    pygame.display.flip()

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()
            X = False
        elif keys[pygame.K_SPACE]:
            flap_sound.play()
            vel = True
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if 1 <= pipes[0].loc <= 35+ pipe_width or u >= size_y-23:
        if isColide(u, current_pipe):
            crash_sound.play()
            time.sleep(1)
            if exit_screen():
                pygame.quit()
                exit()
    pygame.display.update()
exit()
