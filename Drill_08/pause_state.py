import random
import json
import os

from pico2d import *

import game_framework
import main_state

pauseImg = None

name = "PauseState"

frame = 0
cnt = 0


def enter():
    global pauseImg
    pauseImg = load_image('pause.png')


def exit():
    global pauseImg
    del pauseImg


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_state()
            main_state.resume()


def update(): pass


def draw():
    global frame
    global cnt
    clear_canvas()
    main_state.boy.draw()
    main_state.grass.draw()
    frame = (frame + 1) % 2
    pauseImg.clip_draw(frame * 900, 0, 900, 900, 400, 300)
    delay(0.1)
    update_canvas()
