from plistlib import Data

from pico2d import *

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SHIFT_DOWN, SHIFT_UP, DASH_TIMER = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,

    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,

    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
}


# Boy States
class IdleState:
    @staticmethod
    def enter(boy, event):
        if event is RIGHT_DOWN:
            boy.velocity += 1
        elif event is LEFT_DOWN:
            boy.velocity -= 1
        elif event is RIGHT_UP:
            boy.velocity -= 1
        elif event is LEFT_UP:
            boy.velocity += 1
        boy.timer = 1000

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.timer -= 1
        if boy.timer is 0:
            boy.add_event(SLEEP_TIMER)

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, 300, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 200, 100, 100, boy.x, boy.y)


class RunState:
    @staticmethod
    def enter(boy, event):
        if event is SHIFT_UP:
            boy.speed = 1
        if event is RIGHT_DOWN:
            boy.velocity += 1
        elif event is LEFT_DOWN:
            boy.velocity -= 1
        elif event is RIGHT_UP:
            boy.velocity -= 1
        elif event is LEFT_UP:
            boy.velocity += 1
        elif event is DASH_TIMER:
            boy.speed = 1
        boy.dir = boy.velocity

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.timer -= 1
        boy.x += boy.velocity * boy.speed
        boy.x = clamp(25, boy.x, 800 - 25)

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 0, 100, 100, boy.x, boy.y)


class DashState:
    @staticmethod
    def enter(boy, event):
        if event is SHIFT_DOWN:
            boy.speed = 3
            boy.dashtimer = 100
        if event is SHIFT_UP:
            boy.speed = 1
            boy.dashtimer = 0

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.dashtimer -= 1
        if boy.dashtimer is 0:
            boy.add_event(DASH_TIMER)

        boy.frame = (boy.frame + 1) % 8
        boy.timer -= 1
        boy.x += boy.velocity * boy.speed
        boy.x = clamp(25, boy.x, 800 - 25)
        pass

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 0, 100, 100, boy.x, boy.y)


class SleepState:
    @staticmethod
    def enter(boy, event):
        boy.frame = 0

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.dir is 1:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100,
                                          -3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)


next_state_table = {
    IdleState: {
        RIGHT_DOWN: RunState,
        LEFT_DOWN: RunState,
        SLEEP_TIMER: SleepState,
        SHIFT_UP: IdleState,
        SHIFT_DOWN: IdleState,
    },
    RunState: {
        RIGHT_UP: IdleState,
        LEFT_UP: IdleState,
        SHIFT_DOWN: DashState,
        SHIFT_UP: DashState,
    },
    SleepState: {
        LEFT_DOWN: RunState,
        RIGHT_DOWN: RunState,
        SHIFT_UP: SleepState,
        SHIFT_DOWN: SleepState,
    },
    DashState: {
        RIGHT_UP: IdleState,
        RIGHT_DOWN: RunState,
        LEFT_UP: IdleState,
        LEFT_DOWN: RunState,
        SHIFT_UP: RunState,
        DASH_TIMER: RunState,
    },
}


class Boy:
    image = None

    def __init__(self):
        self.x, self.y = 800 // 2, 90
        if Boy.image is None:
            Boy.image = load_image('animation_sheet.png')
        self.dir = 1
        self.speed = 1
        self.velocity = 0
        self.frame = 0
        self.sleeptimer = 0
        self.dashtimer = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)
        pass

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            print(self.cur_state, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        pass

    def draw(self):
        self.cur_state.draw(self)
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass