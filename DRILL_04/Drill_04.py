from pico2d import *

open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')

direction = 1
x = 0
frame = 0

while True:
    if direction == 1:
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(frame * 100, 100, 100, 100, x, 90)
        update_canvas()
        frame = (frame + 1) % 8
        x += 5
        get_events()
        if x == 800:
            direction = 0
    elif direction == 0:
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(frame * 100, 0, 100, 100, x, 90)
        update_canvas()
        frame = (frame + 1) % 8
        x -= 5
        get_events()
        if x == 0:
            direction = 1

# 여기를 채우세요.


close_canvas()
