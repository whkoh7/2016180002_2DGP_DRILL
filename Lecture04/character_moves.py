from pico2d import *
import math
open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

# fill here
speed=5

while(True) :
    
    x=0
    while (x<800):
        clear_canvas_now()
        grass.draw_now(400,30)
        character.draw_now(x,90)
        x=x+speed
        delay(0.01)

    x=90
    while(x<550):
        clear_canvas_now()
        grass.draw_now(400,30)
        character.draw_now(800,x)
        x=x+speed
        delay(0.01)

    x=800
    while (x>0):
        clear_canvas_now()
        grass.draw_now(400,30)
        character.draw_now(x,550)
        x=x-speed
        delay(0.01)

    x=550
    while(x>90):
        clear_canvas_now()
        grass.draw_now(400,30)
        character.draw_now(0,x)
        x=x-speed
        delay(0.01)

    x=0
    while(x<360):
        clear_canvas_now()
        grass.draw_now(400,30)
        character.draw_now(400+200*math.cos(x/360*2*math.pi),300+200*math.sin(x/360*2*math.pi))
        x=x+speed
        delay(0.01)

close_canvas()
