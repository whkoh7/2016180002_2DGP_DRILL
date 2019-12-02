import random
import json
import pickle
import os

from pico2d import *
import game_framework
import game_world
import main_state

import world_build_state

name = "RankingState"

boy = None
time = 0
font = None

def enter():
    # game world is prepared already in world_build_state
    global time
    global font
    global boy
    boy = world_build_state.get_boy()
    time = boy.survival
    font = load_font('ENCR10B.TTF', 20)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(world_build_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            game_world.save()
        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()




def draw():
    clear_canvas()
    font.draw(0,200,'(Time : %3.2f)'%time,(0,0,0))
    update_canvas()
