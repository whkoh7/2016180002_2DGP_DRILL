from pico2d import *
import random


# Game object class here
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Ball_21:
    def __init__(self):
        self.x, self.y = random.randint(0, 600), 599
        self.image = load_image('ball21x21.png')
        self.speed = random.randint(5, 20)
        self.move = True

    def update(self):
        if 96 > self.y > 90:
            self.y = 90
            self.move = False
        if self.move:
            self.y -= self.speed

    def draw(self):
        self.image.clip_draw(0, 0, 21, 21, self.x, self.y)


class Ball_41:
    def __init__(self):
        self.x, self.y = random.randint(0, 600), 599
        self.image = load_image('ball41x41.png')
        self.speed = random.randint(5, 20)
        self.move = True

    def update(self):
        if 96 > self.y > 90:
            self.y = 90
            self.move = False
        if self.move:
            self.y -= self.speed

    def draw(self):
        self.image.clip_draw(0, 0, 41, 41, self.x, self.y)


class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


# initialization code
open_canvas()
boy = Boy()
ball_21 = Ball_21()
ball_41 = Ball_41()
pc_ball_21 = random.randint(0, 20)
pc_ball_41 = 20 - pc_ball_21

balls21 = [Ball_21() for i in range(pc_ball_21)]
balls41 = [Ball_41() for i in range(pc_ball_41)]
team = [Boy() for i in range(11)]
grass = Grass()
running = True

# game main loop code
while running:
    handle_events()
    for boy in team:
        boy.update()

    for ball_21 in balls21:
        Ball_21.update()
    for ball_41 in balls41:
        Ball_41.update()

    boy.update()

    clear_canvas()
    grass.draw()
    boy.draw()
    for boy in team:
        boy.draw()
        for ball_21 in balls21:
            Ball_21.draw()
        for ball_41 in balls41:
            Ball_41.draw()
    update_canvas()

    delay(0.05)
# finalization code
close_canvas()
