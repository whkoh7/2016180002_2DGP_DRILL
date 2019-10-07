from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024


def handle_events():
    # fill here
    global running, draw
    global C_x, C_y, M_x, M_y, F_x, F_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            draw = False
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            F_x, F_y = event.x, KPU_HEIGHT - 1 - event.y
            running = True
        elif event.type == SDL_MOUSEMOTION:
            M_x, M_y = event.x, KPU_HEIGHT - 1 - event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            draw = False
    pass


open_canvas(KPU_WIDTH, KPU_HEIGHT)

# fill here
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
cursor = load_image('hand_arrow.png')
hide_cursor()
C_x, C_y = KPU_WIDTH // 2, KPU_HEIGHT // 2
M_x, M_y = KPU_WIDTH // 2, KPU_HEIGHT // 2
frame = 0
running = False
draw = True
direction=1
i = 0
while draw:
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character.clip_draw(frame * 100, 100 * direction, 100, 100, C_x, C_y)
    cursor.clip_draw(0, 0, 50, 52, M_x + 25, M_y - 25)
    update_canvas()
    frame = (frame + 1) % 8
    if running == True:
        if C_x<F_x:
            direction=1
        elif C_x>=F_x:
            direction=0
        if C_x == F_x and C_y == F_y:
            i = 0
            running = False
        elif running == True and i != 100:
            t = i / 100
            C_x = (1 - t) * C_x + t * F_x
            C_y = (1 - t) * C_y + t * F_y
            i += 1
    delay(0.01)
    handle_events()

close_canvas()
