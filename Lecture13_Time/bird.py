import game_framework
from pico2d import *

import game_world

# Bird Run Speed
# fill expressions correctly
PIXEL_PER_METER = (182.0 / 1.82)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # km/hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Bird Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


class Bird:

    def __init__(self):
        self.x, self.y = 1600 // 2, 250
        self.image = load_image('bird_animation.png')
        self.size_x, self.size_y = 182, 167
        self.dir = 1
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if self.dir == 1:
            self.x += RUN_SPEED_PPS * game_framework.frame_time
        elif self.dir == 0:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time

        if self.x < 0:
            self.dir = 1
        if self.x > 1600:
            self.dir = 0

        pass

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame % 5) * self.size_x, int(self.frame / 5) * self.size_y+self.size_y,
                                           self.size_x, self.size_y, math.radians(0), '', self.x, self.y,
                                           self.size_x, self.size_y)
        elif self.dir == 0:
            self.image.clip_composite_draw(int(self.frame % 5) * self.size_x, int(self.frame / 5) * self.size_y+self.size_y,
                                           self.size_x, self.size_y, math.radians(180), 'v', self.x, self.y,
                                           self.size_x, self.size_y)

        # fill here

    def handle_event(self, event):
        pass
